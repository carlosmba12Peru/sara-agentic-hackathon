import os
import sys
import time
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

from dotenv import load_dotenv
load_dotenv()
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

modelos = [
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite"
]

print("Probando velocidad real de modelos soportados:")
for m in modelos:
    t0 = time.time()
    try:
        res = client.models.generate_content(
            model=m,
            contents="Hola, responde brevemente 'OK'"
        )
        dt = time.time() - t0
        print(f"✅ {m}: {dt:.3f}s -> {res.text.strip()}")
    except Exception as e:
        dt = time.time() - t0
        print(f"❌ {m} ({dt:.3f}s): {e}")
