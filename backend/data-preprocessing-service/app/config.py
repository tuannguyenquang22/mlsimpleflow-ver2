import os

from dotenv import load_dotenv

load_dotenv()


REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
PREPROCESSING_CHANNEL = "preprocessing"

DATASET_SERVICE_URL = os.environ.get('DATASET_SERVICE_URL', '')