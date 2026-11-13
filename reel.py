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
        description="Generate a hand-drawn documentary."
    )

    parser.add_argument(
        "--script",
        default="scripts/example.txt",
    )

    parser.add_argument("--audio", default=None)

    parser.add_argument(
        "--output",
        default="output/documentary.mp4",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    if not settings.cloudflare_account_id:
        raise RuntimeError("CLOUDFLARE_ACCOUNT_ID is missing.")

    if not settings.cloudflare_api_token:
        raise RuntimeError("CLOUDFLARE_API_TOKEN is missing.")

    scenes = load_story(
        args.script,
        default_duration=settings.scene_seconds,
    )

    image_paths = []

    for scene in scenes:
        logging.info("Preparing scene %s", scene.index)

        prompt = create_visual_prompt(scene)

        prompt_path = (
            Path("generated_art")
            / f"scene_{scene.index:03d}_prompt.txt"
        )

        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        prompt_path.write_text(prompt, encoding="utf-8")

        image_path = generate_scene_image(
            prompt,
            scene.index,
        )

        image_paths.append(image_path)

    result = render_video(
        scenes,
        image_paths,
        output_path=args.output,
        narration_audio=args.audio,
    )

    logging.info("Video created: %s", result)


if __name__ == "__main__":
    main()
