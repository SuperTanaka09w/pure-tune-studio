"""Rename songs locally and on Suno with a numeric prefix."""

import argparse
import json
import os
import re
import sys
import time

import requests

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def safe_name(name):
    return re.sub(r'[\\/:*?"<>|\r\n\t]', "_", name).strip()


def local_rename(manifest, names, outdir, string_outdir=None):
    os.makedirs(outdir, exist_ok=True)
    if string_outdir:
        os.makedirs(string_outdir, exist_ok=True)
    for item in manifest:
        index = int(item["index"])
        zh, en = names[str(index)]
        folder = string_outdir if (item.get("is_string") and string_outdir) else outdir
        old_name = safe_name(f"{index:02d}_{item.get('title','song')}_{item['id'][:8]}.mp3")
        new_name = safe_name(f"{index:02d}_{zh} {en}.mp3")
        old_path = os.path.join(folder, old_name)
        new_path = os.path.join(folder, new_name)
        if os.path.exists(old_path) and old_path != new_path:
            os.rename(old_path, new_path)
        print(f"{new_name}")


def suno_rename(manifest, names, token):
    base = "https://studio-api-prod.suno.com"
    headers = {"Authorization": token, "Content-Type": "application/json"}
    for item in manifest:
        index = int(item["index"])
        zh, en = names[str(index)]
        title = f"{index:02d} {zh} {en}"
        lyrics = ""
        try:
            feed = requests.post(
                f"{base}/api/feed/v3",
                headers=headers,
                json={"filters": {"ids": {"presence": "True", "clipIds": [item["id"]]}}, "limit": 1},
                timeout=30,
            ).json()
            clips = feed.get("clips") or []
            if clips:
                lyrics = clips[0].get("metadata", {}).get("lyrics") or ""
        except Exception:
            pass
        body = {
            "title": title,
            "lyrics": lyrics,
            "caption": "",
            "caption_mentions": {"user_mentions": []},
            "remove_image_cover": False,
            "remove_video_cover": False,
        }
        response = requests.post(
            f"{base}/api/gen/{item['id']}/set_metadata/",
            headers=headers,
            json=body,
            timeout=30,
        )
        print(f"{response.status_code} {title}")
        time.sleep(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--names", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--string-outdir", default=None)
    parser.add_argument("--token", default=os.environ.get("PURETUNE_SUNO_TOKEN", ""))
    parser.add_argument("--local-only", action="store_true")
    parser.add_argument("--suno-only", action="store_true")
    args = parser.parse_args()

    manifest = json.load(open(args.manifest, encoding="utf-8"))
    names = json.load(open(args.names, encoding="utf-8"))

    if not args.suno_only:
        local_rename(manifest, names, args.outdir, args.string_outdir)
    if not args.local_only and args.token:
        suno_rename(manifest, names, args.token)


if __name__ == "__main__":
    main()
