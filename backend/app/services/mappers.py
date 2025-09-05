from __future__ import annotations
from typing import List, Optional
from datetime import datetime, timezone

from app.schemas.story import (
    Chapter,
    Story,
    StoryListResponse,
    StoryRetrieveResponse,
    StoryChapterRetrieveResponse,
)
from app.agents.story.model import StoryPlan, ChapterPlotItem, Character
from app.agents.chapter.model import ChapterOutput
from app.agents.graph import StoryPlanState, ChapterState
from app.db.models.story import StoryModel
from app.db.models.chapter import ChapterModel
from app.db.models.chapterplot import ChapterPlotModel


def map_chapter(ch: ChapterModel) -> Chapter:
    def _to_iso(dt: datetime | None) -> str | None:
        if dt is None:
            return None
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()

    return Chapter(
        chapter_id=ch.id,
        chapter_number=ch.chapter_number,
        chapter_name=ch.chapter_name,
        summary="",
        content=ch.content,
        available_from=_to_iso(getattr(ch, "available_from", None)),
    )


def map_story(st: StoryModel) -> Story:
    chapters = [map_chapter(c) for c in st.chapters]
    return Story(story_id=st.id, title=st.title, summary=st.summary, chapters=chapters)


def assemble_story_list_response(items: List[StoryModel]) -> StoryListResponse:
    stories = [map_story(s) for s in items]
    return StoryListResponse(stories=stories)


def assemble_story_retrieve_response(st: StoryModel) -> StoryRetrieveResponse:
    chapters = [map_chapter(c) for c in st.chapters]
    return StoryRetrieveResponse(
        story_id=st.id, title=st.title, summary=st.summary, chapters=chapters
    )


def assemble_chapter_retrieve_response(
    ch: ChapterModel,
) -> StoryChapterRetrieveResponse:
    return StoryChapterRetrieveResponse(chapter=map_chapter(ch))


# ---- LLM <-> ORM Mappers ----


def story_state_to_model(
    plan: StoryPlanState,
    story_id: str,
    user_id: int,
    status: str = "PENDING",
) -> StoryModel:
    return StoryModel(
        id=story_id,
        user_id=user_id,
        title=plan["story_plan"].title,
        status=status,
        genre=plan["genre"],
        characters="\n".join(
            [f"{c.name}: {c.description}" for c in plan["story_plan"].characters]
        ),
        summary=plan["story_plan"].summary,
        num_chapters=plan["story_plan"].num_chapters,
    )


def story_item_to_model(
    plan: StoryPlan,
    user_id: int,
    genre: Optional[str] = None,
    status: str = "PENDING",
) -> StoryModel:
    return StoryModel(
        user_id=user_id,
        title=plan.title,
        status=status,
        genre=genre,
        characters="\n".join([f"{c.name}: {c.description}" for c in plan.characters]),
        summary=plan.summary,
        num_chapters=plan.num_chapters,
    )


def story_model_to_item(story: StoryModel, plots: List[ChapterPlotModel]) -> StoryPlan:
    return StoryPlan(
        title=story.title,
        characters=[
            Character(name=name, description=description)
            for name, description in story.characters.split("\n")
        ],
        summary=story.summary or "",
        num_chapters=story.num_chapters or len(plots),
        plots=[
            chapter_plot_model_to_item(p)
            for p in sorted(plots, key=lambda x: x.chapter_number)
        ],
    )


def chapterplot_item_to_model(story_id: str, item: ChapterPlotItem) -> ChapterPlotModel:
    return ChapterPlotModel(
        story_id=story_id,
        chapter_number=item.chapter_number,
        content=item.content,
    )


def chapter_plot_model_to_item(model: ChapterPlotModel) -> ChapterPlotItem:
    return ChapterPlotItem(chapter_number=model.chapter_number, content=model.content)


def chapter_state_to_model(
    story_id: str,
    chapter_number: int,
    chapter: ChapterState,
    available_from: Optional[datetime] = None,
) -> ChapterModel:
    return ChapterModel(
        story_id=story_id,
        chapter_number=chapter_number,
        chapter_name=chapter["title"],
        content=chapter["content"],
        available_from=available_from,
    )


def chapter_model_to_chapter_output(model: ChapterModel) -> ChapterOutput:
    return ChapterOutput(
        previous_summary=model.previous_summary or "",
        chapter_name=model.chapter_name or "",
        content=model.content or "",
    )
