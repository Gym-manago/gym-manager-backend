"""
This file is responsible for handling the login route.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import SessionDep
from app.schemas.user import UserSchema, UserModelResponse, LoginResponse
from app.utils.login import hash_password, authenticate_user, create_access_token
from datetime import timedelta
from app.settings.base import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid credentials!"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        username=user.username,
        email=user.email,
    )


@router.post("/sign-up", response_model=UserModelResponse)
def signup(payload: UserSchema, session: SessionDep):
    hashed_password = hash_password(password=payload.password)
    user = UserSchema(
        username=payload.username, email=payload.email, password=hashed_password
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
