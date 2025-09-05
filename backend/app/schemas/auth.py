from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr



class LogoutRequest(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    provider: str = "google"


class LogoutResponse(BaseModel):
    status: str = "ok"
