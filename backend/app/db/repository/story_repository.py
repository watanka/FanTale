from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, selectinload

from app.db.repository.base import BaseRepository
from app.db.models.story import StoryModel
from app.db.models.base import SessionLocal
from sqlalchemy import select

class StoryRepository(BaseRepository):
    """CRUD for StoryModel. Single responsibility: story aggregate root."""

    def __init__(self):
        self.db = SessionLocal()

    # Backwards-compatible kwargs API used by tests
    def save(
        self,
        story: StoryModel,
    ) -> int:
        self.db.add(story)
        self.db.commit()
        self.db.refresh(story)
        return story.id

    # Optional helper when a model instance already exists
    def save_model(self, story: StoryModel) -> int:
        self.db.add(story)
        self.db.commit()
        self.db.refresh(story)
        return story.id

    def update(self, story_id: int, **kwargs) -> None:
        story = self.db.get(StoryModel, story_id)
        if not story:
            return
        for key, value in kwargs.items():
            setattr(story, key, value)
        self.db.commit()

    def get(self, story_id: int) -> Optional[StoryModel]:
        return self.db.get(StoryModel, story_id)

    def list_by_user(self, user_id: int) -> List[StoryModel]:
        stmt = (
            select(StoryModel)
            .options(selectinload(StoryModel.chapters))
            .where(StoryModel.user_id == user_id)
        )
        return self.db.execute(stmt).scalars().all()