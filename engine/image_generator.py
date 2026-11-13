import base64
import logging
from pathlib import Path

import requests

from engine.config import settings

logger = logging.getLogger(__name__)


class FreeQuotaExhausted(RuntimeError):
    """Raised when Cloudflare's free inference quota is exhausted."""


def generate_scene_image(
    prompt: str,
    scene_index: int,
    output_dir: str = "generated_art",
) -> Path:

    if not settings.cloudflare_account_id:
        raise RuntimeError("CLOUDFLARE_ACCOUNT_ID is missing.")

    if not settings.cloudflare_api_token:
        raise RuntimeError("CLOUDFLARE_API_TOKEN is missing.")

    if not 1 <= settings.image_steps <= 8:
        raise ValueError("IMAGE_STEPS must be between 1 and 8.")

    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)

    destination = folder / f"scene_{scene_index:03d}.png"

    if destination.exists() and destination.stat().st_size > 10_000:
        logger.info("Using cached image %s", destination)
        return destination

    headers = {
        "Authorization": f"Bearer {settings.cloudflare_api_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "prompt": prompt[:2048],
        "steps": settings.image_steps,
        "seed": scene_index * 7919,
    }

    try:
        response = requests.post(
            settings.cloudflare_url,
            headers=headers,
            json=payload,
            timeout=300,
        )
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Cloudflare request failed: {exc}"
        ) from exc

    if response.status_code in (402, 403, 429):
        raise FreeQuotaExhausted(
            "Cloudflare rejected the inference request. "
            "The free quota may be exhausted or the token may lack "
            f"permission. HTTP {response.status_code}. "
            "The workflow will stop; no paid fallback is configured."
        )

    response.raise_for_status()

    try:
        data = response.json()
        image_data = data["result"]["image"]
        image_bytes = base64.b64decode(image_data, validate=True)
    except (ValueError, KeyError, TypeError) as exc:
        raise RuntimeError(
            "Cloudflare returned an unexpected image response."
        ) from exc

    if len(image_bytes) < 10_000:
        raise RuntimeError("Generated image is unexpectedly small.")

    destination.write_bytes(image_bytes)

    logger.info("Saved scene artwork: %s", destination)

    return destination
