import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN bulunamadı! Lütfen .env dosyasını kontrol edin.")

DB_PATH: str = os.getenv("DB_PATH", "game.db")

# Soru başına süre (saniye)
QUESTION_TIMEOUT: int = 60

# Ödül basamakları (1. sorudan 10. soruya)
PRIZE_LADDER: list[int] = [
    500,       # 1. soru
    1_000,     # 2. soru
    2_500,     # 3. soru
    5_000,     # 4. soru
    10_000,    # 5. soru
    25_000,    # 6. soru
    50_000,    # 7. soru
    100_000,   # 8. soru
    250_000,   # 9. soru
    1_000_000, # 10. soru
]

TOTAL_QUESTIONS_PER_GAME: int = 10
