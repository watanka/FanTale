from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import httpx
from app.core.config import get_settings
from app.schemas.auth import (
    LogoutRequest,
    LogoutResponse,
)
from app.db.models import SessionLocal
from app.db.models.user import UserModel

router = APIRouter()


@router.post("/logout", response_model=LogoutResponse)
async def logout(payload: LogoutRequest) -> LogoutResponse:
    # Revoke tokens with provider if possible
    if payload.provider == "google":
        revoke_url = "https://oauth2.googleapis.com/revoke"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient() as client:
            for token in [payload.access_token, payload.refresh_token, payload.id_token]:
                if not token:
                    continue
                try:
                    await client.post(revoke_url, data={"token": token}, headers=headers)
                except Exception:
                    # Ignore revocation errors to not block logout UX
                    pass
    return LogoutResponse(status="ok")

@router.get("/google/login")
def login():
    settings = get_settings()
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        "&scope=openid%20email%20profile"
        "&access_type=offline"
        "&prompt=consent"
    )
    return RedirectResponse(google_auth_url)


@router.get("/google/callback")
async def auth_callback(code: str):
    settings = get_settings()
    token_url = "https://oauth2.googleapis.com/token"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            token_url,
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_data = resp.json()
        print("token_data: ", token_data)
        if "error" in token_data:
            raise HTTPException(status_code=400, detail=token_data["error"])

        id_token = token_data.get("id_token")
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")

        # id_token 검증 및 사용자 정보 추출
        user_info_resp = await client.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            params={"alt": "json", "access_token": access_token},
        )
        user_info = user_info_resp.json()

    # DB upsert: 사용자 생성 또는 업데이트
    email = user_info.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email not present in Google user info")

    session = SessionLocal()
    is_new = False
    try:
        user = session.query(UserModel).filter(UserModel.email == email).first()
        if user is None:
            user = UserModel(
                email=email,
                name=user_info.get("name"),
                picture=user_info.get("picture"),
                provider="google",
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            is_new = True
        else:
            updated = False
            name = user_info.get("name")
            picture = user_info.get("picture")
            if name and name != user.name:
                user.name = name
                updated = True
            if picture and picture != user.picture:
                user.picture = picture
                updated = True
            if updated:
                session.commit()
                session.refresh(user)
    finally:
        session.close()

    return {
        "id_token": id_token,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_info": user_info,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "picture": user.picture,
            "provider": user.provider,
        },
        "is_new": is_new,
    }