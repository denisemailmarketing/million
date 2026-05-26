"""
Oyun akışını yöneten handler — /play komutu ve tüm oyun callback'leri.

Akış:
  /play veya 'play' callback
    → aktif oyun kontrolü
    → yeni oyun oluştur
    → ilk soruyu gönder + zamanlayıcı başlat

  answer:<game_id>:<seçim>
    → doğru mu?
      Evet → ödül mesajı + devam et / al butonu
      Hayır → oyun bitti mesajı

  continue:<game_id>  → bir sonraki soruyu gönder
  cashout:<game_id>   → kazancı al, oyunu bitir
  fifty:<game_id>     → 50/50 uygula, soruyu yeniden gönder
  giveup:<game_id>    → oyundan çık
  restart:<game_id>   → aktif oyunu iptal et, yeni oyun başlat
  resume:<game_id>    → aktif oyuna devam et
"""

import asyncio
import json
import logging

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import database as db
from game_logic import (
    select_questions,
    get_prize,
    format_prize,
    apply_fifty_fifty,
    parse_questions_json,
    build_question_message,
    build_correct_message,
    build_wrong_message,
    build_timeout_message,
    build_cashout_message,
    build_giveup_message,
)
from keyboards import (
    answer_keyboard,
    continue_or_cashout_keyboard,
    play_again_keyboard,
    confirm_restart_keyboard,
)
from config import QUESTION_TIMEOUT, TOTAL_QUESTIONS_PER_GAME

router = Router()
logger = logging.getLogger(__name__)

# game_id → asyncio.Task (zamanlayıcı)
_timers: dict[int, asyncio.Task] = {}


# ─── Yardımcılar ─────────────────────────────────────────────────────────────

def _cancel_timer(game_id: int) -> None:
    """Varsa zamanlayıcıyı iptal et."""
    task = _timers.pop(game_id, None)
    if task and not task.done():
        task.cancel()


async def _send_question(
    bot: Bot,
    chat_id: int,
    game_id: int,
    questions: list[dict],
    question_index: int,
    used_fifty_fifty: bool,
    edit_message_id: int | None = None,
) -> None:
    """Soruyu gönder (veya düzenle) ve zamanlayıcı başlat."""
    q = questions[question_index]
    text = build_question_message(q, question_number=question_index + 1)
    kb = answer_keyboard(
        options=q["options"],
        game_id=game_id,
        show_fifty_fifty=not used_fifty_fifty,
    )

    if edit_message_id:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=edit_message_id,
                text=text,
                reply_markup=kb,
                parse_mode="HTML",
            )
        except Exception:
            # Düzenleme başarısız olursa yeni mesaj gönder
            await bot.send_message(chat_id, text, reply_markup=kb, parse_mode="HTML")
    else:
        await bot.send_message(chat_id, text, reply_markup=kb, parse_mode="HTML")

    # Zamanlayıcıyı başlat
    _cancel_timer(game_id)
    _timers[game_id] = asyncio.create_task(
        _timeout_task(bot, chat_id, game_id, question_index)
    )


async def _timeout_task(bot: Bot, chat_id: int, game_id: int, question_index: int) -> None:
    """60 saniye bekle; oyun hâlâ bu soruda ise bitir."""
    try:
        await asyncio.sleep(QUESTION_TIMEOUT)
    except asyncio.CancelledError:
        return  # zamanlayıcı iptal edildi (normal)

    # Oyun hâlâ aktif mi ve aynı soruda mı?
    game = await db.get_game_by_id(game_id)
    if not game or game["status"] != "active":
        return
    if game["current_question_index"] != question_index:
        return  # oyuncu zaten ilerledi

    # Timeout — oyunu bitir
    user = await db.get_user_by_telegram_id_by_db_id(game["user_id"])
    await db.update_game(game_id, status="timeout")
    await db.save_result(
        game["user_id"],
        prize=game["current_prize"],
        correct_answers=question_index,
        status="timeout",
    )
    await db.update_user_stats(game["user_id"], game["current_prize"], question_index)

    await bot.send_message(
        chat_id,
        build_timeout_message(),
        reply_markup=play_again_keyboard(),
        parse_mode="HTML",
    )


