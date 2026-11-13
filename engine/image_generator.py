import logging
import time
from pathlib import Path
from urllib.parse import quote

import requests
from google import genai
from google.genai import types

from engine.config import settings

logger = logging.getLogger(__name__)


def _generate_with_gemini(prompt: str, destination: Path) -> None:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=settings.gemini_api_key)

    response = client.models.generate_content(
        model=settings.gemini_image_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio="9:16",
            ),
        ),
    )

    for part in response.parts:
        if part.inline_data is not None:
            part.as_image().save(destination)
            return

    raise RuntimeError("Gemini returned no image.")


def _generate_with_pollinations(
    prompt: str,
    destination: Path,
) -> None:
    if not settings.pollinations_api_key:
        raise RuntimeError("POLLINATIONS_API_KEY is not configured.")

    encoded_prompt = quote(prompt, safe="")
    url = f"https://gen.pollinations.ai/image/{encoded_prompt}"

    headers = {
        "Authorization": f"Bearer {settings.pollinations_api_key}",
    }

    params = {
        "model": settings.pollinations_image_model,
        "width": 1024,
        "height": 1792,
        "nologo": "true",
        "private": "true",
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=(30, 300),
    )
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")

    if not content_type.startswith("image/"):
        raise RuntimeError(
            f"Unexpected Pollinations response: {content_type}"
        )

    destination.write_bytes(response.content)


def generate_scene_image(
    prompt: str,
    scene_index: int,
    output_dir: str = "generated_art",
) -> Path:
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)

    destination = folder / f"scene_{scene_index:03d}.png"

    if destination.exists() and destination.stat().st_size > 10_000:
        logger.info("Using cached image: %s", destination)
        return destination

    generators = {
        "gemini": _generate_with_gemini,
        "pollinations": _generate_with_pollinations,
    }

    errors = []

    for provider in settings.providers:
        for attempt in range(2):
            try:
                logger.info(
                    "Generating scene %s using %s",
                    scene_index,
                    provider,
                )

                generators[provider](prompt, destination)

                if not destination.exists() or destination.stat().st_size < 10_000:
                    raise RuntimeError("Generated image is invalid.")

                return destination

            except Exception as exc:
                logger.warning(
                    "%s failed on attempt %s: %s",
                    provider,
                    attempt + 1,
                    exc,
                )
                errors.append(f"{provider}: {exc}")
                time.sleep(2)

    raise RuntimeError(
        f"All image providers failed for scene {scene_index}: "
        + " | ".join(errors)
    )
