from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_DATABASE_URL, DATABASE_NAME

client = AsyncIOMotorClient(MONGO_DATABASE_URL)
db = client[DATABASE_NAME]

