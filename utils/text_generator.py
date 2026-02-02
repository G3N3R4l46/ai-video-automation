import os
from pathlib import Path
import google.generativeai as genai

# === AYARLAR ===
BASE_DIR = Path(__file__).resolve().parents[1]
PROMPT_PATH = BASE_DIR / "prompts" / "tarih_prompt.txt"

MODEL_NAME = "gemini-1.5-flash"  # ücretsiz ve hızlı

def load_prompt():
    if not PROMPT_PATH.exists():
        raise FileNotFoundError("tarih_prompt.txt bulunamadı.")
    return PROMPT_PATH.read_text(encoding="utf-8")

def setup_genai():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")
    if not api_key:
        raise EnvironmentError("API key bulunamadı. Repo Secrets kontrol et.")
    genai.configure(api_key=api_key)

def generate_history_content(extra_context: str = ""):
    """
    extra_context: Gündem, tarih, özel bir olay eklemek istersen
    """
    setup_genai()
    prompt = load_prompt()

    full_prompt = prompt
    if extra_context:
        full_prompt += f"\n\nEk bağlam:\n{extra_context}"

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(full_prompt)

    if not response or not response.text:
        raise RuntimeError("AI çıktı üretmedi.")

    return response.text.strip()

if __name__ == "__main__":
    # Test amaçlı
    print("İçerik üretiliyor...\n")
    output = generate_history_content()
    print(output)

