from fastapi import APIRouter
from app.api.api_v1.endpoints import(
    users,
    login,
    dataset,
    training,
)
api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(dataset.router, prefix="/dataset", tags=["dataset"])
api_router.include_router(training.router, prefix="/model", tags=["model"])