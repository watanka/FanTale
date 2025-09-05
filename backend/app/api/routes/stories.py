from typing import Optional
from fastapi import APIRouter, HTTPException
import uuid
from app.schemas.story import (
    StoryCreateRequest,
    StoryCreateResponse,
    StoryStatusResponse,
    StoryListResponse,
    StoryRetrieveResponse,
    StoryChapterRetrieveResponse,
    ChapterFeedbackRequest,
    ChapterFeedbackResponse,
    StoryShareResponse,
    FandomListResponse,
)

from celery import chain
from app.services.story_service import story_service
from app.services.chapter_service import chapter_service
from app.tasks.story_tasks import generate_story_task
from app.tasks.chapter_tasks import generate_chapters_task

router = APIRouter()


@router.post("/stories", response_model=StoryCreateResponse)
def create_story(req: StoryCreateRequest) -> StoryCreateResponse:
    story_id = str(uuid.uuid4())
    task_chain = chain(
        generate_story_task.si(req.model_dump_json(), story_id)
        | generate_chapters_task.si(story_id)
    )
    task_chain.delay()
    return StoryCreateResponse(story_id=story_id, status="PENDING")


@router.get("/stories/{story_id}/status", response_model=StoryStatusResponse)
def get_story_status(story_id: str) -> StoryStatusResponse:
    return story_service.get_status(story_id)


@router.get("/users/stories", response_model=StoryListResponse)
def list_user_stories(user_id: int) -> StoryListResponse:
    return story_service.list_stories(user_id)


@router.get("/stories/{story_id}", response_model=StoryRetrieveResponse)
def get_story(story_id: str) -> StoryRetrieveResponse:
    res = story_service.get_story(story_id)
    if not res:
        raise HTTPException(status_code=404, detail="Story not found")
    return res


@router.get(
    "/stories/{story_id}/chapter/{chapter_id}",
    response_model=StoryChapterRetrieveResponse,
)
def get_chapter(story_id: str, chapter_id: int) -> StoryChapterRetrieveResponse:
    res = chapter_service.get_chapter(chapter_id)
    if not res:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return res


@router.post(
    "/stories/{story_id}/chapter/{chapter_id}/feedback",
    response_model=ChapterFeedbackResponse,
)
def submit_chapter_feedback(
    story_id: str, chapter_id: int, feedback_text: str, like: bool
) -> ChapterFeedbackResponse:
    req = ChapterFeedbackRequest(
        chapter_id=chapter_id, feedback_text=feedback_text, like=like
    )
    res = chapter_service.add_feedback(chapter_id, req)
    if not res:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return res


@router.post("/stories/{story_id}/share", response_model=StoryShareResponse)
def share_story(story_id: str) -> StoryShareResponse:
    # MVP: no-op share that just acknowledges
    return StoryShareResponse(story_id=story_id)


@router.get("/fandoms", response_model=FandomListResponse)
def list_fandoms() -> FandomListResponse:
    # MVP: use all stories as sample fandoms
    stories = story_service.list_stories(user_id=-1).stories  # empty by default
    return FandomListResponse(fandoms=stories)
