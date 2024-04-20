from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from fastapi.security import OAuth2PasswordRequestForm

from auth.Auth import Token, authenticate_user, create_access_token, read_users_db

ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()

@router.post("/token", tags=["auth"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(read_users_db(), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")