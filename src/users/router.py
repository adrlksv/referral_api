from fastapi import APIRouter, Request, Response, Depends

from src.auth.jwt.jwt_auth import (
    authenticate_user, 
    create_access_token,
    create_refresh_token, 
    get_password_hash
)
from src.auth.jwt.dependencies import get_current_user
from src.users.schemas import SUserRegister, SUserLogin
from src.users.dao import UserDAO
from src.users.models import User

from src.exceptions import (
    UserAlreadyExistsException, 
    IncorrectEmailOrPasswordException, 
    TokenAbsentException
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
async def register_user(user_data: SUserRegister):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(
        email=user_data.email,
        login=user_data.login,
        hashed_password=hashed_password
    )


@router.post("/login")
async def login_user(response: Response, user_data: SUserLogin):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    response.set_cookie(
        "refer_access_token",
        access_token,
        httponly=True,
        samesite="strict",
    )
    response.set_cookie(
        "refer_refresh_token",
        refresh_token,
        httponly=True,
        samesite="strict"
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.post("/refresh")
async def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refer_refresh_token")
    if not refresh_token:
        raise TokenAbsentException
    
    user = await get_current_user(refresh_token)
    new_access_token = create_access_token({"sub": str(user.id)})

    response.set_cookie(
        "refer_access_token",
        new_access_token,
        httponly=True,
        samesite="strict"
    )

    return {
        "access_token": new_access_token
    }


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("refer_access_token")
    response.delete_cookie("refer_refresh_token")


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
