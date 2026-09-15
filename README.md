# PureTune / 纯音工坊

从一首参考曲，自动生成原创纯音乐，并做成剪映草稿和发布文案。

## 这个工具能做什么

- 完整分析你提供的参考曲
- 根据分析结果写三版 Suno 提示词：保守版、推荐版、实验版
- 用自动化 Edge 在 Suno 批量生成歌曲
- 免费版无法下载时，通过系统回环录音获取歌曲
- 分析新曲、生成中英文名字
- 本地文件和 Suno 标题同步改名并加序号
- 按参考曲整理文件夹
- 生成剪映草稿
- 生成三平台标题、正文和标签

## 安装

```bash
python scripts/install.py
```

这个脚本会安装 Python 依赖，并检查 `ffmpeg` / `ffprobe`。

可能需要配置的环境变量：

- `PURETUNE_FFMPEG`
- `PURETUNE_FFPROBE`
- `PURETUNE_CDP_URL`
- `PURETUNE_OUTPUT_ROOT`
- `PURETUNE_JIANYING_DRAFT_LIB`
- `PURETUNE_SUNO_TOKEN`

## 使用流程

1. 告诉 AI 你的参考曲文件。
2. 选择背景图来源：用户提供，或自动生成 1920×1080。
3. 选择文案生成方式：AI 生成，或按你的模板仿写。
4. AI 会完成分析、写提示词、Suno 生成、录音、起名、改名、整理、剪映草稿和文案。
5. 你只需要在剪映里导出，再上传到平台。

## 目录结构

```text
pure-tune-studio/
├── SKILL.md
├── README.md
├── requirements.txt
├── agents/
├── scripts/
├── references/
└── assets/
```

## 注意

- 分析参考曲可能需要较长时间，请耐心等待。
- Suno 生成前会把 More Options 里的 Variety 滑条设为 off。
- 剪映步骤目前主要在 Windows 环境测试。

如果你觉得这个项目有用，欢迎点个 Star ⭐。
