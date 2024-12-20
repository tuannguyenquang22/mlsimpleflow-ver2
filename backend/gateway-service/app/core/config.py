from typing import Any
import os
from pydantic_settings import BaseSettings
import secrets
from dotenv import load_dotenv


load_dotenv()


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 30
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 30 * 24 * 30
    JWT_ALGO: str = "HS512"
    TOTP_ALGO: str = "SHA-1"
    ALLOWED_HOSTS: str = os.getenv("ALLOWED_HOSTS")
    MONGO_DATABASE: str = "mlsimpleflow_gateway"
    MONGO_DATABASE_URL: str = os.getenv("MONGO_DATABASE_URL")
    DATASET_SERVICE_URL: str = os.getenv("DATASET_SERVICE_URL")
    MODEL_SERVICE_URL: str = os.getenv("MODEL_SERVICE_URL")
    MULTI_MAX: int = 20


settings = Settings()