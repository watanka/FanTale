from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, timezone, time as dtime
from typing import Optional

from app.services.mappers import (
    assemble_chapter_retrieve_response,
    chapter_state_to_model,
)
from app.db.repository.story_repository import StoryRepository
from app.db.repository.chapter_plot_repository import ChapterPlotRepository
from app.db.repository.chapter_repository import ChapterRepository
from app.agents.graph import chapter_graph


from app.schemas.story import (
    StoryChapterRetrieveResponse,
    ChapterFeedbackRequest,
    ChapterFeedbackResponse,
)

TZ = ZoneInfo("Asia/Seoul")
RELEASE_AT = dtime(hour=9, minute=0)
CHAPTERS_PER_DAY = 3


class ChapterService:
    def __init__(self):
        self.story_repo = StoryRepository()
        self.plot_repo = ChapterPlotRepository()
        self.chapter_repo = ChapterRepository()

    def create_chapter(self, story_id: int):
        try:

            story = self.story_repo.get(story_id)
            chapter_plots = self.plot_repo.list_by_story(story_id)

            genre = story.genre
            title = story.title
            character_descriptions = story.characters
            total_summary = story.summary

            created_at = getattr(story, "created_at", None)
            if created_at is None:
                created_utc = datetime.now(tz=timezone.utc)
            else:
                created_utc = (
                    created_at.replace(tzinfo=timezone.utc)
                    if created_at.tzinfo is None
                    else created_at.astimezone(timezone.utc)
                )
            created_kst = created_utc.astimezone(TZ)
            base_09_kst = created_kst.replace(
                hour=RELEASE_AT.hour, minute=RELEASE_AT.minute, second=0, microsecond=0
            )
            base_release_kst = created_kst if created_kst > base_09_kst else base_09_kst

            previous_summary = ""
            for plot in chapter_plots:
                day_index = (plot.chapter_number - 1) // CHAPTERS_PER_DAY
                available_kst = base_release_kst + timedelta(days=day_index)
                available_utc = available_kst.astimezone(timezone.utc)

                chapter_state = chapter_graph.invoke(
                    {
                        "genre": genre,
                        "title": title,
                        "character_descriptions": character_descriptions,
                        "previous_summary": previous_summary,
                        "chapter_plot": plot.content,
                        "total_summary": total_summary,
                        "content": "",
                        "cliche_feedback": "",
                        "detail_feedback": "",
                        "novelist_feedback": "",
                        "num_edits": 0,
                    }
                )
                self.plot_repo.update(
                    plot.id, previous_summary=chapter_state["previous_summary"]
                )
                chapter_db_model = chapter_state_to_model(
                    story_id, plot.chapter_number, chapter_state, available_utc
                )
                self.chapter_repo.save(chapter_db_model)
                previous_summary = chapter_state["previous_summary"]
            self.story_repo.update(story_id, status="READY")
        except Exception:
            self.story_repo.update(story_id, status="FAILED")

    def get_chapter(self, chapter_id: int) -> Optional[StoryChapterRetrieveResponse]:
        # Story ID is not used in current repository API; kept for compatibility.
        chapter = self.chapter_repo.get(chapter_id)
        if not chapter:
            return None
        return assemble_chapter_retrieve_response(chapter)

    # feedback 구현 필요
    def add_feedback(
        self, chapter_id: int, req: ChapterFeedbackRequest
    ) -> Optional[ChapterFeedbackResponse]:
        # No persistence for MVP. Validate story exists.
        if not self.chapter_repo.get(chapter_id):
            return None
        # For MVP, we just echo back.
        return ChapterFeedbackResponse(
            chapter_id=req.chapter_id, feedback=req.feedback_text
        )


chapter_service = ChapterService()
