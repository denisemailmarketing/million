"""
Telegram inline ve reply klavyeleri.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Ana menü."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Oyuna Başla", callback_data="play")],
        [
            InlineKeyboardButton(text="📊 Profilim", callback_data="profile"),
            InlineKeyboardButton(text="🏆 Liderlik Tablosu", callback_data="top"),
        ],
        [InlineKeyboardButton(text="📖 Kurallar", callback_data="rules")],
    ])


def answer_keyboard(options: list[str], game_id: int, show_fifty_fifty: bool) -> InlineKeyboardMarkup:
    """
    Cevap şıklarını göster.
    options — gösterilecek şıklar (2 veya 4 adet).
    50/50 henüz kullanılmadıysa buton eklenir.
    """
    rows = []

    # Şıklar — A, B, C, D etiketleriyle
    labels = ["A", "B", "C", "D"]
    for i, opt in enumerate(options):
        label = labels[i] if i < len(labels) else str(i + 1)
        rows.append([
            InlineKeyboardButton(
                text=f"{label}) {opt}",
                callback_data=f"answer:{game_id}:{opt}"
            )
        ])

    # Yardım / çıkış satırı
    bottom = []
    if show_fifty_fifty:
        bottom.append(InlineKeyboardButton(text="🧠 50/50", callback_data=f"fifty:{game_id}"))
    bottom.append(InlineKeyboardButton(text="🏳 Pes Et", callback_data=f"giveup:{game_id}"))
    rows.append(bottom)

    return InlineKeyboardMarkup(inline_keyboard=rows)


def continue_or_cashout_keyboard(game_id: int) -> InlineKeyboardMarkup:
    """Doğru cevaptan sonra devam et / kazancı al."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="▶️ Devam Et", callback_data=f"continue:{game_id}"),
            InlineKeyboardButton(text="💰 Kazancı Al", callback_data=f"cashout:{game_id}"),
        ]
    ])


def play_again_keyboard() -> InlineKeyboardMarkup:
    """Oyun bittikten sonra."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Tekrar Oyna", callback_data="play")],
        [
            InlineKeyboardButton(text="📊 Profilim", callback_data="profile"),
            InlineKeyboardButton(text="🏆 Liderlik Tablosu", callback_data="top"),
        ],
    ])


def confirm_restart_keyboard(game_id: int) -> InlineKeyboardMarkup:
    """Aktif oyun varken yeni oyun isteme."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Evet, Yeniden Başla", callback_data=f"restart:{game_id}"),
            InlineKeyboardButton(text="❌ Hayır, Devam Et", callback_data=f"resume:{game_id}"),
        ]
    ])
