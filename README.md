# Lugatçe WhatsApp Kanal Botu

Günlük 09.00 Türkiye saati için GitHub Actions + Python AI içerik üretimi.

## GitHub Actions ayarları
Secrets: AI_API_KEY
Variables:
- AI_BASE_URL = https://generativelanguage.googleapis.com/v1beta/openai/
- AI_MODEL = gemini-2.5-flash
- CONTENT_PROMPT = Her gün az bilinen bir Türkçe kelimeyi anlamı ve örnek cümlesiyle anlat.
- CONTENT_MODE = ai
- DRY_RUN = true

Actions sekmesinden Lugatce Daily Bot > Run workflow ile dene.
Çıktı artifact olarak saklanır.

## Önemli
WhatsApp Channels için resmi yayın API'si yoktur. Bu sürüm gerçek kanal yayını yapmaz; DRY_RUN=false olduğunda doğrulanmamış gönderim yerine açık hata verir. WhatsApp oturum dosyasını repoya veya Actions artifact'ına yüklemeyin. Kanal UI otomasyonu ayrıca doğrulanmalıdır.
