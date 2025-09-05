from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import sessionmaker
from app.db.models import SessionLocal


class BaseRepository:
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory
