from __future__ import annotations

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .story import StoryModel


class ChapterPlotModel(Base):
    __tablename__ = "chapter_plots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    story_id: Mapped[int] = mapped_column(
        ForeignKey("stories.id", ondelete="CASCADE"),
        index=True,
    )
    chapter_number: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(String)
    previous_summary: Mapped[str | None] = mapped_column(String, nullable=True)

    story: Mapped[StoryModel] = relationship(back_populates="plots")