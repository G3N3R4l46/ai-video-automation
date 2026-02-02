import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "assets"
AUDIO_DIR = BASE_DIR / "output" / "audio"
SUB_DIR = BASE_DIR / "output" / "subtitles"
VIDEO_DIR = BASE_DIR / "output" / "videos"

VIDEO_DIR.mkdir(parents=True, exist_ok=True)

def make_video(background_video: str, audio_file: str, subtitle_file: str, output_name: str):
    bg_path = ASSETS_DIR / background_video
    audio_path = AUDIO_DIR / audio_file
    sub_path = SUB_DIR / subtitle_file
    out_path = VIDEO_DIR / output_name

    if not bg_path.exists():
        raise FileNotFoundError("Background video yok.")
    if not audio_path.exists():
        raise FileNotFoundError("Audio dosyası yok.")
    if not sub_path.exists():
        raise FileNotFoundError("Subtitle dosyası yok.")

    command = [
        "ffmpeg",
        "-y",
        "-i", str(bg_path),
        "-i", str(audio_path),
        "-vf", f"subtitles={sub_path}",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        str(out_path)
    ]

    subprocess.run(command, check=True)
    return out_path

if __name__ == "__main__":
    # demo
    print("Video oluşturuluyor...")
