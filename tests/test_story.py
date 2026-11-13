from pathlib import Path

import pytest

from engine.story import load_story


def test_story_creates_one_scene_per_paragraph(tmp_path: Path):
    path = tmp_path / "story.txt"

    path.write_text(
        "First scene.\n\nSecond scene.",
        encoding="utf-8",
    )

    scenes = load_story(str(path), 6)

    assert len(scenes) == 2
    assert scenes[0].index == 1
    assert scenes[1].index == 2
    assert scenes[0].duration == 6


def test_empty_story_is_rejected(tmp_path: Path):
    path = tmp_path / "empty.txt"
    path.write_text("  ", encoding="utf-8")

    with pytest.raises(ValueError):
        load_story(str(path))
