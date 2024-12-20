from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException
from motor.core import AgnosticDatabase
from pydantic import EmailStr
from app.api import deps
from app import crud, schemas, models
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=schemas.User)
async def create_user_profile(
    *,
    db: AgnosticDatabase = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    display_name: str = Body("")
) -> Any:
    user = await crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="This email is not available."
        )
    user_in = schemas.UserCreate(password=password, email=email, display_name=display_name)
    user = await crud.user.create(db, obj_in=user_in)
    return user


@router.get("/email/{user_id}")
async def get_user_email(
    *,
    db: AgnosticDatabase = Depends(deps.get_db),
    user_id: str,
    key: str,
):
    if key != "FROM_NOTIFY_20200563":
        raise HTTPException(status_code=400, detail="Invalid key")

    user = await crud.user.get(db, id=ObjectId(user_id))
    return user.email

@router.get("/me", response_model=schemas.User)
async def read_user(
    *,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user