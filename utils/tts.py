from pathlib import Path
from gtts import gTTS

BASE_DIR = Path(__file__).resolve().parents[1]
AUDIO_DIR = BASE_DIR / "output" / "audio"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def text_to_speech(text: str, filename: str):
    """
    Türkçe metni mp3 ses dosyasına çevirir
    """
    if not text.strip():
        raise ValueError("Seslendirme için metin boş.")

    output_path = AUDIO_DIR / filename

    tts = gTTS(
        text=text,
        lang="tr",
        slow=False  # TikTok temposu için hızlı
    )

    tts.save(str(output_path))
    return output_path

if __name__ == "__main__":
    # Test
    demo_text = "Bu olay, tarihin karanlık sayfalarında gizli kaldı."
    path = text_to_speech(demo_text, "demo.mp3")
    print(f"Ses oluşturuldu: {path}")

