from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.include_router(api_router, prefix=settings.API_V1_STR)
    yield

app: FastAPI = FastAPI(lifespan=lifespan)


from fastapi.middleware.cors import CORSMiddleware


origins = [
    settings.ALLOWED_HOSTS,
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)