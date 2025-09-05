from app.celery_app import celery
from app.services.chapter_service import chapter_service


@celery.task(name="generate_chapters")
def generate_chapters_task(story_id: str) -> None:
    chapter_service.create_chapter(story_id)
