"""Install Python dependencies and check external tools for PureTune."""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd):
    print("+", " ".join(str(x) for x in cmd))
    return subprocess.run(cmd).returncode


def main():
    root = Path(__file__).resolve().parent.parent
    requirements = root / "requirements.txt"

    print("安装 Python 依赖...")
    code = run([sys.executable, "-m", "pip", "install", "-r", str(requirements)])
    if code != 0:
        print("依赖安装失败，请检查网络或手动安装 requirements.txt")
        return 1

    print("\n检查外部工具...")
    ffmpeg = shutil.which("ffmpeg") or os.environ.get("PURETUNE_FFMPEG")
    ffprobe = shutil.which("ffprobe") or os.environ.get("PURETUNE_FFPROBE")
    if ffmpeg:
        print(f"[OK] ffmpeg: {ffmpeg}")
    else:
        print("[!] 未找到 ffmpeg，请安装后设置环境变量 PURETUNE_FFMPEG")
    if ffprobe:
        print(f"[OK] ffprobe: {ffprobe}")
    else:
        print("[!] 未找到 ffprobe，请安装后设置环境变量 PURETUNE_FFPROBE")

    print("\n可选配置环境变量：")
    print("  PURETUNE_FFMPEG          ffmpeg 路径")
    print("  PURETUNE_FFPROBE         ffprobe 路径")
    print("  PURETUNE_CDP_URL         Chrome 调试地址，默认 http://127.0.0.1:9222")
    print("  PURETUNE_OUTPUT_ROOT     输出根目录，默认当前目录")
    print("  PURETUNE_JIANYING_DRAFT_LIB  剪映草稿库，默认 ./jianying_drafts")
    print("  PURETUNE_SUNO_TOKEN      Suno Bearer 令牌（改名时用）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
