from typing import Optional
import os
from app.database import db, redis_client, PREPROCESSING_CHANNEL
from app.schemas.dataset import create_dataset_document
from bson.objectid import ObjectId
import json


async def insert_dataset(
    name: str,
    user_id: str,
    file_path: str,
    columns: list,
    data_types: list,
    num_rows: int,
    message: str,
    dataset_type: str,
    problem_type: Optional[str] = None,
    target_column: Optional[str] = None,
) -> str:
    doc = create_dataset_document(
        name,
        user_id,
        file_path,
        columns,
        data_types,
        num_rows,
        message,
        dataset_type,
        problem_type,
        target_column,
    )
    result = await db.datasets.insert_one(doc)
    return str(result.inserted_id)


async def get_dataset_info(dataset_id: str) -> Optional[dict]:
    doc = await db.datasets.find_one({"_id": ObjectId(dataset_id)})
    if doc:
        return {
            "id": str(doc["_id"]),
            "name": doc["name"],
            "type": doc["type"],
            "columns": doc["columns"],
            "data_types": doc["data_types"],
            "num_rows": doc["num_rows"],
            "created_at": doc["created_at"].isoformat(),
            "message": doc["message"],
            "problem_type": doc["problem_type"],
            "target_column": doc["target_column"],
        }
    return None


async def get_dataset_by_type(dataset_type: str) -> Optional[list]:
    cursor = db.datasets.find({"type": dataset_type})
    docs = await cursor.to_list(None)
    datasets = []
    for doc in docs:
        datasets.append({
            "id": str(doc["_id"]),
            "name": doc["name"],
            "type": doc["type"],
            "columns": doc["columns"],
            "data_types": doc["data_types"],
            "num_rows": doc["num_rows"],
            "created_at": doc["created_at"].isoformat(),
            "message": doc["message"],
            "problem_type": doc["problem_type"],
            "target_column": doc["target_column"],
        })
    return datasets


async def delete_dataset(dataset_id: str) -> bool:
    doc = await db.datasets.find_one({"_id": ObjectId(dataset_id)})
    if not doc:
        return False
    file_path = doc["file_path"]
    result = await db.datasets.delete_one({"_id": ObjectId(dataset_id)})
    if result and os.path.exists(file_path):
        os.remove(file_path)
    return True


async def get_dataset_file_path(dataset_id: str) -> Optional[str]:
    doc = await db.datasets.find_one({"_id": ObjectId(dataset_id)})
    if doc:
        return doc["file_path"]
    return None


async def publish_preprocessing_dataset(user_id: str, dataset_id: str, use_columns: list, target_column: str, desired_data_type: list):
    task = {
        "dataset_id": dataset_id,
        "user_id": user_id,
        "use_columns": use_columns,
        "target_column": target_column,
        "desired_data_type": desired_data_type
    }
    task_encoded = json.dumps(task).encode("utf-8")
    await redis_client.publish(PREPROCESSING_CHANNEL, task_encoded)