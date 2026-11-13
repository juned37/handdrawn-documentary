from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


PAPER = (239, 229, 207)


def create_parchment(size: tuple[int, int]) -> Image.Image:
    paper = Image.new("RGB", size, PAPER)

    noise = Image.effect_noise(size, 8).convert("L")
    noise = ImageEnhance.Contrast(noise).enhance(0.35)

    texture = Image.merge("RGB", (noise, noise, noise))

    paper = Image.blend(paper, texture, 0.045)

    return paper.filter(ImageFilter.GaussianBlur(0.25))


def prepare_artwork(
    image_path: str | Path,
    size: tuple[int, int],
) -> Image.Image:

    image = Image.open(image_path).convert("RGB")

    fitted = ImageOps.fit(
        image,
        size,
        method=Image.Resampling.LANCZOS,
    )

    parchment = create_parchment(size)

    # Keep original soft shadows and shading.
    fitted = Image.blend(fitted, parchment, 0.08)
    fitted = ImageEnhance.Color(fitted).enhance(0.82)
    fitted = ImageEnhance.Contrast(fitted).enhance(1.04)

    return fitted
