from __future__ import annotations
from typing import List, Dict, Optional

from app.db.models import StoryModel, ChapterPlotModel, ChapterModel

class FakeStoryRepository:
    """
    Lightweight helper to seed and read data through real repositories
    without coupling tests to XML or external inputs.
    """
    def __init__(self):
        self.stories: Dict[int, StoryModel] = {}

    def save(
        self,
        story: StoryModel
    ) -> int:
        story_id = len(self.stories) + 1
        self.stories[story_id] = story
        return story_id

    def get(self, story_id: int) -> Optional[StoryModel]:
        return self.stories.get(story_id)


class FakeChapterPlotRepository:
    def __init__(self):
        self.plots: Dict[int, ChapterPlotModel] = {}

    def save(self, plot: ChapterPlotModel) -> int:
        plot_id = len(self.plots) + 1
        self.plots[plot_id] = plot
        return plot_id

    def get(self, plot_id: int) -> Optional[ChapterPlotModel]:
        return self.plots.get(plot_id)

    def list_by_story(self, story_id: int) -> List[ChapterPlotModel]:
        return [plot for plot in self.plots.values() if plot.story_id == story_id]

class FakeChapterRepository:
    def __init__(self):
        self.chapters: Dict[int, ChapterModel] = {}
    
    def save(self, chapter: ChapterModel) -> int:
        chapter_id = len(self.chapters) + 1
        self.chapters[chapter_id] = chapter
        return chapter_id
    
    def get(self, chapter_id: int) -> Optional[ChapterModel]:
        return self.chapters.get(chapter_id)