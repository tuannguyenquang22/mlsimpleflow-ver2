import aioredis
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_DATABASE_URL, DATABASE_NAME, REDIS_URL, PREPROCESSING_CHANNEL


client = AsyncIOMotorClient(MONGO_DATABASE_URL)
db = client[DATABASE_NAME]

redis_client = aioredis.from_url(REDIS_URL)