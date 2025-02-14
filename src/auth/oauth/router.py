from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse

from src.auth.oauth.github import (
    get_github_auth_url, 
    exchange_code_for_token, 
    get_github_user
)
from src.users.dao import UserDAO
from src.auth.jwt.jwt_auth import create_access_token, create_refresh_token


router = APIRouter(
    prefix="/oauth", 
    tags=["Oauth"]
)


@router.get("/github/login")
async def github_login():
    return RedirectResponse(get_github_auth_url())


@router.get("/github/callback")
async def github_callback(request: Request, response: Response):
    code = request.query_params.get("code")
    if not code:
        return {
            "error": "Authorization failed"
        }

    token = await exchange_code_for_token(code)
    user_data = await get_github_user(token)

    email = user_data.get("email")
    if not email:
        email = f"{user_data['id']}@github.com"

    existing_user = await UserDAO.find_one_or_none(email=email)

    if not existing_user:
        await UserDAO.add(
            email=email,
            login=user_data["login"],
            hashed_password="github_auth",
        )
        existing_user = await UserDAO.find_one_or_none(email=email)

    access_token = create_access_token({"sub": str(existing_user.id)})
    refresh_token = create_refresh_token({"sub": str(existing_user.id)})

    response.set_cookie(
        key="refer_access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        secure=False,
        path="/",
    )
    response.set_cookie(
        key="refer_refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="Lax",
        secure=False,
        path="/",
    )

    return {
        "message": "Успешная аутентификация",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": existing_user.id,
            "email": existing_user.email,
            "login": existing_user.login
        }
    }
