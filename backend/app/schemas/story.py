from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


# ---- Requests ----
class StoryParameter(BaseModel):
    num_chapters: int = Field(ge=1, le=50)
    idols: str
    genre: str  # backend may later switch to enum


class StoryCreateRequest(BaseModel):
    user_id: int
    story_parameter: StoryParameter


class StoryListRequest(BaseModel):
    user_id: int


class StoryRetrieveRequest(BaseModel):
    story_id: str


class ChapterRetrieveRequest(BaseModel):
    chapter_id: int


class ChapterFeedbackRequest(BaseModel):
    chapter_id: int
    feedback_text: str
    like: bool


# ---- Core Resources ----
class Chapter(BaseModel):
    chapter_id: int
    chapter_number: int
    chapter_name: str
    summary: str
    content: str
    available_from: Optional[str] = None


class Story(BaseModel):
    story_id: str
    title: str
    summary: str
    chapters: List[Chapter]


# ---- Responses ----
class StoryCreateResponse(BaseModel):
    story_id: str
    status: str


class StoryStatusResponse(BaseModel):
    status: str


class StoryListResponse(BaseModel):
    stories: List[Story]


class StoryRetrieveResponse(BaseModel):
    story_id: str
    title: str
    summary: str
    chapters: List[Chapter]


class StoryChapterRetrieveResponse(BaseModel):
    chapter: Chapter


class ChapterFeedbackResponse(BaseModel):
    chapter_id: int
    feedback: str


class StoryShareResponse(BaseModel):
    story_id: str


class FandomListResponse(BaseModel):
    fandoms: List[Story]
