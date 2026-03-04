import subprocess
import sys
import os
import argparse


def burn_subtitles(video_path, srt_path, output_path, delta_y=0):
    """烧录字幕到视频"""
    srt_escaped = srt_path.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")

    style = f"Fontname=AlibabaPuHuiTi-H,FontSize=10,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H800A0A0A,BackColour=&H00000000,BorderStyle=1,Outline=1,Shadow=1,Spacing=0,MarginV={delta_y}"

    ffmpeg_command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles='{srt_escaped}':force_style='{style}'",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-strict", "experimental",
        "-y",
        output_path
    ]

    print(f"输入视频: {video_path}")
    print(f"字幕文件: {srt_path}")
    print(f"输出视频: {output_path}")

    subprocess.run(ffmpeg_command, check=True)
    print(f"视频已保存: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video_path", help="Input video file")
    parser.add_argument("srt_path", nargs="?", help="Subtitle file (default: video base name.srt)")
    parser.add_argument("output_path", nargs="?", help="Output video file (default: video base name_subtitled.mp4)")
    parser.add_argument("--deltaY", type=int, default=0, help="Vertical offset for subtitle position")
    args = parser.parse_args()

    video_path = args.video_path

    if args.srt_path:
        srt_path = args.srt_path
    else:
        base, _ = os.path.splitext(video_path)
        srt_path = base + ".srt"

    if args.output_path:
        output_path = args.output_path
    else:
        base, _ = os.path.splitext(video_path)
        output_path = base + "_subtitled.mp4"

    burn_subtitles(video_path, srt_path, output_path, args.deltaY)
