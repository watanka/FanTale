from .base import Base, engine, SessionLocal, _ensure_sqlite_columns
# Import models to register tables
from .story import StoryModel  # noqa: F401
from .chapter import ChapterModel  # noqa: F401
from .chapterplot import ChapterPlotModel  # noqa: F401
from .user import UserModel  # noqa: F401

# Create tables and ensure columns on import
Base.metadata.create_all(bind=engine)
_ensure_sqlite_columns()
