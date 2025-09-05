from __future__ import annotations
from typing import Optional

from app.schemas.story import (
    StoryCreateRequest,
    StoryCreateResponse,
    StoryStatusResponse,
    StoryListResponse,
    StoryRetrieveResponse,
)
from app.services.mappers import (
    assemble_story_list_response,
    assemble_story_retrieve_response,
    story_state_to_model,
    chapterplot_item_to_model,
)
from app.db.models.story import StoryModel
from app.db.repository.story_repository import StoryRepository
from app.db.repository.chapter_plot_repository import ChapterPlotRepository
from app.db.repository.chapter_repository import ChapterRepository
from app.agents.graph import storyplan_graph, StoryPlanState


class StoryService:
    def __init__(self):
        # Use modular repositories
        self.story_repo = StoryRepository()
        self.plot_repo = ChapterPlotRepository()
        self.chapter_repo = ChapterRepository()

    def create_storyplan(self, req: StoryCreateRequest, story_id: str):
        # Generate full story plan (title, characters, summary, plots)
        # StoryParameter: num_chapters, idols, genre
        plan: StoryPlanState = storyplan_graph.invoke(
            {
                "genre": req.story_parameter.genre,
                "character_descriptions": req.story_parameter.idols,
                "story_plan": "",
                "cliche_feedback": "",
                "storyline_feedback": "",
                "character_feedback": "",
                "num_edits": 0,
            }
        )

        # mapper
        story_model = story_state_to_model(
            plan, story_id=story_id, user_id=req.user_id, status="PENDING"
        )

        # # Persist Story and ChapterPlot entries
        # story_model = story_item_to_model(
        #     plan,
        #     user_id=req.user_id,
        #     genre=req.story_parameter.genre,
        #     status="PENDING",
        # )
        self.story_repo.save(story_model)
        for item in plan["story_plan"].plots:
            self.plot_repo.save(chapterplot_item_to_model(story_id, item))

        # return StoryCreateResponse(story_id=story_id, status="PENDING")

    def get_status(self, story_id: str) -> StoryStatusResponse:
        story = self.story_repo.get(story_id)
        status = story.status if story else "NOT_FOUND"
        return StoryStatusResponse(status=status)

    def list_stories(self, user_id: int) -> StoryListResponse:
        models = self.story_repo.list_by_user(user_id)
        return assemble_story_list_response(models)

    def get_story(self, story_id: str) -> Optional[StoryRetrieveResponse]:
        story: StoryModel = self.story_repo.get(story_id)
        if not story:
            return None
        return assemble_story_retrieve_response(story)


story_service = StoryService()
