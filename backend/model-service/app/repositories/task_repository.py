from typing import Optional

from bson import ObjectId
from pymongo import ReturnDocument
from app.core.database import db
from app.entities.task_entity import TaskEntity


class TaskRepository:
    @staticmethod
    async def insert(task: TaskEntity):
        result = await db.tasks.insert_one(task.to_dict())
        return str(result.inserted_id)

    @staticmethod
    async def get_by_id(task_id: str) -> Optional[TaskEntity]:
        doc = await db.tasks.find_one({"_id": ObjectId(task_id)})
        if doc:
            return TaskEntity(
                _id=str(doc["_id"]),
                name=doc["name"],
                user_id=doc["user_id"],
                task_type=doc["task_type"],
                dataset_id=doc["dataset_id"],
                model_names=doc["model_names"],
                model_params=doc["model_params"],
                modified_at=doc["modified_at"],
                cron_expression=doc["cron_expression"]
            )
        return None

    @staticmethod
    async def update(task_id: str, updates: dict):
        doc = await db.tasks.find_one_and_update(
            {"_id": ObjectId(task_id)},
            {"$set": updates},
            return_document=ReturnDocument.AFTER
        )

        if doc:
            return TaskEntity(
                _id=str(doc["_id"]),
                name=doc["name"],
                task_type=doc["task_type"],
                dataset_id=doc["dataset_id"],
                model_names=doc["model_names"],
                model_params=doc["model_params"],
                modified_at=doc["modified_at"],
                cron_expression=doc["cron_expression"]
            )
        return None

    @staticmethod
    async def get_all(user_id):
        cursor = db.tasks.find({"user_id": user_id})
        docs = await cursor.to_list(None)
        tasks = []
        for doc in docs:
            tasks.append(TaskEntity(
                _id=str(doc["_id"]),
                user_id=doc["user_id"],
                name=doc["name"],
                task_type=doc["task_type"],
                dataset_id=doc["dataset_id"],
                model_names=doc["model_names"],
                model_params=doc["model_params"],
                modified_at=doc["modified_at"],
                cron_expression=doc["cron_expression"],
            ))

        return tasks