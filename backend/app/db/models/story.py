from __future__ import annotations
from typing import List, Optional
from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base


class StoryModel(Base):
    __tablename__ = "stories"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
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
