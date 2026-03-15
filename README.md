# Video Subtlte Generationor
# 视频子母生成器

* 为视频自动生成子母，直接支持中英双语。


## 安装依赖

```bash
pip install -r requirements.txt
```

## Python Scripts Usage

### 1. transcribe.py
转录音频并生成双语字幕文件（SRT格式）。

```bash
python transcribe.py <video_path> [output_srt] [language]
```

- `video_path`: 输入视频文件路径
- `output_srt`: 输出的字幕文件路径（可选，默认与视频同名的.srt文件）
- `language`: 语言代码，如 `zh`、`en`、`auto`（可选，默认自动检测）

### 2. subtitle.py
转录音频生成字幕，并直接将字幕烧录到视频中。

```bash
python subtitle.py <video_path>
```

- `video_path`: 输入视频文件路径
- 自动生成同名的 `.srt` 字幕文件和 `_subtitled.mp4` 视频文件

### 3. burn_subtitles.py
将现有的SRT字幕文件烧录到视频中。

```bash
python burn_subtitles.py <video_path> [srt_path] [output_path] [--deltaY N]
```

- `video_path`: 输入视频文件路径
- `srt_path`: 字幕文件路径（可选，默认与视频同名的.srt文件）
- `output_path`: 输出视频路径（可选，默认 `视频名_subtitled.mp4`）
- `--deltaY N`: 字幕垂直位置偏移量

## requirements.txt

### opencode
    write a requirements file, record all the requirement modules. if run this script in a new env, we can install requirements with pip.

## FONTS

SimHei
思源黑体 Noto Sans 
Roboto
Open Sans

"subtitles='{srt_escaped}':force_style='

Fontname=Roboto,FontSize=11,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BackColour=&H808080,BorderStyle=3,Outline=1,Shadow=1
Fontname=Roboto,FontSize=11,PrimaryColour=&H00FFFFFF,OutlineColour=&H40202020,BackColour=&H00000000,BorderStyle=1,Outline=1,Shadow=0
Fontname=Roboto,FontSize=11,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H40202020,BackColour=&H00000000,BorderStyle=1,Outline=1,Shadow=0

换用这个字体：阿里巴巴普惠体 H

Fontname=阿里巴巴普惠体 H,FontSize=11,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H40202020,BackColour=&H00000000,BorderStyle=1,Outline=1,Shadow=0

去掉描边，添加阴影。
