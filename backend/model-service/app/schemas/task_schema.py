from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.entities.task_entity import TaskEntity


class TaskSchema(BaseModel):
    id: str
    name: str
    task_type: str
    dataset_id: str
    model_names: List[str]
    model_params: Optional[List[str]] = None
    modified_at: datetime
    cron_expression: Optional[str] = None

    @staticmethod
    def from_entity(e: TaskEntity):
        return TaskSchema(
            id=e.id,
            name=e.name,
            task_type=e.task_type,
            dataset_id=e.dataset_id,
            model_names=e.model_names,
            model_params=e.model_params,
            modified_at=e.modified_at,
            cron_expression=e.cron_expression
        )

