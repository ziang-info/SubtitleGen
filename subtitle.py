import whisper
import os
from datetime import datetime as t
import torch
from deep_translator import GoogleTranslator
import subprocess

def extract_audio(video_path, audio_path):
    """从视频中提取音频"""
    try:
        subprocess.run([
            "ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le", 
            "-ar", "16000", "-ac", "1", audio_path, "-y"
        ], check=True, capture_output=True)
    except Exception as e:
        print(f"音频提取错误: {str(e)}")
        raise

def format_srt_time(seconds):
    """Format seconds to SRT time format HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def generate_srt(segments, output_srt):
    """生成SRT格式字幕文件，同时生成中英文双语字幕"""
    translator = None
    try:
        translator = GoogleTranslator(source='en', target='zh-CN')
    except Exception:
        print("Translation service unavailable, using English only")

    with open(output_srt, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(segments, start=1):
            start = format_srt_time(segment['start'])
            end = format_srt_time(segment['end'])

            english_text = segment['text'].strip()

            if translator:
                try:
                    simplified_text = translator.translate(english_text)
                except Exception:
                    simplified_text = english_text
            else:
                simplified_text = english_text

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{english_text}\n")
            f.write(f"{simplified_text}\n\n")

def transcribe_audio(audio_path, device="cpu"):
    """使用Whisper转录音频"""
    print("加载Whisper模型...")
    model = whisper.load_model("tiny", device=device)  # 使用更高精度的模型，"tiny" 可能精度不够
    print("开始转录...")
    result = model.transcribe(audio_path, verbose=False, language='en')  # 假设视频为英文
    return result["segments"]

def main(video_path, output_video_path, output_srt):
    """主函数"""
    try:
        # 检查CUDA是否可用
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"使用设备: {device}")

        # 设置音频文件路径
        audio_path = "temp_audio.wav"  # 提取的音频文件

        # 提取音频
        print("提取音频中...")
        extract_audio(video_path, audio_path)

        # 使用Whisper转录音频
        print("开始转录音频...")
        segments = transcribe_audio(audio_path, device)

        # 生成SRT字幕文件
        print("生成字幕文件...")
        generate_srt(segments, output_srt)

        print(f"字幕已生成: {output_srt}")

        # 使用ffmpeg烧录字幕到视频中
        print("生成带字幕的视频...")
        # 构造ffmpeg命令
        srt_path = output_srt.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
        ffmpeg_command = [
            "ffmpeg",
            "-i", video_path,
            "-vf", f"subtitles='{srt_path}'",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-strict", "experimental",
            "-y",
            output_video_path
        ]
        
        # 执行ffmpeg命令
        subprocess.run(ffmpeg_command, check=True)
        
        print(f"视频已保存: {output_video_path}")

        # 可选：删除提取的音频文件
        os.remove(audio_path)

    except Exception as e:
        print(f"处理过程中出错: {str(e)}")
        raise


import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python subtitle.py <video_path>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    base, _ = os.path.splitext(video_path)
    output_video_path = base + "_subtitled.mp4"
    output_srt = base + ".srt"
    
    main(video_path, output_video_path, output_srt)
