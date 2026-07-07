from dataclasses import dataclass
from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).parent.parent / "database" / "prompts.db"


# Dataclasses

@dataclass(slots=True)
class Prompt:
    prompt_id: int
    category_id: int
    model_id: int
    conversation_id: int
    prompt_number: int

    prompt_text: str
    raw_output: str | None = None
    expected_behaviour: str | None = None
    source: str | None = None
    notes: str | None = None


@dataclass(slots=True)
class Category:
    category_id: int
    category_name: str
    description: str | None = None


@dataclass(slots=True)
class Model:
    model_id: int
    model_name: str
    provider: str | None = None
    model_version: str | None = None
    notes: str | None = None


@dataclass(slots=True)
class Conversation:
    conversation_id: int
    started_at: str
    title: str | None = None
    source: str | None = None
    notes: str | None = None


# Row mappers

def _row_to_prompt(row: sqlite3.Row) -> Prompt:
    return Prompt(
        prompt_id=row["prompt_id"],
        category_id=row["category_id"],
        model_id=row["model_id"],
        conversation_id=row["conversation_id"],
        prompt_number=row["prompt_number"],
        prompt_text=row["prompt_text"],
        raw_output=row["raw_output"],
        expected_behaviour=row["expected_behaviour"],
        source=row["source"],
        notes=row["notes"],
    )


def _row_to_category(row: sqlite3.Row) -> Category:
    return Category(
        category_id=row["category_id"],
        category_name=row["category_name"],
        description=row["description"],
    )


def _row_to_model(row: sqlite3.Row) -> Model:
    return Model(
        model_id=row["model_id"],
        model_name=row["model_name"],
        provider=row["provider"],
        model_version=row["model_version"],
        notes=row["notes"],
    )


def _row_to_conversation(row: sqlite3.Row) -> Conversation:
    return Conversation(
        conversation_id=row["conversation_id"],
        started_at=row["started_at"],
        title=row["title"],
        source=row["source"],
        notes=row["notes"],
    )


# DB connection

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# Categories

def add_category(name: str, description: str = ""):
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO categories(category_name, description)
            VALUES (?, ?)
            """,
            (name, description),
        )


def list_categories() -> list[Category]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM categories
            ORDER BY category_name
            """
        ).fetchall()

    return [_row_to_category(r) for r in rows]


# Models

def add_model(name: str, provider: str, version: str, notes: str | None = None):
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO models(
                model_name,
                provider,
                model_version,
                notes
            )
            VALUES (?, ?, ?, ?)
            """,
            (name, provider, version, notes),
        )


def list_models() -> list[Model]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM models
            ORDER BY model_name
            """
        ).fetchall()

    return [_row_to_model(r) for r in rows]


# Conversations

def add_conversation(
    started_at: str,
    title: str | None = None,
    source: str | None = None,
    notes: str | None = None,
) -> int:
    with connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO conversations(
                started_at,
                title,
                source,
                notes
            )
            VALUES (?, ?, ?, ?)
            """,
            (started_at, title, source, notes),
        )
        return cur.lastrowid


def get_conversation(conversation_id: int) -> Conversation | None:
    with connect() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM conversations
            WHERE conversation_id = ?
            """,
            (conversation_id,),
        ).fetchone()

    return _row_to_conversation(row) if row else None


def list_conversations() -> list[Conversation]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM conversations
            ORDER BY started_at DESC
            """
        ).fetchall()

    return [_row_to_conversation(r) for r in rows]


# Prompts

def add_prompt(prompt: Prompt):
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO prompts(
                prompt_id,
                category_id,
                model_id,
                conversation_id,
                prompt_number,
                prompt_text,
                raw_output,
                expected_behaviour,
                source,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                prompt.prompt_id,
                prompt.category_id,
                prompt.model_id,
                prompt.conversation_id,
                prompt.prompt_number,
                prompt.prompt_text,
                prompt.raw_output,
                prompt.expected_behaviour,
                prompt.source,
                prompt.notes,
            ),
        )


def get_prompt(prompt_id: int) -> Prompt | None:
    with connect() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM prompts
            WHERE prompt_id = ?
            """,
            (prompt_id,),
        ).fetchone()

    return _row_to_prompt(row) if row else None


def get_prompts() -> list[Prompt]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM prompts
            ORDER BY conversation_id, prompt_number
            """
        ).fetchall()

    return [_row_to_prompt(r) for r in rows]


def prompts_by_category(category: str) -> list[Prompt]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT p.*
            FROM prompts p
            JOIN categories c
                ON p.category_id = c.category_id
            WHERE c.category_name = ?
            """,
            (category,),
        ).fetchall()

    return [_row_to_prompt(r) for r in rows]


def prompts_by_model(model: str) -> list[Prompt]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT p.*
            FROM prompts p
            JOIN models m
                ON p.model_id = m.model_id
            WHERE m.model_name = ?
            """,
            (model,),
        ).fetchall()

    return [_row_to_prompt(r) for r in rows]


def delete_prompt(prompt_id: int):
    with connect() as conn:
        conn.execute(
            """
            DELETE FROM prompts
            WHERE prompt_id = ?
            """,
            (prompt_id,),
        )


def update_expected_behaviour(prompt_id: int, behaviour: str):
    with connect() as conn:
        conn.execute(
            """
            UPDATE prompts
            SET expected_behaviour = ?
            WHERE prompt_id = ?
            """,
            (behaviour, prompt_id),
        )

