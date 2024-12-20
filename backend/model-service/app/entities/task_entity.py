from typing import Optional
from datetime import datetime


class TaskEntity:
    def __init__(self,
        name: str,
        user_id: str,
        task_type: str,
        dataset_id: str,
        model_names: list,
        model_params: list,
        modified_at: Optional[datetime] = None,
        cron_expression: Optional[str] = None,
        _id: Optional[str] = None
    ):
        self.id = _id
        self.name = name
        self.user_id = user_id
        self.task_type = task_type
        self.dataset_id = dataset_id
        self.model_names = model_names
        self.model_params = model_params
        self.modified_at = modified_at or datetime.now()
        self.cron_expression = cron_expression

    def to_dict(self):
        return {
            "name": self.name,
            "user_id": self.user_id,
            "task_type": self.task_type,
            "dataset_id": self.dataset_id,
            "model_names": self.model_names,
            "model_params": self.model_params,
            "modified_at": self.modified_at.isoformat(),
            "cron_expression": self.cron_expression if self.cron_expression else None,
        }