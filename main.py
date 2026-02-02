from utils.video_maker import make_video
from utils.subtitles import generate_srt
from utils.tts import text_to_speech
from utils.text_generator import generate_history_content
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"

TEXT_DIR = OUTPUT_DIR / "texts"
AUDIO_DIR = OUTPUT_DIR / "audio"
SUB_DIR = OUTPUT_DIR / "subtitles"
VIDEO_DIR = OUTPUT_DIR / "videos"

for d in [TEXT_DIR, AUDIO_DIR, SUB_DIR, VIDEO_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def parse_sections(text: str):
    sections = {"ANLATIM": "", "AÇIKLAMA": "", "HASHTAG": ""}
    current = None

    for line in text.splitlines():
        line = line.strip()
        if line == "===ANLATIM===":
            current = "ANLATIM"
        elif line == "===AÇIKLAMA===":
            current = "AÇIKLAMA"
        elif line == "===HASHTAG===":
            current = "HASHTAG"
        elif current:
            sections[current] += line + "\n"

    return {k: v.strip() for k, v in sections.items()}


def save_output(sections: dict):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    anlatim_path = TEXT_DIR / f"anlatim_{ts}.txt"
    aciklama_path = TEXT_DIR / f"aciklama_{ts}.txt"
    hashtag_path = TEXT_DIR / f"hashtag_{ts}.txt"

    anlatim_path.write_text(sections["ANLATIM"], encoding="utf-8")
    aciklama_path.write_text(sections["AÇIKLAMA"], encoding="utf-8")
    hashtag_path.write_text(sections["HASHTAG"], encoding="utf-8")

    print("✔ Metinler kaydedildi")

    audio_file = AUDIO_DIR / f"anlatim_{ts}.mp3"
    text_to_speech(sections["ANLATIM"], audio_file)
    print("🎙️ Ses oluşturuldu")

    subtitle_file = SUB_DIR / f"anlatim_{ts}.srt"
    generate_srt(sections["ANLATIM"], subtitle_file, total_duration=40.0)
    print("📝 Altyazı oluşturuldu")

    video_file = VIDEO_DIR / f"video_{ts}.mp4"
    make_video(
        background_video=BASE_DIR / "assets" / "background.mp4",
        audio_file=audio_file,
        subtitle_file=subtitle_file,
        output_name=video_file
    )

    print("🎬 Video oluşturuldu:", video_file)


def main():
    print("📜 Tarih içeriği üretiliyor...")
    raw_output = generate_history_content()
    sections = parse_sections(raw_output)

    if not all(sections.values()):
        raise ValueError("Prompt çıktısı eksik!")

    save_output(sections)


if __name__ == "__main__":
    main()
