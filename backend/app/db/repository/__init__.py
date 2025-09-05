from app.db.models import SessionLocal
from .story_repository import StoryRepository
from .chapter_repository import ChapterRepository
from .chapter_plot_repository import ChapterPlotRepository

# Expose repository singletons (keeps backwards compatibility)
story_repository = StoryRepository()
chapter_repository = ChapterRepository()
summary_repository = ChapterPlotRepository()
