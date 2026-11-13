from dataclasses import dataclass
from pathlib import Path
import re


@dataclass
class Scene:
    index: int
    narration: str
    duration: float
    visual_prompt: str = ""


def load_story(
    path: str,
    default_duration: float = 5.0,
) -> list[Scene]:

    text = Path(path).read_text(encoding="utf-8").strip()

    paragraphs = [
        re.sub(r"\s+", " ", part).strip()
        for part in re.split(r"\n\s*\n", text)
        if part.strip()
    ]

    if not paragraphs:
        raise ValueError("The story file is empty.")

    return [
        Scene(
            index=i,
            narration=paragraph,
            duration=default_duration,
        )
        for i, paragraph in enumerate(paragraphs, 1)
    ]
