import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

try:
    genai.configure(api_key=os.getenv("API_KEY"))
    model = genai.GenerativeModel('gemini-flash-latest')
    print("Yapay zeka servisi başlatıldı.")

except Exception as e:
    print(f"Yapay zeka servisi başlatılırken bir hata oluştu: {e}")
    model = None
