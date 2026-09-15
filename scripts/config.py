"""PureTune runtime configuration.

Paths come from environment variables with safe fallbacks. Keep personal or
machine-specific paths in the environment, not in source files.
"""

import os
import shutil
from pathlib import Path


def _env(name: str, default: str = "") -> str:
    value = os.environ.get(name, default).strip()
    return value


FFMPEG = _env("PURETUNE_FFMPEG", shutil.which("ffmpeg") or "ffmpeg")
FFPROBE = _env("PURETUNE_FFPROBE", shutil.which("ffprobe") or "ffprobe")

CDP_URL = _env("PURETUNE_CDP_URL", "http://127.0.0.1:9222")

OUTPUT_ROOT = Path(_env("PURETUNE_OUTPUT_ROOT", str(Path.cwd()))).resolve()

JIANYING_DRAFT_LIB = _env(
    "PURETUNE_JIANYING_DRAFT_LIB",
    str(Path.cwd() / "jianying_drafts"),
)

RECORD_SAMPLE_RATE = int(_env("PURETUNE_RECORD_SAMPLE_RATE", "44100"))
RECORD_MP3_BITRATE = _env("PURETUNE_RECORD_MP3_BITRATE", "320k")
