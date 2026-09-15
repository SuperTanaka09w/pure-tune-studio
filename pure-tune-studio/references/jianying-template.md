# JianYing Draft Template

The draft generator must reuse the shared layout template, including:

- Canvas: 1920x1080 at 30 fps
- Song-list text color: light cyan `#C0F1F5`
- Song-list border color: blue `#469DF3`, width `0.08`
- Current-track indicator text: white `#FFFFFF`
- All text shadow: none
- Line spacing, forced line width, font path, and per-line indicator coordinates must match the template.

When the song count exceeds the template's original line count, tighten line spacing and scale proportionally so the last line stays inside the canvas.

Use the recorded real durations as timeline durations. The track-list timestamps for publish copy must be read from the final JianYing draft, not recalculated separately.
