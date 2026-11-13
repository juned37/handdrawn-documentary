import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    pollinations_api_key: str = os.getenv("POLLINATIONS_API_KEY", "")

    image_provider: str = os.getenv("IMAGE_PROVIDER", "both").lower()

    gemini_image_model: str = os.getenv(
        "GEMINI_IMAGE_MODEL",
        "gemini-3.1-flash-image",
    )

    gemini_text_model: str = os.getenv(
        "GEMINI_TEXT_MODEL",
        "gemini-2.5-flash",
    )

    pollinations_image_model: str = os.getenv(
        "POLLINATIONS_IMAGE_MODEL",
        "black-forest-labs/flux.1-schnell",
    )

    width: int = int(os.getenv("VIDEO_WIDTH", "1080"))
    height: int = int(os.getenv("VIDEO_HEIGHT", "1920"))
    fps: int = int(os.getenv("VIDEO_FPS", "24"))
    scene_seconds: int = int(os.getenv("SCENE_SECONDS", "5"))

    @property
    def providers(self) -> list[str]:
        if self.image_provider == "both":
            return ["gemini", "pollinations"]

        if self.image_provider in {"gemini", "pollinations"}:
            return [self.image_provider]

        raise ValueError(
            "IMAGE_PROVIDER must be both, gemini, or pollinations"
        )


settings = Settings()