async def _finish_game(
    game: dict,
    chat_id: int,
    bot: Bot,
    status: str,
    text: str,
) -> None:
    """Ortak oyun bitirme işlemi."""
    game_id = game["id"]
    _cancel_timer(game_id)
    correct = game["current_question_index"]

    # Oyun durumunu güncelle
    await db.update_game(game_id, status=status)

    # Sonucu kaydet
    await db.save_result(
        game["user_id"],
        prize=game["current_prize"],
        correct_answers=correct,
        status=status,
    )
    await db.update_user_stats(game["user_id"], game["current_prize"], correct)

    await bot.send_message(chat_id, text, reply_markup=play_again_keyboard(), parse_mode="HTML")


# ─── /play komutu ─────────────────────────────────────────────────────────────

async def _start_new_game(user_db_id: int, bot: Bot, chat_id: int) -> None:
    """Yeni oyun oluştur ve ilk soruyu gönder."""
    questions = select_questions()
    game_id = await db.create_game(user_db_id, questions)

    await bot.send_message(
        chat_id,
        "🎙 <b>Milyona Giden Yol</b> başlıyor!\n\n"
        "Hazır mısınız? İlk sorunuz geliyor... 🔥",
        parse_mode="HTML",
    )

    await _send_question(
        bot=bot,
        chat_id=chat_id,
        game_id=game_id,
        questions=questions,
        question_index=0,
        used_fifty_fifty=False,
    )


@router.message(Command("play"))
async def cmd_play(message: Message, bot: Bot) -> None:
    user = await db.get_or_create_user(
        telegram_id=message.from_user.id,  # type: ignore[union-attr]
        username=message.from_user.username,  # type: ignore[union-attr]
        first_name=message.from_user.first_name or "Oyuncu",  # type: ignore[union-attr]
    )
    active = await db.get_active_game(user["id"])

    if active:
        await message.answer(
            "⚠️ Zaten aktif bir oyununuz var!\n\n"
            "Yeniden başlamak istiyor musunuz? Mevcut oyununuz silinecek.",
            reply_markup=confirm_restart_keyboard(active["id"]),
            parse_mode="HTML",
        )
        return

    await _start_new_game(user["id"], bot, message.chat.id)


# ─── Callback: 'play' butonu (ana menüden) ────────────────────────────────────

@router.callback_query(F.data == "play")
async def cb_play(callback: CallbackQuery, bot: Bot) -> None:
    user = await db.get_or_create_user(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        first_name=callback.from_user.first_name or "Oyuncu",
    )
    active = await db.get_active_game(user["id"])

    await callback.answer()

    if active:
        await callback.message.answer(  # type: ignore[union-attr]
            "⚠️ Zaten aktif bir oyununuz var!\n\n"
            "Yeniden başlamak istiyor musunuz? Mevcut oyununuz silinecek.",
            reply_markup=confirm_restart_keyboard(active["id"]),
            parse_mode="HTML",
        )
        return

    await _start_new_game(user["id"], bot, callback.message.chat.id)  # type: ignore[union-attr]


# ─── Callback: Yeniden başla / devam et ───────────────────────────────────────

@router.callback_query(F.data.startswith("restart:"))
async def cb_restart(callback: CallbackQuery, bot: Bot) -> None:
    old_game_id = int(callback.data.split(":")[1])  # type: ignore[union-attr]
    _cancel_timer(old_game_id)
    await db.finish_all_active_games(
        (await db.get_game_by_id(old_game_id))["user_id"], status="lost"  # type: ignore[index]
    )
    await callback.answer("Yeni oyun başlıyor!")

    user = await db.get_or_create_user(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        first_name=callback.from_user.first_name or "Oyuncu",
    )
    await _start_new_game(user["id"], bot, callback.message.chat.id)  # type: ignore[union-attr]


