from typing import Optional
from app.entities.result_entity import ResultEntity
from app.repositories.result_repository import ResultRepository


class ResultService:
    @staticmethod
    async def create_result(
        task_id: str,
        task_type: str,
        model_names: list,
        model_params: list,
        user_id: str,
    ):
        result = ResultEntity(
            task_id=task_id,
            task_type=task_type,
            model_names=model_names,
            model_params=model_params,
            user_id=user_id
        )

        result_id = await ResultRepository.insert(result)
        return result_id

    @staticmethod
    async def get_all(user_id: str):
        return await ResultRepository.find_all(user_id=user_id)

    @staticmethod
    async def get_result_by_id(result_id: str) -> Optional[ResultEntity]:
        result = await ResultRepository.get_by_id(result_id)
        return result

    @staticmethod
    async def update_result(result_id: str, updates: dict):
        result = await ResultRepository.update(result_id, updates)
        return result