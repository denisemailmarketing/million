"""
/profile ve /top komutları + ilgili callback'ler.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from database import get_user_by_telegram_id, get_top_players
from game_logic import format_prize
from keyboards import main_menu_keyboard

router = Router()

MEDALS = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


def _profile_text(user: dict) -> str:
    name = user.get("first_name") or "Oyuncu"
    username = f"@{user['username']}" if user.get("username") else "—"
    return (
        f"📊 <b>Profil: {name}</b>\n"
        f"Kullanıcı adı: {username}\n\n"
        f"🎮 Toplam Oyun: <b>{user['total_games']}</b>\n"
        f"🏆 En Yüksek Ödül: <b>{format_prize(user['best_prize'])}</b>\n"
        f"✅ En İyi Skor: <b>{user['best_score']} doğru cevap</b>\n"
        f"💰 Toplam Kazanç: <b>{format_prize(user['total_prize'])}</b>"
    )


@router.message(Command("profile"))
async def cmd_profile(message: Message) -> None:
    user = await get_user_by_telegram_id(message.from_user.id)  # type: ignore[union-attr]
    if not user:
        await message.answer("Henüz kayıtlı değilsiniz. /start yazın.", parse_mode="HTML")
        return
    await message.answer(_profile_text(user), parse_mode="HTML", reply_markup=main_menu_keyboard())


@router.message(Command("top"))
async def cmd_top(message: Message) -> None:
    players = await get_top_players(10)
    await message.answer(_top_text(players), parse_mode="HTML", reply_markup=main_menu_keyboard())


@router.callback_query(F.data == "profile")
async def cb_profile(callback: CallbackQuery) -> None:
    user = await get_user_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer("Önce /start yazın.", show_alert=True)
        return
    await callback.message.edit_text(  # type: ignore[union-attr]
        _profile_text(user), parse_mode="HTML", reply_markup=main_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "top")
async def cb_top(callback: CallbackQuery) -> None:
    players = await get_top_players(10)
    await callback.message.edit_text(  # type: ignore[union-attr]
        _top_text(players), parse_mode="HTML", reply_markup=main_menu_keyboard()
    )
    await callback.answer()


def _top_text(players: list[dict]) -> str:
    if not players:
        return "🏆 <b>Liderlik Tablosu</b>\n\nHenüz oyun oynanmamış."

    lines = ["🏆 <b>Liderlik Tablosu — En İyi 10</b>\n"]
    for i, p in enumerate(players):
        medal = MEDALS[i] if i < len(MEDALS) else f"{i + 1}."
        name = p.get("first_name") or "Oyuncu"
        username = f" (@{p['username']})" if p.get("username") else ""
        prize = format_prize(p["best_prize"])
        lines.append(f"{medal} <b>{name}</b>{username} — {prize}")

    return "\n".join(lines)
