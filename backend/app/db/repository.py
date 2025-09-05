from __future__ import annotations
from typing import List, Optional
from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
    selectinload,
)
from sqlalchemy import create_engine, select


# --- SQLAlchemy setup ---
class Base(DeclarativeBase):
    pass


engine = create_engine(
    "sqlite:///./fantale.db",
    echo=False,
    future=True,
)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


# --- Models ---
class StoryModel(Base):
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    title: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(32), index=True)
    # New fields for DB-first generation flow
    genre: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    characters: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # overall
    num_chapters: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    chapters: Mapped[List["ChapterModel"]] = relationship(
        back_populates="story",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    plots: Mapped[List["ChapterPlotModel"]] = relationship(
        back_populates="story",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class ChapterModel(Base):
    __tablename__ = "chapters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    story_id: Mapped[int] = mapped_column(
        ForeignKey("stories.id", ondelete="CASCADE"),
        index=True,
    )
    chapter_number: Mapped[int] = mapped_column(Integer)
    # Backward-compat fields kept but we prefer the new names
    title: Mapped[str] = mapped_column(String(255))                      # deprecated alias of chapter_name
    summary: Mapped[str] = mapped_column(String)                         # deprecated alias of previous_summary
    # New preferred fields
    chapter_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    previous_summary: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    content: Mapped[str] = mapped_column(String)
    available_from: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    story: Mapped[StoryModel] = relationship(back_populates="chapters")


class ChapterPlotModel(Base):
    __tablename__ = "chapter_plots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    story_id: Mapped[int] = mapped_column(
        ForeignKey("stories.id", ondelete="CASCADE"),
        index=True,
    )
    chapter_number: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(String)

    story: Mapped[StoryModel] = relationship(back_populates="plots")


# Create tables on import for MVP
Base.metadata.create_all(bind=engine)


# --- Lightweight SQLite column ensure for dev ---
def _ensure_sqlite_columns():
    try:
        with engine.begin() as conn:
            # stories.created_at
            cols = conn.exec_driver_sql("PRAGMA table_info('stories')").all()
            names = {c[1] for c in cols}
            if "created_at" not in names:
                conn.exec_driver_sql("ALTER TABLE stories ADD COLUMN created_at TEXT")
            if "genre" not in names:
                conn.exec_driver_sql("ALTER TABLE stories ADD COLUMN genre TEXT")
            if "characters" not in names:
                conn.exec_driver_sql("ALTER TABLE stories ADD COLUMN characters TEXT")
            if "summary" not in names:
                conn.exec_driver_sql("ALTER TABLE stories ADD COLUMN summary TEXT")
            if "num_chapters" not in names:
                conn.exec_driver_sql("ALTER TABLE stories ADD COLUMN num_chapters INTEGER")
            # chapters.available_from
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
            tables = {r[0] for r in conn.exec_driver_sql("SELECT name FROM sqlite_master WHERE type='table'").all()}
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


_ensure_sqlite_columns()


# --- Repository ---
class StoryRepository:
    """CRUD for StoryModel. Single responsibility: story aggregate root."""

    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    def save(
        self,
        *,
        user_id: int,
        title: str,
        status: str = "PENDING",
        genre: Optional[str] = None,
        characters: Optional[str] = None,
        summary: Optional[str] = None,
        num_chapters: Optional[int] = None,
    ) -> int:
        with self._session_factory() as session:
            story = StoryModel(
                user_id=user_id,
                title=title,
                status=status,
                genre=genre,
                characters=characters,
                summary=summary,
                num_chapters=num_chapters,
            )
            session.add(story)
            session.commit()
            session.refresh(story)
            return story.id

    def update_status(self, story_id: int, status: str) -> None:
        with self._session_factory() as session:
            story = session.get(StoryModel, story_id)
            if not story:
                return
            story.status = status
            session.commit()

    def get(self, story_id: int) -> Optional[StoryModel]:
        with self._session_factory() as session:
            return session.get(StoryModel, story_id)

    def get_with_children(self, story_id: int) -> Optional[StoryModel]:
        with self._session_factory() as session:
            stmt = (
                select(StoryModel)
                .options(selectinload(StoryModel.chapters), selectinload(StoryModel.plots))
                .where(StoryModel.id == story_id)
            )
            return session.execute(stmt).scalars().first()

    def list_by_user(self, user_id: int) -> List[StoryModel]:
        with self._session_factory() as session:
            stmt = (
                select(StoryModel)
                .options(selectinload(StoryModel.chapters))
                .where(StoryModel.user_id == user_id)
            )
            return session.execute(stmt).scalars().all()

    def get_status(self, story_id: int) -> Optional[str]:
        with self._session_factory() as session:
            story = session.get(StoryModel, story_id)
            return story.status if story else None


class ChapterRepository:
    """CRUD for ChapterModel."""

    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    def save(
        self,
        *,
        story_id: int,
        chapter_number: int,
        chapter_name: str,
        previous_summary: str,
        content: str,
        available_from: Optional[datetime] = None,
    ) -> int:
        with self._session_factory() as session:
            story = session.get(StoryModel, story_id)
            if not story:
                raise ValueError("Story not found")
            ch = ChapterModel(
                story_id=story_id,
                chapter_number=chapter_number,
                # keep legacy fields in sync
                title=chapter_name,
                summary=previous_summary,
                chapter_name=chapter_name,
                previous_summary=previous_summary,
                content=content,
                available_from=available_from,
            )
            session.add(ch)
            session.commit()
            session.refresh(ch)
            return ch.id

    def get(self, story_id: int, chapter_id: int) -> Optional[ChapterModel]:
        with self._session_factory() as session:
            stmt = select(ChapterModel).where(
                ChapterModel.id == chapter_id,
                ChapterModel.story_id == story_id,
            )
            return session.execute(stmt).scalars().first()


class ChapterPlotRepository:
    """CRUD for ChapterPlotModel (aka chapter summaries/plots)."""

    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    def save(self, *, story_id: int, chapter_number: int, content: str) -> int:
        with self._session_factory() as session:
            story = session.get(StoryModel, story_id)
            if not story:
                raise ValueError("Story not found")
            plot = ChapterPlotModel(
                story_id=story_id,
                chapter_number=chapter_number,
                content=content,
            )
            session.add(plot)
            session.commit()
            session.refresh(plot)
            return plot.id

    def list_by_story(self, story_id: int) -> List[ChapterPlotModel]:
        with self._session_factory() as session:
            stmt = select(ChapterPlotModel).where(ChapterPlotModel.story_id == story_id)
            return session.execute(stmt).scalars().all()


story_repository = StoryRepository(SessionLocal)
chapter_repository = ChapterRepository(SessionLocal)
summary_repository = ChapterPlotRepository(SessionLocal)
