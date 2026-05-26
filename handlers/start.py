"""
/start, /help, /rules komutları ve ana menü callback'leri.
"""

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from database import get_or_create_user
from keyboards import main_menu_keyboard

router = Router()

WELCOME_TEXT = (
    "🎙 <b>Milyona Giden Yol'a Hoş Geldiniz!</b>\n\n"
    "Bu oyunda <b>10 soruyu</b> doğru cevaplayarak "
    "<b>1.000.000 TL</b> kazanabilirsiniz!\n\n"
    "Her soruyu cevaplamak için <b>60 saniyeniz</b> var.\n"
    "Her doğru cevap sizi bir basamak daha yukarı taşır.\n\n"
    "Hazır mısınız? 🔥"
)

RULES_TEXT = (
    "📖 <b>Oyun Kuralları</b>\n\n"
    "• Her oyunda <b>10 soru</b> sorulur.\n"
    "• Her sorunun <b>4 şıkkı</b> vardır, yalnızca 1 doğru.\n"
    "• Her soru için <b>60 saniye</b> süreniz var.\n"
    "• Doğru cevaptan sonra kazancınızı alabilir veya devam edebilirsiniz.\n"
    "• Yanlış cevap veya süre dolması oyunu bitirir.\n\n"
    "<b>🧠 50/50 Joker:</b> 2 yanlış şıkkı ortadan kaldırır. Oyun başına 1 kez kullanılabilir.\n\n"
    "<b>Ödül Basamakları:</b>\n"
    "1️⃣ 500 TL\n"
    "2️⃣ 1.000 TL\n"
    "3️⃣ 2.500 TL\n"
    "4️⃣ 5.000 TL\n"
    "5️⃣ 10.000 TL\n"
    "6️⃣ 25.000 TL\n"
    "7️⃣ 50.000 TL\n"
    "8️⃣ 100.000 TL\n"
    "9️⃣ 250.000 TL\n"
    "🔟 1.000.000 TL 🏆"
)

HELP_TEXT = (
    "🤖 <b>Bot Komutları</b>\n\n"
    "/start — Ana menüyü aç\n"
    "/play — Yeni oyun başlat\n"
    "/rules — Oyun kuralları\n"
    "/profile — Profilinizi görün\n"
    "/top — Liderlik tablosu\n"
    "/help — Bu yardım mesajı"
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await get_or_create_user(
        telegram_id=message.from_user.id,  # type: ignore[union-attr]
        username=message.from_user.username,  # type: ignore[union-attr]
        first_name=message.from_user.first_name or "Oyuncu",  # type: ignore[union-attr]
    )
    name = message.from_user.first_name or "Oyuncu"  # type: ignore[union-attr]
    await message.answer(
        f"Merhaba, <b>{name}</b>! 👋\n\n{WELCOME_TEXT}",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT, parse_mode="HTML")


@router.message(Command("rules"))
async def cmd_rules(message: Message) -> None:
    await message.answer(RULES_TEXT, parse_mode="HTML", reply_markup=main_menu_keyboard())


# ── Callback: kurallar butonu ──────────────────────────────────────────────────

@router.callback_query(F.data == "rules")
async def cb_rules(callback: CallbackQuery) -> None:
    await callback.message.edit_text(  # type: ignore[union-attr]
        RULES_TEXT, parse_mode="HTML", reply_markup=main_menu_keyboard()
    )
    await callback.answer()
