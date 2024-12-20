from typing import Optional
from app.entities.task_entity import TaskEntity
from app.repositories.task_repository import TaskRepository


class TaskService:
    @staticmethod
    async def create_task(
        name: str,
        user_id: str,
        task_type: str,
        dataset_id: str,
        model_names: list,
        model_params: list,
        cron_expression: str = None,
    ):
        task = TaskEntity(
            name=name,
            user_id=user_id,
            task_type=task_type,
            dataset_id=dataset_id,
            model_names=model_names,
            model_params=model_params,
            cron_expression=cron_expression,
        )

        task_id = await TaskRepository.insert(task)
        return task_id

    @staticmethod
    async def get_all(user_id: str):
        tasks = await TaskRepository.get_all(user_id)
        return tasks

    @staticmethod
    async def get_task_by_id(task_id: str) -> Optional[TaskEntity]:
        task = await TaskRepository.get_by_id(task_id)
        return task

    @staticmethod
    async def update_task(task_id: str, updates: dict):
        task = await TaskRepository.update(task_id, updates)
        return task