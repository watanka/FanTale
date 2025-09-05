from app.db.models import ChapterModel
from app.db.repository.base import BaseRepository
from app.db.models.base import SessionLocal
from typing import Optional


class ChapterRepository(BaseRepository):
    def __init__(self):
        self.db = SessionLocal()

    def save(self, chapter: ChapterModel) -> int:
        self.db.add(chapter)
        self.db.commit()
        self.db.refresh(chapter)
        return chapter.id

    def get(self, chapter_id: int) -> Optional[ChapterModel]:
        return self.db.get(ChapterModel, chapter_id)
