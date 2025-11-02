import os
import google.generativeai as genai
from dotenv import load_dotenv

print("AI servisine bağlanılıyor")

try:
    load_dotenv()
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError("API_KEY .env dosyasında bulunamadı!")

    genai.configure(api_key=api_key)

    print("\n--- Kullanabileceğin Modeller ---")

    found_models = False
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(model.name)
            found_models = True

    if not found_models:
        print("Metin üretimi için uygun model bulunamadı.")

except Exception as e:
    print(f"\n!!! Bir hata oluştu: {e}")
