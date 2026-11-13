import argparse
import logging
from pathlib import Path

from engine.config import settings
from engine.story import load_story
from engine.scene_prompts import create_visual_prompt
from engine.image_generator import generate_scene_image
from engine.renderer import render_video


def main():
    parser = argparse.ArgumentParser(
        description="Generate a hand-drawn documentary video."
    )

    parser.add_argument(
        "--script",
        default="scripts/example.txt",
    )

    parser.add_argument(
        "--audio",
        default=None,
    )

    parser.add_argument(
        "--output",
        default="output/documentary.mp4",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is missing.")

    scenes = load_story(
        args.script,
        default_duration=settings.scene_seconds,
    )

    image_paths = []

    for scene in scenes:
        logging.info("Creating prompt for scene %s", scene.index)

        scene.visual_prompt = create_visual_prompt(scene)

        prompt_file = Path("generated_art") / (
            f"scene_{scene.index:03d}_prompt.txt"
        )
        prompt_file.parent.mkdir(parents=True, exist_ok=True)

        prompt_file.write_text(
            scene.visual_prompt,
            encoding="utf-8",
        )

        image_path = generate_scene_image(
            scene.visual_prompt,
            scene.index,
        )

        image_paths.append(image_path)

    result = render_video(
        scenes=scenes,
        image_paths=image_paths,
        output_path=args.output,
        narration_audio=args.audio,
    )

    logging.info("Video generated: %s", result)


if __name__ == "__main__":
    main()
