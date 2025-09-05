from app.db.models import ChapterPlotModel
from app.db.repository.base import BaseRepository
from app.db.models.base import SessionLocal
from typing import Optional, List
from sqlalchemy import select

class ChapterPlotRepository(BaseRepository):
    def __init__(self):
        self.db = SessionLocal()
    
    def save(self, plot: ChapterPlotModel) -> int:
        self.db.add(plot)
        self.db.commit()
        self.db.refresh(plot)
        return plot.id
    
    def get(self, plot_id: int) -> Optional[ChapterPlotModel]:
        return self.db.get(ChapterPlotModel, plot_id)

    def list_by_story(self, story_id: int) -> List[ChapterPlotModel]:
        stmt = select(ChapterPlotModel).where(ChapterPlotModel.story_id == story_id)
        return self.db.execute(stmt).scalars().all()
        
    def update(self, plot_id: int, **kwargs) -> None:
        plot = self.get(plot_id)
        for key, value in kwargs.items():
            setattr(plot, key, value)
        self.db.commit()
        self.db.refresh(plot)