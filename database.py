"""
Veritabanı işlemleri — aiosqlite kullanılarak async SQLite.
Tablolar: users, games, results
"""

import json
import aiosqlite
from datetime import datetime
from config import DB_PATH


# ─── Başlangıç ────────────────────────────────────────────────────────────────

async def init_db() -> None:
    """Tabloları oluştur (yoksa). DB dizini yoksa oluştur."""
    import os
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True) if os.path.dirname(DB_PATH) else None
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                username    TEXT,
                first_name  TEXT,
                total_games INTEGER DEFAULT 0,
                best_score  INTEGER DEFAULT 0,
                best_prize  INTEGER DEFAULT 0,
                total_prize INTEGER DEFAULT 0,
                created_at  TEXT DEFAULT (datetime('now'))
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id                    INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id               INTEGER NOT NULL,
                status                TEXT    DEFAULT 'active',
                current_question_index INTEGER DEFAULT 0,
                current_prize         INTEGER DEFAULT 0,
                used_fifty_fifty      INTEGER DEFAULT 0,
                questions_json        TEXT,
                started_at            TEXT    DEFAULT (datetime('now')),
                finished_at           TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id          INTEGER NOT NULL,
                prize            INTEGER DEFAULT 0,
                correct_answers  INTEGER DEFAULT 0,
                status           TEXT,
                created_at       TEXT    DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        await db.commit()


# ─── Kullanıcı ────────────────────────────────────────────────────────────────

async def get_or_create_user(telegram_id: int, username: str | None, first_name: str) -> dict:
    """Kullanıcıyı getir, yoksa oluştur."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        # Güncelle veya ekle
        await db.execute("""
            INSERT INTO users (telegram_id, username, first_name)
            VALUES (?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE
                SET username   = excluded.username,
                    first_name = excluded.first_name
        """, (telegram_id, username, first_name))
        await db.commit()

        async with db.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
        ) as cur:
            row = await cur.fetchone()
            return dict(row)


async def get_user_by_telegram_id(telegram_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
        ) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def update_user_stats(user_id: int, prize: int, correct_answers: int) -> None:
    """Oyun bittikten sonra istatistikleri güncelle."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE users
            SET total_games = total_games + 1,
                total_prize = total_prize + ?,
                best_prize  = MAX(best_prize, ?),
                best_score  = MAX(best_score, ?)
            WHERE id = ?
        """, (prize, prize, correct_answers, user_id))
        await db.commit()


# ─── Oyun ─────────────────────────────────────────────────────────────────────

async def create_game(user_id: int, questions: list[dict]) -> int:
    """Yeni oyun oluştur, game_id döndür."""
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("""
            INSERT INTO games (user_id, questions_json)
            VALUES (?, ?)
        """, (user_id, json.dumps(questions, ensure_ascii=False)))
        await db.commit()
        return cur.lastrowid  # type: ignore[return-value]


async def get_active_game(user_id: int) -> dict | None:
    """Kullanıcının aktif oyununu getir."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM games WHERE user_id = ? AND status = 'active'",
            (user_id,)
        ) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def get_game_by_id(game_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM games WHERE id = ?", (game_id,)
        ) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def update_game(
    game_id: int,
    *,
    current_question_index: int | None = None,
    current_prize: int | None = None,
    used_fifty_fifty: bool | None = None,
    status: str | None = None,
) -> None:
    """Oyun durumunu kısmen güncelle."""
    fields, values = [], []

    if current_question_index is not None:
        fields.append("current_question_index = ?")
        values.append(current_question_index)
    if current_prize is not None:
        fields.append("current_prize = ?")
        values.append(current_prize)
    if used_fifty_fifty is not None:
        fields.append("used_fifty_fifty = ?")
        values.append(1 if used_fifty_fifty else 0)
    if status is not None:
        fields.append("status = ?")
        values.append(status)
        if status != "active":
            fields.append("finished_at = ?")
            values.append(datetime.now().isoformat(sep=" ", timespec="seconds"))

    if not fields:
        return

    values.append(game_id)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            f"UPDATE games SET {', '.join(fields)} WHERE id = ?", values
        )
        await db.commit()


async def finish_all_active_games(user_id: int, status: str = "lost") -> None:
    """Kullanıcının tüm açık oyunlarını kapat (yeniden başlarken temizlik)."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE games
            SET status = ?, finished_at = datetime('now')
            WHERE user_id = ? AND status = 'active'
        """, (status, user_id))
        await db.commit()


# ─── Sonuç ────────────────────────────────────────────────────────────────────

async def save_result(user_id: int, prize: int, correct_answers: int, status: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO results (user_id, prize, correct_answers, status)
            VALUES (?, ?, ?, ?)
        """, (user_id, prize, correct_answers, status))
        await db.commit()


# ─── Liderlik ─────────────────────────────────────────────────────────────────

async def get_user_by_telegram_id_by_db_id(user_db_id: int) -> dict | None:
    """DB id'si ile kullanıcıyı getir."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users WHERE id = ?", (user_db_id,)
        ) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def get_top_players(limit: int = 10) -> list[dict]:
    """En iyi ödülü kazanan ilk N oyuncuyu döndür."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT first_name, username, best_prize, total_games
            FROM users
            ORDER BY best_prize DESC
            LIMIT ?
        """, (limit,)) as cur:
            rows = await cur.fetchall()
            return [dict(r) for r in rows]
