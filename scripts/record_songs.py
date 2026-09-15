"""Record Suno songs through system loopback.

Expects a manifest JSON with objects containing id, title, duration, is_string.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time

import numpy as np
import soundcard as sc
import soundfile as sf

import cdp
from config import FFMPEG, RECORD_MP3_BITRATE, RECORD_SAMPLE_RATE


def safe_name(name):
    return re.sub(r'[\\/:*?"<>|\r\n\t]', "_", name).strip()


def loopback_mic():
    speaker = sc.default_speaker()
    for mic in sc.all_microphones(include_loopback=True):
        if mic.name == speaker.name:
            return mic
    return None


def click_play(tab):
    info = tab.eval_js(
        "JSON.stringify((() => {"
        "const b=[...document.querySelectorAll('button')].find(x=>{"
        "const r=x.getBoundingClientRect(); return r.width>0 && r.height>0 && "
        "x.getAttribute('aria-label')==='Play';});"
        "if(!b)return null;"
        "const r=b.getBoundingClientRect();"
        "return {x:Math.round(r.x+r.width/2), y:Math.round(r.y+r.height/2)};"
        "})())"
    )
    point = json.loads(info or "null")
    if not point:
        return False
    tab.cmd("Input.dispatchMouseEvent", {"type": "mousePressed", "x": point["x"], "y": point["y"], "button": "left", "clickCount": 1})
    tab.cmd("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": point["x"], "y": point["y"], "button": "left", "clickCount": 1})
    return True


def record_one(tab, item, outfile):
    duration = float(item.get("duration") or 180)
    song_id = item["id"]
    tab.navigate(f"https://suno.com/song/{song_id}")
    time.sleep(7)
    if not click_play(tab):
        return False, 0.0, duration, "no_play_button"
    mic = loopback_mic()
    if mic is None:
        return False, 0.0, duration, "no_loopback"
    tab.navigate(f"https://suno.com/song/{song_id}")
    time.sleep(7)
    if not click_play(tab):
        return False, 0.0, duration, "no_play_button_retry"
    frames = int(RECORD_SAMPLE_RATE * int(duration))
    with mic.recorder(samplerate=RECORD_SAMPLE_RATE) as recorder:
        click_play(tab)
        data = recorder.record(numframes=frames)
    peak = float(np.max(np.abs(data[:, 0]))) if len(data) else 0.0
    if peak < 0.02:
        return False, peak, duration, "too_quiet"
    wav_tmp = os.path.join(tempfile.gettempdir(), f"puretune_{song_id[:8]}.wav")
    sf.write(wav_tmp, data[:, 0], RECORD_SAMPLE_RATE)
    subprocess.run([FFMPEG, "-y", "-i", wav_tmp, "-b:a", RECORD_MP3_BITRATE, outfile], check=True, capture_output=True)
    os.remove(wav_tmp)
    return True, peak, duration, ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--string-outdir", default=None)
    args = parser.parse_args()

    manifest = json.load(open(args.manifest, encoding="utf-8"))
    os.makedirs(args.outdir, exist_ok=True)
    if args.string_outdir:
        os.makedirs(args.string_outdir, exist_ok=True)

    tab = cdp.get_tab()
    try:
        for item in manifest:
            outdir = args.string_outdir if (item.get("is_string") and args.string_outdir) else args.outdir
            fname = safe_name(f"{int(item.get('index', 0)):02d}_{item.get('title','song')}_{item['id'][:8]}.mp3")
            outfile = os.path.join(outdir, fname)
            for attempt in range(2):
                ok, peak, duration, error = record_one(tab, item, outfile)
                if ok:
                    break
                time.sleep(4)
            print(f"{'OK' if ok else 'FAIL'} {fname} peak={peak:.2f} {error}", flush=True)
            time.sleep(2)
    finally:
        tab.close()


if __name__ == "__main__":
    main()
