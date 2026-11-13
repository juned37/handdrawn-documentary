import re

from engine.story import Scene


STYLE_BIBLE = """
Cinematic hand-drawn historical documentary illustration.
Organic uneven ink outlines with visibly varied line thickness.
Loose pencil construction marks and delicate cross-hatching.
Soft watercolor and ink-wash shading.
Detailed fabric texture and natural robe folds.
Warm aged cream parchment background.
Restrained antique gold accents and muted earth tones.
Atmospheric natural lighting and soft shadows.
Carefully composed foreground, middle ground and background.
Museum-quality illustrated documentary artwork.

Portrait composition intended for a vertical documentary video.
No text, captions, lettering, logos or watermarks.

Absolutely avoid flat vector shapes, clip-art, generic icons,
uniform outlines, glossy 3D, photorealism and cartoon styling.
"""


def _visual_subject(narration: str) -> str:
    """
    Convert narration into a scene description.

    The complete narration is retained so that each generated
    composition is tied to its own scene.
    """
    cleaned = re.sub(r"\s+", " ", narration).strip()

    return (
        "Illustrate this exact documentary moment: "
        f"{cleaned} "
        "Choose a specific visual composition that communicates "
        "the event, environment, objects and atmosphere described. "
        "Do not reuse a generic stock composition."
    )


def create_visual_prompt(scene: Scene) -> str:
    restrictions = """
    Religious and historical care:
    Never depict Prophet Muhammad in any form, including face,
    body, silhouette, shadow or reflection.
    Do not depict any other prophet.
    If a prophet is mentioned, use respectful environmental,
    architectural or object-based imagery instead.
    Do not invent identifiable historical portraits or unsupported
    historical details.
    """

    scene.visual_prompt = (
        STYLE_BIBLE
        + "\n"
        + restrictions
        + "\nSCENE DESCRIPTION:\n"
        + _visual_subject(scene.narration)
    )

    return scene.visual_prompt
