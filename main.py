"""
Milyona Giden Yol — Telegram Bot
Giriş noktası: bot başlatma, router kayıt, polling.
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN
from database import init_db
from handlers import start, game, profile

# Loglama ayarları
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    # Veritabanını hazırla
    await init_db()
    logger.info("Veritabanı hazır.")

    # Bot ve Dispatcher oluştur
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # Router'ları kaydet (sıra önemli — game en son)
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(game.router)

    logger.info("Bot başlatılıyor...")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        logger.info("Bot durduruldu.")


if __name__ == "__main__":
    asyncio.run(main())
