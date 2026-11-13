# Hand-Drawn Documentary

A free-first cinematic documentary and Reels generator.

Every narration scene receives its own generated image using
Cloudflare Workers AI and FLUX.1 Schnell.

## Main visual direction

- Uneven organic ink outlines
- Variable line thickness
- Pencil and cross-hatching texture
- Soft watercolor and ink-wash shading
- Detailed environments and fabric folds
- Warm parchment and restrained antique-gold accents
- A unique composition for every narration scene
- Slow camera push and irregular image reveal

This is not a fixed icon or flat vector illustration system.

## Free-first architecture

- GitHub Actions for video generation
- Cloudflare Workers AI for image generation
- FLUX.1 Schnell image model
- Local Python scene prompt composer
- Pillow for image processing
- FFmpeg for MP4 rendering

No Gemini API.
No Pollinations API.
No .env file.
No paid provider fallback.

## Cloudflare free allowance

Workers AI currently provides 10,000 Neurons per day
on the Free plan.

The allowance resets at 00:00 UTC.

When the free allowance is exhausted, inference requests
may fail. This project does not automatically switch to
a paid provider.

Check current limits and pricing:

https://developers.cloudflare.com/workers-ai/platform/pricing/

## Setup

1. Create a Cloudflare account.
2. Enable Workers AI.
3. Create an API token with permission to use Workers AI.
4. Find your Cloudflare Account ID.
5. Add both values as GitHub repository secrets.

Required secrets:

- CLOUDFLARE_ACCOUNT_ID
- CLOUDFLARE_API_TOKEN

Never put API tokens in source files.

## Generate a documentary

1. Open the Actions tab.
2. Select Make Hand-Drawn Documentary.
3. Click Run workflow.
4. Choose a narration file.
5. Optionally provide narration audio.
6. Start the workflow.

## Narration format

Create a text file inside scripts/.

Separate scenes with blank lines.

Every paragraph becomes one scene and receives its own
visual prompt and generated illustration.

## Output

The workflow creates:

output/documentary.mp4

generated_art/scene_001.png
generated_art/scene_001_prompt.txt
generated_art/scene_002.png
generated_art/scene_002_prompt.txt

Download the results from the Actions artifacts.

## Historical and religious care

The prompt system prohibits depicting Prophet Muhammad
in any form, including a face, body, silhouette or shadow.

It also prohibits depicting other prophets.

Uncertain historical details should not be presented
as established facts.

## Current limitations

- Prompt composition is local and rule-based, not LLM-powered.
- The first version uses an irregular reveal mask rather than
  actual individual pen-stroke animation.
- Camera movement uses a slow push.
- Scene duration is currently fixed.
- The image model's visual quality and composition need testing.
- Free inference availability and limits can change.

## Tests

Run:

pytest -q
