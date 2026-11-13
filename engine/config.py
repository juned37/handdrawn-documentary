import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    cloudflare_account_id: str = os.getenv(
        "CLOUDFLARE_ACCOUNT_ID", ""
    )
    cloudflare_api_token: str = os.getenv(
        "CLOUDFLARE_API_TOKEN", ""
    )

    image_model: str = (
        "@cf/black-forest-labs/flux-1-schnell"
    )

    width: int = int(os.getenv("VIDEO_WIDTH", "1080"))
    height: int = int(os.getenv("VIDEO_HEIGHT", "1920"))
    fps: int = int(os.getenv("VIDEO_FPS", "24"))
    scene_seconds: int = int(os.getenv("SCENE_SECONDS", "5"))

    # Keep inference conservative. FLUX.1 Schnell supports up to 8.
    image_steps: int = int(os.getenv("IMAGE_STEPS", "4"))

    @property
    def cloudflare_url(self) -> str:
        return (
            "https://api.cloudflare.com/client/v4/accounts/"
            f"{self.cloudflare_account_id}/ai/run/{self.image_model}"
        )


settings = Settings()
