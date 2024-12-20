import os
from dotenv import load_dotenv


load_dotenv()


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
EXECUTE_CHANNEL = os.getenv("EXECUTE_CHANNEL", "execute")

DATASET_SERVICE_URL = os.getenv("DATASET_SERVICE_URL", "")
MODEL_SERVICE_URL = os.getenv("MODEL_SERVICE_URL", "")