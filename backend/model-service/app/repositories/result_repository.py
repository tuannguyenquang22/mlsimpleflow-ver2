from bson import ObjectId
from pymongo import ReturnDocument

from app.core.database import db
from app.entities.result_entity import ResultEntity


class ResultRepository:

    @staticmethod
    async def insert(result: ResultEntity):
        doc = await db.results.insert_one(result.to_dict())
        return str(doc.inserted_id)


    @staticmethod
    async def find_all(user_id: str):
        cursor = db.results.find({"user_id": user_id})
        docs = await cursor.to_list(None)
        results = []
        for doc in docs:
            results.append(ResultEntity(
                _id=str(doc["_id"]),
                user_id=doc["user_id"],
                task_id=doc["task_id"],
                task_type=doc["task_type"],
                model_names=doc["model_names"],
                model_params=doc["model_params"],
                status=doc["status"],
                created_at=doc["created_at"],
                completed_at=doc["completed_at"],
                score_report=doc["score_report"],
                target_pred=doc["target_pred"],
                target_true=doc["target_true"],
            ))
        return results
        

    @staticmethod
    async def get_by_id(result_id: str):
        doc = await db.results.find_one({"_id": ObjectId(result_id)})
        if doc:
            return ResultEntity(
                _id=str(doc["_id"]),
                user_id=doc["user_id"],
                task_id=doc["task_id"],
                task_type=doc["task_type"],
                model_names=doc["model_names"],
                model_params=doc["model_params"],
                status=doc["status"],
                created_at=doc["created_at"],
                completed_at=doc["completed_at"],
                target_pred=doc["target_pred"],
                target_true=doc["target_true"],
                feature_importance=doc["feature_importance"],
                score_report=doc["score_report"]
            )
        return None

    @staticmethod
    async def update(result_id: str, updates: dict):
        doc = await db.results.find_one_and_update(
            {"_id": ObjectId(result_id)},
            {"$set": updates},
            return_document=ReturnDocument.AFTER
        )

        if doc:
            return ResultEntity(
                _id=str(doc["_id"]),
                user_id=doc["user_id"],
                task_id=doc["task_id"],
                task_type=doc["task_type"],
                model_names=doc["model_names"],
                model_params=doc["model_params"],
            )
        return None