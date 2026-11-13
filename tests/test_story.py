from pathlib import Path

from engine.story import load_story


def test_story_is_split_into_scenes(tmp_path: Path):
    story_file = tmp_path / "story.txt"

    story_file.write_text(
        "First scene narration.\n\nSecond scene narration.",
        encoding="utf-8",
    )

    scenes = load_story(str(story_file), default_duration=6)

    assert len(scenes) == 2
    assert scenes[0].index == 1
    assert scenes[1].index == 2
    assert scenes[0].duration == 6


def test_empty_story_raises_error(tmp_path: Path):
    story_file = tmp_path / "empty.txt"
    story_file.write_text("   ", encoding="utf-8")

    try:
        load_story(str(story_file))
        assert False, "Expected ValueError"
    except ValueError:
        pass
