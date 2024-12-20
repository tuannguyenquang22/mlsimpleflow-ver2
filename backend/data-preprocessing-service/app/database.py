import aioredis
from app.config import REDIS_URL, PREPROCESSING_CHANNEL


redis_client = aioredis.from_url(REDIS_URL)