@router.callback_query(F.data.startswith("resume:"))
async def cb_resume(callback: CallbackQuery, bot: Bot) -> None:
    game_id = int(callback.data.split(":")[1])  # type: ignore[union-attr]
    game = await db.get_game_by_id(game_id)

    if not game or game["status"] != "active":
        await callback.answer("Oyun bulunamadı.", show_alert=True)
        return

    questions = parse_questions_json(game["questions_json"])
    idx = game["current_question_index"]

    await callback.answer("Oyuna devam ediyorsunuz!")
    await _send_question(
        bot=bot,
        chat_id=callback.message.chat.id,  # type: ignore[union-attr]
        game_id=game_id,
        questions=questions,
        question_index=idx,
        used_fifty_fifty=bool(game["used_fifty_fifty"]),
    )


# ─── Callback: Cevap ──────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("answer:"))
async def cb_answer(callback: CallbackQuery, bot: Bot) -> None:
    parts = callback.data.split(":", 2)  # type: ignore[union-attr]
    game_id = int(parts[1])
    chosen = parts[2]

    game = await db.get_game_by_id(game_id)

    # Güvenlik kontrolleri
    if not game or game["status"] != "active":
        await callback.answer("Bu oyun artık aktif değil.", show_alert=True)
        return

    # Cevabı veren kişi oyunun sahibi mi?
    user = await db.get_user_by_telegram_id(callback.from_user.id)
    if not user or user["id"] != game["user_id"]:
        await callback.answer("Bu oyun size ait değil!", show_alert=True)
        return

    _cancel_timer(game_id)

    questions = parse_questions_json(game["questions_json"])
    idx = game["current_question_index"]
    q = questions[idx]
    correct = q["correct"]
    prize = get_prize(idx)

    await callback.answer()

    if chosen == correct:
        # ── Doğru ──────────────────────────────────────────────────────────
        is_last = (idx + 1) == TOTAL_QUESTIONS_PER_GAME

        # Ödülü güncelle
        await db.update_game(game_id, current_prize=prize)

        if is_last:
            # Oyun kazanıldı
            await db.update_game(
                game_id,
                current_question_index=idx + 1,
                current_prize=prize,
                status="won",
            )
            await db.save_result(user["id"], prize=prize, correct_answers=idx + 1, status="won")
            await db.update_user_stats(user["id"], prize, idx + 1)

            await callback.message.answer(  # type: ignore[union-attr]
                build_correct_message(prize, is_last=True),
                reply_markup=play_again_keyboard(),
                parse_mode="HTML",
            )
        else:
            # Bir sonraki soruya geçiş seçeneği sun
            await db.update_game(
                game_id,
                current_question_index=idx + 1,
                current_prize=prize,
            )
            await callback.message.answer(  # type: ignore[union-attr]
                build_correct_message(prize, is_last=False),
                reply_markup=continue_or_cashout_keyboard(game_id),
                parse_mode="HTML",
            )
    else:
        # ── Yanlış ──────────────────────────────────────────────────────────
        await _finish_game(
            game=game,
            chat_id=callback.message.chat.id,  # type: ignore[union-attr]
            bot=bot,
            status="lost",
            text=build_wrong_message(correct),
        )


# ─── Callback: Devam et ───────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("continue:"))
async def cb_continue(callback: CallbackQuery, bot: Bot) -> None:
    game_id = int(callback.data.split(":")[1])  # type: ignore[union-attr]
    game = await db.get_game_by_id(game_id)

    if not game or game["status"] != "active":
        await callback.answer("Oyun aktif değil.", show_alert=True)
        return

    questions = parse_questions_json(game["questions_json"])
    idx = game["current_question_index"]

    await callback.answer("Devam ediyoruz! Son kararınız mı? 🔥")

    await _send_question(
        bot=bot,
        chat_id=callback.message.chat.id,  # type: ignore[union-attr]
        game_id=game_id,
        questions=questions,
        question_index=idx,
        used_fifty_fifty=bool(game["used_fifty_fifty"]),
    )


