# Reference-Track Folder Layout

Every reference track gets its own folder. All prompts and songs derived from that reference track stay inside that folder.

```text
<reference-track-name>/
├── 源文件/                    # Original reference mp3/wav
├── 分析/                      # Analysis JSON/MD
├── 提示词/                    # Prompt versions
│   ├── 保守版.md
│   ├── 推荐版.md
│   └── 实验版.md
├── 生成歌曲/                  # Songs generated from those prompts
│   ├── <theme-A>/
│   ├── <theme-B>/
│   └── 弦乐版/
├── 剪映草稿/                  # JianYing drafts
└── 发布文案/                  # Titles, copy, tags
```

Rules:

- A prompt derived from the reference track belongs under that reference track's `提示词/`.
- Any songs generated from that prompt and its alternate versions belong under the same reference track's `生成歌曲/`.
- Songs may be grouped by theme or type inside `生成歌曲/`, but they must not move to another reference track's folder.
- The JianYing draft and publish copy for those songs also stay under the same reference track.
