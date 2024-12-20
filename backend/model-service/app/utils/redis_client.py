import aioredis
from app.core.config import REDIS_URL


redis_client = aioredis.from_url(REDIS_URL)