"""
Oyun mantığı — soru seçimi, 50/50, ödül hesaplama, mesaj şablonları.
"""

import json
import random
from config import PRIZE_LADDER, TOTAL_QUESTIONS_PER_GAME
from questions import QUESTIONS


def select_questions() -> list[dict]:
    """
    Toplam 100 sorudan rastgele 10 soru seç.
    Seçilen sorularda şıkların sırası da karıştırılır.
    """
    chosen = random.sample(QUESTIONS, TOTAL_QUESTIONS_PER_GAME)
    result = []
    for q in chosen:
        options = q["options"].copy()
        random.shuffle(options)
        result.append({
            "category": q["category"],
            "question": q["question"],
            "options": options,          # karıştırılmış şıklar
            "correct": q["correct"],
        })
    return result


def get_prize(question_index: int) -> int:
    """0-tabanlı soru indeksine göre ödülü döndür."""
    if 0 <= question_index < len(PRIZE_LADDER):
        return PRIZE_LADDER[question_index]
    return 0


def format_prize(amount: int) -> str:
    """1000000 → '1.000.000 TL'"""
    return f"{amount:,.0f}".replace(",", ".") + " TL"


def apply_fifty_fifty(options: list[str], correct: str) -> list[str]:
    """
    50/50: doğru cevabı + rastgele 1 yanlış cevabı bırak,
    geri kalan 2 yanlışı kaldır.
    Döndürülen liste 2 elemanlı ve sırası karıştırılmış.
    """
    wrong = [o for o in options if o != correct]
    kept_wrong = random.choice(wrong)
    remaining = [correct, kept_wrong]
    random.shuffle(remaining)
    return remaining


def build_question_message(
    question_data: dict,
    question_number: int,      # 1-tabanlı
    total: int = TOTAL_QUESTIONS_PER_GAME,
) -> str:
    """Soru mesajını HTML olarak oluştur."""
    prize = format_prize(get_prize(question_number - 1))
    is_last = question_number == total

    header = "🎙 <b>Milyona Giden Yol</b>\n"
    if is_last:
        header += "\n🔥 <b>1.000.000 TL için son soru!</b>\n"

    return (
        f"{header}\n"
        f"Soru <b>{question_number}/{total}</b>\n"
        f"Kategori: <i>{question_data['category']}</i>\n"
        f"Ödül: <b>{prize}</b>\n\n"
        f"❓ {question_data['question']}\n\n"
        f"⏳ Süre: <b>60 saniye</b>"
    )


def build_correct_message(prize: int, is_last: bool = False) -> str:
    if is_last:
        return (
            "🏆 <b>İnanılmaz!</b>\n\n"
            "Tüm soruları doğru cevapladınız.\n"
            f"Büyük ödül sizin: <b>{format_prize(prize)}</b>!\n\n"
            "Milyona Giden Yol'un yeni yıldızı sizsiniz! 🌟"
        )
    return (
        "✅ <b>Doğru cevap!</b>\n\n"
        f"Şu anki kazancınız: <b>{format_prize(prize)}</b>\n\n"
        "Devam ederseniz sıradaki soru daha değerli olacak.\n"
        "<i>Karar sizin...</i>"
    )


def build_wrong_message(correct_answer: str) -> str:
    return (
        "❌ <b>Maalesef yanlış cevap...</b>\n\n"
        f"Doğru cevap: <b>{correct_answer}</b>\n\n"
        "Yarışma sona erdi.\n"
        "Tekrar denemeye hazır mısınız? 💪"
    )


def build_timeout_message() -> str:
    return (
        "⏰ <b>Süre doldu!</b>\n\n"
        "Cevap vermek için 60 saniyeniz vardı.\n"
        "Yarışma sona erdi."
    )


def build_cashout_message(prize: int) -> str:
    return (
        "💰 <b>Kazancınızı aldınız!</b>\n\n"
        f"Tebrikler! <b>{format_prize(prize)}</b> kazandınız.\n\n"
        "Akıllıca bir karar. Bir dahaki sefere daha da ilerlersiniz! 🎯"
    )


def build_giveup_message() -> str:
    return (
        "🏳 <b>Oyundan çıktınız.</b>\n\n"
        "Bir dahaki sefere daha şanslı olursunuz!"
    )


def parse_questions_json(questions_json: str) -> list[dict]:
    """DB'den gelen JSON string'i çöz."""
    return json.loads(questions_json)
