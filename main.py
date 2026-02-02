from utils.tts import text_to_speech


from pathlib import Path
from utils.text_generator import generate_history_content
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
TEXT_DIR = OUTPUT_DIR / "texts"

TEXT_DIR.mkdir(parents=True, exist_ok=True)

def parse_sections(text: str):
    sections = {
        "ANLATIM": "",
        "AÇIKLAMA": "",
        "HASHTAG": ""
    }

    current = None
    for line in text.splitlines():
        line = line.strip()
        if line == "===ANLATIM===":
            current = "ANLATIM"
            continue
        if line == "===AÇIKLAMA===":
            current = "AÇIKLAMA"
            continue
        if line == "===HASHTAG===":
            current = "HASHTAG"
            continue

        if current:
            sections[current] += line + "\n"

    # trim
    for k in sections:
        sections[k] = sections[k].strip()

    return sections

def save_output(sections: dict):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    anlatim_path = TEXT_DIR / f"anlatim_{ts}.txt"
    aciklama_path = TEXT_DIR / f"aciklama_{ts}.txt"
    hashtag_path = TEXT_DIR / f"hashtag_{ts}.txt"

    anlatim_path.write_text(sections["ANLATIM"], encoding="utf-8")
    aciklama_path.write_text(sections["AÇIKLAMA"], encoding="utf-8")
    hashtag_path.write_text(sections["HASHTAG"], encoding="utf-8")

    print("✔ Dosyalar kaydedildi:")
    print(anlatim_path)
    print(aciklama_path)
    print(hashtag_path)
        audio_file = f"anlatim_{ts}.mp3"
    audio_path = text_to_speech(sections["ANLATIM"], audio_file)
    print("🎙️ Ses dosyası oluşturuldu:", audio_path)


def main():
    print("📜 Tarih içeriği üretiliyor...")
    raw_output = generate_history_content()

    sections = parse_sections(raw_output)

    if not all(sections.values()):
        raise ValueError("Çıktı formatı bozuk. Prompt formatını kontrol et.")

    save_output(sections)

if __name__ == "__main__":
    main()

