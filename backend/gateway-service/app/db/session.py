from odmantic import AIOEngine
from pymongo.driver_info import DriverInfo
from motor.motor_asyncio import AsyncIOMotorClient
from motor import core
from app.core.config import settings


DRIVER_INFO = DriverInfo(name="mlsimpleflow_api_gateway_mongo")


class _MongoClientSingleton:
    mongo_client: AsyncIOMotorClient | None
    engine: AIOEngine
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(_MongoClientSingleton, cls).__new__(cls)
            cls.instance.mongo_client = AsyncIOMotorClient(
                settings.MONGO_DATABASE_URL, driver=DRIVER_INFO
            )
            cls.instance.engine = AIOEngine(
                client=cls.instance.mongo_client,
                database=settings.MONGO_DATABASE,
            )
        return cls.instance


def MongoDatabase() -> core.AgnosticDatabase:
    return _MongoClientSingleton().mongo_client[settings.MONGO_DATABASE]


def get_engine() -> AIOEngine:
    return _MongoClientSingleton().engine


async def ping():
    await MongoDatabase().command("ping")


__all__ = ["MongoDatabase", "ping", "get_engine"]