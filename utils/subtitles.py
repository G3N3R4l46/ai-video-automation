from pathlib import Path
import math

BASE_DIR = Path(__file__).resolve().parents[1]
SUB_DIR = BASE_DIR / "output" / "subtitles"
SUB_DIR.mkdir(parents=True, exist_ok=True)

def seconds_to_timestamp(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec - math.floor(sec)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def split_sentences(text: str):
    # Nokta, soru, ünlem bazlı böl
    raw = []
    buff = ""
    for ch in text:
        buff += ch
        if ch in ".?!":
            raw.append(buff.strip())
            buff = ""
    if buff.strip():
        raw.append(buff.strip())

    # Çok uzun satırları ikiye böl
    sentences = []
    for s in raw:
        if len(s) > 80:
            mid = len(s) // 2
            sentences.append(s[:mid].strip())
            sentences.append(s[mid:].strip())
        else:
            sentences.append(s)
    return sentences

def generate_srt(anlatim_text: str, filename: str, total_duration: float = 40.0):
    """
    anlatim_text: seslendirme metni
    total_duration: videonun yaklaşık süresi (sn)
    """
    if not anlatim_text.strip():
        raise ValueError("Altyazı için metin boş.")

    sentences = split_sentences(anlatim_text)
    count = len(sentences)
    if count == 0:
        raise ValueError("Cümle bulunamadı.")

    per_sentence = total_duration / count
    current_time = 0.0

    lines = []
    for i, s in enumerate(sentences, start=1):
        start = seconds_to_timestamp(current_time)
        end = seconds_to_timestamp(current_time + per_sentence)
        current_time += per_sentence

        lines.append(str(i))
        lines.append(f"{start} --> {end}")
        lines.append(s)
        lines.append("")

    srt_content = "\n".join(lines)
    out_path = SUB_DIR / filename
    out_path.write_text(srt_content, encoding="utf-8")
    return out_path

if __name__ == "__main__":
    demo = (
        "Bu olay tarihten özellikle silindi. "
        "Yıllar boyunca kimse konuşmadı. "
        "Ama gerçek, her zaman bir yolunu bulur."
    )
    path = generate_srt(demo, "demo.srt", total_duration=30.0)
    print("Altyazı oluşturuldu:", path)

