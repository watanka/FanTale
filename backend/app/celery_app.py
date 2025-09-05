from __future__ import annotations
from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery = Celery(
    "fantale",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.story_tasks",
        "app.tasks.chapter_tasks",
    ],
)

# Basic configuration
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=settings.CELERY_TIMEZONE,
    enable_utc=True,
    task_ignore_result=False,
)
