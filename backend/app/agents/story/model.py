from pydantic import BaseModel, Field
from typing import List


class ChapterPlotItem(BaseModel):
    chapter_number: int = Field(..., ge=1, description="챕터 번호(1부터)")
    content: str


class Character(BaseModel):
    name: str
    description: str

    def to_str(self):
        return f"{self.name}: {self.description}"


class StoryPlan(BaseModel):
    title: str
    characters: List[Character]
    summary: str  # 전체 줄거리
    num_chapters: int = Field(..., ge=1, description="총 챕터 수")
    plots: List[ChapterPlotItem] = Field(..., min_items=1)

    def to_str(self):
        return (
            f"Title: {self.title}"
            + "\n"
            + f"Characters: {', '.join([c.to_str() for c in self.characters])}"
            + f"\nSummary: {self.summary}\nNum Chapters: {self.num_chapters}\nPlots: {self.plots}"
        )


class FeedBack(BaseModel):
    score: int
    reasoning: str


class StoryPlanFeedBack(BaseModel):
    cliche_feedback: FeedBack
    storyline_feedback: FeedBack
    character_feedback: FeedBack
