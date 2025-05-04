import google.generativeai as genai
from dotenv import load_dotenv
import os

# .envファイルからAPIキーの情報を読み取ります。
load_dotenv()
# Geminiの準備をします。
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# ========================== ↓↓↓ ここから下に記述してください ↓↓↓ ==========================
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = "こんにちは"

response = model.generate_content(prompt)

print(response.text)