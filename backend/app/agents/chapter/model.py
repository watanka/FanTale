from pydantic import BaseModel


class ChapterOutput(BaseModel):
    previous_summary: str
    chapter_name: str
    content: str


class FeedBack(BaseModel):
    score: int
    reasoning: str


class ChapterFeedBack(BaseModel):
    cliche_feedback: FeedBack
    detail_feedback: FeedBack
    novelist_feedback: FeedBack
