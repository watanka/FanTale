from __future__ import annotations
from typing import Set, Optional
import os

from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fantale.db")
engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def _ensure_sqlite_columns():
    """
    Best-effort column/table ensure for local SQLite dev.
    Safe to call multiple times.
    """
    from sqlalchemy import text

    try:
        with engine.begin() as conn:
            # stories table
            cols = conn.exec_driver_sql("PRAGMA table_info('stories')").all()
            names: Set[str] = {c[1] for c in cols}
            if "created_at" not in names:
                conn.exec_driver_sql("ALTER TABLE stories ADD COLUMN created_at TEXT")
            if "genre" not in names:
                conn.exec_driver_sql("ALTER TABLE stories ADD COLUMN genre TEXT")
            if "characters" not in names:
                conn.exec_driver_sql("ALTER TABLE stories ADD COLUMN characters TEXT")
            if "summary" not in names:
                conn.exec_driver_sql("ALTER TABLE stories ADD COLUMN summary TEXT")
            if "num_chapters" not in names:
                conn.exec_driver_sql(
                    "ALTER TABLE stories ADD COLUMN num_chapters INTEGER"
                )

            # chapters table
            cols = conn.exec_driver_sql("PRAGMA table_info('chapters')").all()
            names = {c[1] for c in cols}
            if "available_from" not in names:
                conn.exec_driver_sql(
                    "ALTER TABLE chapters ADD COLUMN available_from TEXT"
                )
            if "chapter_name" not in names:
                conn.exec_driver_sql(
                    "ALTER TABLE chapters ADD COLUMN chapter_name TEXT"
                )
            if "previous_summary" not in names:
                conn.exec_driver_sql(
                    "ALTER TABLE chapters ADD COLUMN previous_summary TEXT"
                )

            # chapter_plots table
            tables = {
                r[0]
                for r in conn.exec_driver_sql(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).all()
            }
            if "chapter_plots" not in tables:
                conn.exec_driver_sql(
                    "CREATE TABLE chapter_plots (\n"
                    " id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                    " story_id INTEGER NOT NULL REFERENCES stories(id) ON DELETE CASCADE,\n"
                    " chapter_number INTEGER NOT NULL,\n"
                    " content TEXT NOT NULL\n"
                    ")"
                )
    except Exception:
        # Best-effort only for dev
        pass


def init_db():
    """SQLite DB 초기화 및 컬럼 보완"""
    print("📦 Creating tables if not exist...")
    # Ensure all models are imported so SQLAlchemy knows them
    import app.db.models  # noqa: F401
    Base.metadata.create_all(bind=engine)

    print("🔍 Ensuring SQLite columns...")
    _ensure_sqlite_columns()

    print("✅ Database initialized.")


class BaseRepository:
    def save(self, model: Base) -> int:
        raise NotImplementedError

    def get(self, model_id: int) -> Optional[Base]:
        raise NotImplementedError
