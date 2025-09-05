from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.models.base import init_db
from app.api.routes.auth import router as auth_router
from app.api.routes.stories import router as stories_router

app = FastAPI(title="FanTale API", version="0.1.0")

init_db()

# CORS (development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Limit this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(stories_router, prefix="", tags=["stories"])
