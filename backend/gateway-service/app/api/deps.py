from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from motor.core import AgnosticDatabase
from pydantic import ValidationError
from app import schemas, models, crud
from app.core.config import settings
from app.db.session import MongoDatabase


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/oauth")


def get_db() -> Generator:
    try:
        db = MongoDatabase()
        yield db
    finally:
        pass


def get_token_payload(token: str) -> schemas.TokenPayload:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGO])
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    return token_data


async def get_current_user(
    db: AgnosticDatabase = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    token_data = get_token_payload(token)
    if token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_refresh_user(
    db: AgnosticDatabase = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    token_data = get_token_payload(token)
    if not token_data.refresh:
        # Access token is not a valid refresh token
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    # Check and revoke this refresh token
    token_obj = await crud.token.get(token=token, user=user)
    if not token_obj:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    await crud.token.remove(db, db_obj=token_obj)
    # Make sure to revoke all other refresh tokens
    return await crud.user.get(id=token_data.sub)