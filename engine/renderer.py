import subprocess
from pathlib import Path

import imageio.v2 as imageio
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from engine.config import settings
from engine.image_processing import prepare_artwork


def _font(size: int):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]

    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)

    return ImageFont.load_default()


def _caption(frame: Image.Image, text: str) -> Image.Image:
    draw = ImageDraw.Draw(frame, "RGBA")
    width, height = frame.size

    font = _font(max(25, width // 25))
    max_width = width - 100

    lines = []
    current = ""

    for word in text.split():
        candidate = f"{current} {word}".strip()

        if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    lines = lines[:3]
    line_height = max(38, height // 25)
    panel_height = line_height * len(lines) + 55
    top = height - panel_height - 75

    draw.rounded_rectangle(
        (35, top, width - 35, height - 45),
        radius=18,
        fill=(239, 229, 207, 205),
        outline=(95, 72, 45, 130),
        width=2,
    )

    y = top + 22

    for line in lines:
        box = draw.textbbox((0, 0), line, font=font)
        x = (width - (box[2] - box[0])) // 2

        draw.text(
            (x, y),
            line,
            font=font,
            fill=(45, 38, 29, 255),
        )

        y += line_height

    return frame


def _animate_frame(
    artwork: Image.Image,
    progress: float,
    reveal_noise: Image.Image,
    caption: str,
) -> Image.Image:
    width, height = artwork.size

    zoom = 1.0 + (0.09 * progress)

    scaled = artwork.resize(
        (int(width * zoom), int(height * zoom)),
        Image.Resampling.LANCZOS,
    )

    extra_x = scaled.width - width
    extra_y = scaled.height - height

    left = int(extra_x * (0.35 + 0.20 * progress))
    top = int(extra_y * (0.35 + 0.20 * progress))

    frame = scaled.crop((left, top, left + width, top + height))

    threshold = int(progress * 255)

    mask = reveal_noise.point(
        lambda value: 255 if value <= threshold else 0
    )
    mask = mask.filter(ImageFilter.GaussianBlur(3))

    blank = Image.new("RGB", (width, height), (239, 229, 207))
    frame = Image.composite(frame, blank, mask)

    return _caption(frame, caption)


def render_video(
    scenes: list,
    image_paths: list[Path],
    output_path: str = "output/documentary.mp4",
    narration_audio: str | None = None,
) -> Path:
    if len(scenes) != len(image_paths):
        raise ValueError("Every scene must have one image.")

    width = settings.width
    height = settings.height
    fps = settings.fps

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    writer = imageio.get_writer(
        str(output),
        fps=fps,
        codec="libx264",
        quality=8,
        macro_block_size=1,
        ffmpeg_params=["-pix_fmt", "yuv420p"],
    )

    try:
        for scene, image_path in zip(scenes, image_paths):
            artwork = prepare_artwork(
                image_path,
                (width, height),
            )

            frame_count = max(1, int(scene.duration * fps))

            rng = np.random.default_rng(scene.index)

            noise = rng.integers(
                0,
                256,
                size=(height, width),
                dtype=np.uint8,
            )

            reveal_noise = Image.fromarray(noise, mode="L")

            for frame_number in range(frame_count):
                progress = frame_number / max(1, frame_count - 1)

                frame = _animate_frame(
                    artwork,
                    progress,
                    reveal_noise,
                    scene.narration,
                )

                writer.append_data(np.asarray(frame))

    finally:
        writer.close()

    if narration_audio:
        audio_path = Path(narration_audio)

        if not audio_path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        muxed = output.with_name(
            f"{output.stem}_with_audio.mp4"
        )

        command = [
            ffmpeg,
            "-y",
            "-i", str(output),
            "-i", str(audio_path),
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            "-movflags", "+faststart",
            str(muxed),
        ]

        subprocess.run(command, check=True)
        muxed.replace(output)

    return output
