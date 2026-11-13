import json
import re

from google import genai

from engine.config import settings
from engine.story import Scene


STYLE_BIBLE = """
Create a cinematic hand-drawn historical documentary illustration.

VISUAL STYLE:
- Uneven organic black ink outlines.
- Visible sketch marks and variable line thickness.
- Pencil texture and delicate cross-hatching.
- Soft ink-wash and watercolor shading.
- Detailed fabric, architecture and environmental textures.
- Natural robe folds and cloth draping where appropriate.
- Warm aged cream parchment.
- Restrained antique-gold accents.
- Muted earth tones and soft shadows.

COMPOSITION:
- Every scene must have its own unique composition.
- Illustrate the actual narration, not a generic symbolic icon.
- Use foreground, middle-ground and background depth.
- Portrait 9:16 framing.
- Cinematic visual storytelling.
- Keep the main subject clear and away from the edges.

AVOID:
- Flat vector illustrations.
- Clip-art and generic icons.
- Uniform line thickness.
- Glossy 3D.
- Photorealism.
- Cartoon styling.
- Reusing the same composition for every scene.
- Text, captions, logos and watermarks.
"""


def _extract_json(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```(?:json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    return json.loads(text)


def create_visual_prompt(scene: Scene) -> str:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=settings.gemini_api_key)

    request = f"""
You are an art director for a historically careful documentary.

Create a detailed image-generation prompt for this exact narration scene.

Describe:
- The actual visual event.
- People or objects, when appropriate.
- Environment and architecture.
- Clothing and materials.
- Composition and camera perspective.
- Lighting, atmosphere and background details.

Make the composition specific to this scene.
Do not reuse a generic composition.

Historical accuracy:
Do not invent precise historical details when they are uncertain.
Use restrained, non-specific visual details where evidence is unclear.

Religious depiction restrictions:
Never depict Prophet Muhammad in any form, including face, body,
silhouette, shadow, reflection or symbolic human representation.
Do not depict any other prophet. Use respectful environmental,
architectural or object-based imagery instead.

Return valid JSON:
{{
  "visual_prompt": "Detailed image prompt"
}}

NARRATION:
{scene.narration}
"""

    response = client.models.generate_content(
        model=settings.gemini_text_model,
        contents=request,
        config={
            "response_mime_type": "application/json",
        },
    )

    data = _extract_json(response.text or "")
    prompt = data.get("visual_prompt", "").strip()

    if not prompt:
        raise ValueError("Gemini returned an empty visual prompt.")

    return f"{STYLE_BIBLE}\n\nSCENE DESCRIPTION:\n{prompt}"
