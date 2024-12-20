import os
from app.config import DATASET_STORAGE_PATH
from fastapi import UploadFile
import uuid


def save_dataset_file(file: UploadFile) -> str:
    file_ext = file.filename.split(".")[-1].lower()
    new_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(DATASET_STORAGE_PATH, new_filename)

    os.makedirs(DATASET_STORAGE_PATH, exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path