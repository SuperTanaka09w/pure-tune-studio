"""Generate generic platform titles, copy, and tags from a song list."""

import argparse
import json
from pathlib import Path


def timestamp(seconds):
    return f"{int(seconds // 60):02d}:{int(seconds % 60):02d}"


def build_tracklist(songs):
    lines = []
    total = 0
    for song in songs:
        lines.append(f"{timestamp(total)} {song['display_name']}")
        total += float(song.get("duration") or 0)
    return lines, total


def build_copy(songs, name, instrument, mood, use_case):
    tracklist, total_seconds = build_tracklist(songs)
    minutes = int(total_seconds // 60)
    tag_map = {
        "bilibili": ["纯音乐", "钢琴曲", "古典钢琴", "学习歌单", "治愈系音乐", "背景音乐"],
        "douyin": ["纯音乐", "钢琴曲", "古典练习曲", "学习歌单", "治愈系", "背景音乐"],
        "xiaohongshu": ["纯音乐", "钢琴曲", "钢琴独奏", "古典钢琴", "歌单分享", "学习音乐"],
    }
    details = "\n".join([
        f"这是《{name}》主题的{instrument}纯音乐合集。",
        f"{mood}，适合{use_case}。",
        "",
        "🎵 曲目列表",
        *tracklist,
    ])
    titles = {
        "bilibili": f"{name}｜{instrument}·{len(songs)}首纯音乐合集（{minutes}分钟）",
        "douyin": f"{len(songs)}首{instrument}纯音乐｜{name}（{minutes}分钟）",
        "xiaohongshu": f"{name}｜{len(songs)}首{instrument}纯音乐合集",
    }
    return {
        "title_candidates": list(titles.values()),
        "platform": {
            p: {"标题": titles[p], "正文": details, "标签": tag_map[p]}
            for p in titles
        },
        "tags": tag_map,
        "tracklist": tracklist,
        "total_minutes": minutes,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--songs", required=True, help="JSON list with display_name and duration")
    parser.add_argument("--name", default="纯音乐")
    parser.add_argument("--instrument", default="钢琴独奏")
    parser.add_argument("--mood", default="优雅、舒缓、有呼吸感")
    parser.add_argument("--use-case", default="学习、办公、阅读、开车、发呆")
    parser.add_argument("--output", default="copy.json")
    args = parser.parse_args()

    songs = json.load(open(args.songs, encoding="utf-8"))
    result = build_copy(songs, args.name, args.instrument, args.mood, args.use_case)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
