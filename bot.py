import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from openai import OpenAI
from playwright.async_api import async_playwright

CHANNEL = os.getenv("CHANNEL_NAME", "Lugatçe")
DRY_RUN = os.getenv("DRY_RUN", "true").lower() != "false"
PROMPT = os.getenv("CONTENT_PROMPT", "Türkçede az bilinen bir kelimeyi, anlamını ve örnek cümlesini paylaş. 500 karakteri geçme.")

def generate():
    if os.getenv("CONTENT_MODE", "ai") == "static":
        return PROMPT
    key = os.environ["AI_API_KEY"]
    client = OpenAI(api_key=key, base_url=os.getenv("AI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/"))
    result = client.chat.completions.create(
        model=os.getenv("AI_MODEL", "gemini-2.5-flash"),
        messages=[{"role": "user", "content": PROMPT}],
        max_tokens=400,
    )
    text = (result.choices[0].message.content or "").strip()
    if not text:
        raise RuntimeError("AI boş içerik üretti")
    return text

async def publish(message):
    state = Path("whatsapp_state.json")
    if not state.exists():
        raise RuntimeError("WhatsApp oturumu yok. Yerel bilgisayarda QR ile giriş yapıp güvenli oturum aktarımı gerekir.")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=str(state))
        page = await context.new_page()
        await page.goto("https://web.whatsapp.com/", wait_until="domcontentloaded")
        await page.wait_for_timeout(12000)
        # Fail closed: Channel UI is undocumented and requires validation on a live authorized account.
        await browser.close()
        raise RuntimeError("Kanal yayın seçicileri henüz doğrulanmadı; yanlış hedefe mesaj gönderilmedi.")

async def main():
    message = generate()
    Path("output").mkdir(exist_ok=True)
    path = Path("output") / (datetime.now(ZoneInfo("Europe/Istanbul")).strftime("%Y-%m-%d") + ".txt")
    path.write_text(message, encoding="utf-8")
    print(f"İçerik üretildi: {path}; hedef kanal: {CHANNEL}")
    if DRY_RUN:
        print("DRY_RUN aktif; yayın yapılmadı.")
    else:
        await publish(message)

if __name__ == "__main__":
    asyncio.run(main())
