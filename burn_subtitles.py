import subprocess
import sys
import os


def burn_subtitles(video_path, srt_path, output_path):
    """烧录字幕到视频"""
    srt_escaped = srt_path.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")

    ffmpeg_command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles='{srt_escaped}'",
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
    if len(sys.argv) < 2:
        print("Usage: python burn_subtitles.py <video_path> [srt_path] [output_path]")
        sys.exit(1)

    video_path = sys.argv[1]

    if len(sys.argv) >= 3:
        srt_path = sys.argv[2]
    else:
        base, _ = os.path.splitext(video_path)
        srt_path = base + ".srt"

    if len(sys.argv) >= 4:
        output_path = sys.argv[3]
    else:
        base, _ = os.path.splitext(video_path)
        output_path = base + "_subtitled.mp4"

    burn_subtitles(video_path, srt_path, output_path)
