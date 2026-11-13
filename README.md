# Hand-Drawn Documentary

A cinematic documentary and Reels generator built with Python,
Gemini and Pollinations.

Each narration scene receives its own AI-generated illustration.
The project aims for a hand-drawn historical documentary aesthetic,
not a fixed collection of icons or flat vector graphics.

## Visual direction

- Uneven organic ink outlines
- Variable line weight and sketch marks
- Pencil texture and cross-hatching
- Soft ink-wash and watercolor shading
- Detailed historical environments and fabric folds
- Warm cream parchment and restrained gold accents
- Unique composition for each narration scene
- Slow camera push and gradual irregular reveal

## Image providers

Gemini writes scene-specific image prompts and is the first
image-generation provider.

Pollinations is the fallback image-generation provider.

Both providers are configured through GitHub Actions secrets.

## Repository setup

Create these repository secrets:

- GEMINI_API_KEY
- POLLINATIONS_API_KEY

No .env file is required.

## Add narration

Create a text file in scripts/.

Separate scenes with a blank line. Each paragraph becomes
a separate scene and receives its own visual prompt and illustration.

## Generate a video

1. Open the repository's Actions tab.
2. Select Make Documentary Video.
3. Select Run workflow.
4. Choose the narration script path.
5. Optionally provide an audio path.
6. Start the workflow.

## Output artifacts

The workflow uploads:

- handdrawn-documentary-video
- generated-scene-artwork

Download them from the completed workflow run.

## Historical and religious care

The prompt system prohibits depicting Prophet Muhammad in any form,
including silhouettes and shadows. It also prohibits depicting
other prophets.

Uncertain historical details should not be presented as established fact.

## Current limitations

- The first version uses a gradual irregular reveal mask, not true
  individual pen-stroke animation.
- Camera movement is a slow Ken Burns-style push and drift.
- Scene duration is currently configured as a fixed number of seconds.
- Narration audio is supplied by the user.
- API usage and image generation may incur provider charges.

## Tests

The GitHub Actions workflow runs:

    pytest -q