# ─── Callback: Kazancı al ─────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("cashout:"))
async def cb_cashout(callback: CallbackQuery, bot: Bot) -> None:
    game_id = int(callback.data.split(":")[1])  # type: ignore[union-attr]
    game = await db.get_game_by_id(game_id)

    if not game or game["status"] != "active":
        await callback.answer("Oyun aktif değil.", show_alert=True)
        return

    _cancel_timer(game_id)
    prize = game["current_prize"]

    await db.update_game(game_id, status="cashed_out")
    await db.save_result(
        game["user_id"],
        prize=prize,
        correct_answers=game["current_question_index"],
        status="cashed_out",
    )
    await db.update_user_stats(game["user_id"], prize, game["current_question_index"])

    await callback.answer("Kazancınız alındı! 💰")
    await callback.message.answer(  # type: ignore[union-attr]
        build_cashout_message(prize),
        reply_markup=play_again_keyboard(),
        parse_mode="HTML",
    )


# ─── Callback: 50/50 ──────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("fifty:"))
async def cb_fifty(callback: CallbackQuery, bot: Bot) -> None:
    game_id = int(callback.data.split(":")[1])  # type: ignore[union-attr]
    game = await db.get_game_by_id(game_id)

    if not game or game["status"] != "active":
        await callback.answer("Oyun aktif değil.", show_alert=True)
        return

    if game["used_fifty_fifty"]:
        await callback.answer("50/50 hakkını zaten kullandınız!", show_alert=True)
        return

    # 50/50 uygula
    questions = parse_questions_json(game["questions_json"])
    idx = game["current_question_index"]
    q = questions[idx]
    reduced = apply_fifty_fifty(q["options"], q["correct"])

    # Güncellenmiş şıkları kaydet
    questions[idx]["options"] = reduced
    async def _save_reduced_options():
        import aiosqlite
        from config import DB_PATH
        async with aiosqlite.connect(DB_PATH) as conn:
            await conn.execute(
                "UPDATE games SET questions_json = ?, used_fifty_fifty = 1 WHERE id = ?",
                (json.dumps(questions, ensure_ascii=False), game_id),
            )
            await conn.commit()

    await _save_reduced_options()

    await callback.answer("50/50 kullanıldı! 🧠")

    # Zamanlayıcıyı iptal etme — süre devam ediyor
    # Soruyu güncellenmiş şıklarla yeniden gönder
    text = build_question_message(q, question_number=idx + 1)
    kb = answer_keyboard(
        options=reduced,
        game_id=game_id,
        show_fifty_fifty=False,  # artık gösterme
    )
    try:
        await callback.message.edit_text(  # type: ignore[union-attr]
            text + "\n\n🧠 <i>50/50 kullanıldı — 2 yanlış şık kaldırıldı.</i>",
            reply_markup=kb,
            parse_mode="HTML",
        )
    except Exception as e:
        logger.warning("edit_text başarısız: %s", e)
        await bot.send_message(
            callback.message.chat.id,  # type: ignore[union-attr]
            text + "\n\n🧠 <i>50/50 kullanıldı — 2 yanlış şık kaldırıldı.</i>",
            reply_markup=kb,
            parse_mode="HTML",
        )


# ─── Callback: Pes et ─────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("giveup:"))
async def cb_giveup(callback: CallbackQuery, bot: Bot) -> None:
    game_id = int(callback.data.split(":")[1])  # type: ignore[union-attr]
    game = await db.get_game_by_id(game_id)

    if not game or game["status"] != "active":
        await callback.answer("Oyun aktif değil.", show_alert=True)
        return

    await _finish_game(
        game=game,
        chat_id=callback.message.chat.id,  # type: ignore[union-attr]
        bot=bot,
        status="lost",
        text=build_giveup_message(),
    )
    await callback.answer("Oyundan çıkıldı.")
