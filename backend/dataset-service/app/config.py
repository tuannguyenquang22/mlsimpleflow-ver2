import os
from dotenv import load_dotenv


load_dotenv()


MONGO_DATABASE_URL = os.getenv("MONGO_DATABASE_URL", "mongodb://root:example@localhost:27017")
DATABASE_NAME = "mlsimpleflow_dataset"
DATASET_STORAGE_PATH = "./data/datasets"
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
PREPROCESSING_CHANNEL = "preprocessing"