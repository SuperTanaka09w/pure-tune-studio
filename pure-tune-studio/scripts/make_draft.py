"""Generate a JianYing draft from a song list and shared template parameters."""

import argparse
import json
import sys
from pathlib import Path

from config import JIANYING_DRAFT_LIB


def parse_color(color, default=(1.0, 1.0, 1.0)):
    if isinstance(color, (list, tuple)):
        return tuple(float(x) for x in color[:3])
    text = str(color).strip().lstrip("#")
    if len(text) != 6:
        return default
    return tuple(int(text[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def layout(params, count):
    indicator = params["指示器"]
    song_list = params["歌单"]
    step0 = float(indicator["行距步长"])
    first_y = float(indicator["首行y"])
    allowed = float(indicator["允许带宽"])
    scale0 = float(song_list["位置"]["缩放"])
    center_offset = float(song_list.get("中心偏移", 0.0))
    need = abs(step0) * (count - 1)
    if need <= allowed + 1e-4 or count <= 1:
        step, scale = step0, scale0
    else:
        step = -allowed / (count - 1)
        scale = scale0 * (abs(step) / abs(step0))
    ys = [first_y + i * step for i in range(count)]
    center_y = first_y + (count - 1) * step / 2 + center_offset
    return {
        "step": step,
        "scale": scale,
        "ys": ys,
        "center_y": center_y,
        "x": float(song_list["位置"]["x"]),
        "indicator_x": float(indicator["x"]),
    }


def build_draft(songs, background, draft_name, params):
    try:
        from pyJianYingDraft import (
            AudioMaterial, AudioSegment, ClipSettings, DraftFolder,
            TextBorder, TextSegment, TextStyle, TrackSpec, TrackType,
            VideoMaterial, VideoSegment, trange,
        )
    except ImportError as exc:
        raise SystemExit("请先安装 pyJianYingDraft: pip install pyJianYingDraft") from exc

    canvas = params["画布"]
    total = int(sum(float(s["duration"]) for s in songs) * 1_000_000)
    folder = DraftFolder(str(JIANYING_DRAFT_LIB))
    draft = folder.create_draft(draft_name, canvas["宽"], canvas["高"], canvas["fps"], allow_replace=True)

    draft.add_material(VideoMaterial(str(background), "背景图"))
    for song in songs:
        draft.add_material(AudioMaterial(str(song["path"]), song["display_name"]))

    video_track = draft.append_track(TrackSpec(TrackType.video, name="视频-背景"))
    draft.add_segment(VideoSegment(str(background), trange(0, total)), video_track)

    audio_track = draft.append_track(TrackSpec(TrackType.audio, name="音频"))
    cursor = 0
    for song in songs:
        duration = int(float(song["duration"]) * 1_000_000)
        draft.add_segment(AudioSegment(str(song["path"]), trange(cursor, duration)), audio_track)
        cursor += duration

    song_list = params["歌单"]
    indicator = params["指示器"]
    lay = layout(params, len(songs))

    text_track = draft.append_track(TrackSpec(TrackType.text, name="文字-歌单"))
    text_segment = TextSegment(
        "\n".join(s["display_name"] for s in songs),
        trange(0, total),
        style=TextStyle(
            size=float(song_list["字号"]),
            bold=False,
            color=parse_color(song_list["字色"]),
            align=int(song_list["对齐"]),
            line_spacing=int(round(song_list["行距_参数"])),
        ),
        border=TextBorder(
            alpha=float(song_list["描边"]["不透明度"]),
            color=parse_color(song_list["描边"]["颜色"]),
            width=float(song_list["描边"]["宽度_UI"]),
        ),
        clip_settings=ClipSettings(
            transform_x=lay["x"],
            transform_y=lay["center_y"],
            scale_x=lay["scale"],
            scale_y=lay["scale"],
        ),
    )
    draft.add_segment(text_segment, text_track)

    indicator_track = draft.append_track(TrackSpec(TrackType.text, name="文字-指示器"))
    cursor = 0
    for i, song in enumerate(songs):
        duration = int(float(song["duration"]) * 1_000_000)
        segment = TextSegment(
            indicator["文本"],
            trange(cursor, duration),
            style=TextStyle(size=float(indicator["字号"]), bold=True, color=parse_color(indicator["字色"]), align=0),
            clip_settings=ClipSettings(transform_x=lay["indicator_x"], transform_y=lay["ys"][i]),
        )
        draft.add_segment(segment, indicator_track)
        cursor += duration

    draft.save()
    return Path(JIANYING_DRAFT_LIB) / draft_name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--songs", required=True, help="JSON list with path, display_name, duration")
    parser.add_argument("--background", required=True)
    parser.add_argument("--draft-name", required=True)
    parser.add_argument("--template-params", default=str(Path(__file__).resolve().parent.parent / "assets" / "template_params.json"))
    args = parser.parse_args()

    songs = json.load(open(args.songs, encoding="utf-8"))
    params = json.load(open(args.template_params, encoding="utf-8"))
    draft_dir = build_draft(songs, args.background, args.draft_name, params)
    print(f"草稿已生成：{draft_dir}")


if __name__ == "__main__":
    main()
