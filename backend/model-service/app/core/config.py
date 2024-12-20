import os

from dotenv import load_dotenv

load_dotenv()

MONGO_DATABASE_URL = os.getenv("MONGO_DATABASE_URL", "mongodb://root:example@localhost:27017")
DATABASE_NAME = "mlsimpleflow_model"
MODEL_STORAGE_PATH = os.getenv("MODEL_STORAGE_PATH", "./data/models")

# DATASET_SERVICE_URL = os.getenv("DATASET_SERVICE_URL", "http://localhost:8081/v1")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
EXECUTE_CHANNEL = os.getenv("EXECUTE_CHANNEL", "execute")