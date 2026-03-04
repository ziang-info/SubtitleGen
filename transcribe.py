import whisper
import os
import torch
import requests
from opencc import OpenCC
import subprocess
import sys


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


def generate_srt(segments, output_srt, source_language=None):
    """生成SRT格式字幕文件"""
    src = source_language if source_language else 'auto'
    print(f"Translating from: {src}")
    cc = OpenCC('t2s')

    with open(output_srt, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(segments, start=1):
            start = format_srt_time(segment['start'])
            end = format_srt_time(segment['end'])

            original_text = segment['text'].strip()
            translated_text = original_text

            try:
                if src.startswith('zh'):
                    r = requests.get(f'https://api.mymemory.translated.net/get?q={requests.utils.quote(original_text)}&langpair=zh-CN|en')
                    result = r.json()
                    translated_text = result.get('responseData', {}).get('translatedText', original_text)
                    chinese_text = cc.convert(original_text)
                    english_text = translated_text
                else:
                    r = requests.get(f'https://api.mymemory.translated.net/get?q={requests.utils.quote(original_text)}&langpair=en|zh-CN|')
                    result = r.json()
                    translated_text = result.get('responseData', {}).get('translatedText', original_text)
                    chinese_text = translated_text
                    english_text = original_text
                print(f"Translated: {original_text} -> {translated_text}")
            except Exception as e:
                print(f"Translation error: {e}")
                if src.startswith('zh'):
                    chinese_text = cc.convert(original_text)
                    english_text = original_text
                else:
                    chinese_text = original_text
                    english_text = original_text

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{chinese_text}\n")
            f.write(f"{english_text}\n\n")


def transcribe_audio(audio_path, device="cpu", language=None):
    """使用Whisper转录音频"""
    print("加载Whisper模型...")
    model = whisper.load_model("tiny", device=device)
    print("开始转录...")
    result = model.transcribe(audio_path, verbose=False, language=language)
    detected_lang = result.get("language", "en")
    print(f"Detected language: {detected_lang}")
    return result["segments"], detected_lang


def main(video_path, output_srt, language=None):
    """主函数"""
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"使用设备: {device}")

        audio_path = "temp_audio.wav"

        print("提取音频中...")
        extract_audio(video_path, audio_path)

        print("开始转录音频...")
        segments, detected_lang = transcribe_audio(audio_path, device, language)

        print("生成字幕文件...")
        generate_srt(segments, output_srt, detected_lang)

        print(f"字幕已生成: {output_srt}")

        os.remove(audio_path)

    except Exception as e:
        print(f"处理过程中出错: {str(e)}")
        raise


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <video_path> [output_srt] [language]")
        sys.exit(1)

    video_path = sys.argv[1]
    if len(sys.argv) >= 3:
        output_srt = sys.argv[2]
    else:
        base, _ = os.path.splitext(video_path)
        output_srt = base + ".srt"
    
    language = sys.argv[3] if len(sys.argv) >= 4 else None

    main(video_path, output_srt, language)
