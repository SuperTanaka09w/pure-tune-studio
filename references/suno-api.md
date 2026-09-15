# Suno Browser and API Notes

## Browser automation

- Use an automated Edge/Chromium instance with a remote debugging port.
- Use a dedicated user-data directory so the login session is isolated and reusable.
- The debugging WebSocket may require `--remote-allow-origins=http://127.0.0.1:<port>`.
- Use `--autoplay-policy=no-user-gesture-required` so playback can start automatically.

## Variety slider

Before generating:

1. Expand **More Options**.
2. Find the **Variety** slider.
3. Set it to **off** by dragging the slider to the far left.

## Song list

The page requests `https://studio-api-prod.suno.com/api/feed/v3`. A valid `Authorization: Bearer ...` token can be captured from browser network requests. The feed response includes:

- `id`
- `title`
- `created_at`
- `metadata.duration`
- `metadata.tags`
- `media_urls`

Do not hardcode personal API tokens or session cookies into the skill.

## Rename on Suno

Use `POST /api/gen/{clip_id}/set_metadata/` with the title and existing lyrics to rename a song. Free/preview tracks may return 403 for some operations.
