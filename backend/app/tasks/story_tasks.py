from app.celery_app import celery
from app.services.story_service import story_service
from app.schemas.story import StoryCreateRequest
import uuid


@celery.task(name="generate_story")
def generate_story_task(req_json: str, story_id: str) -> dict:
    req = StoryCreateRequest.model_validate_json(req_json)
    story_service.create_storyplan(req, story_id)

    return {"story_id": story_id}
