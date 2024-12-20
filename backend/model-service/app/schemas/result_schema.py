from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.entities.result_entity import ResultEntity


class ResultSchema(BaseModel):
    id: str
    task_id: str
    task_type: str
    model_names: List[str]
    model_params: List[str]
    status: str
    created_at: Optional[datetime] = None

    # This will create after execute
    completed_at: Optional[datetime] = None
    target_pred: Optional[list] = None
    target_true: Optional[list] = None
    feature_importance: Optional[list] = None
    score_report: Optional[str] = None

    @staticmethod
    def from_entity(e: ResultEntity):
        return ResultSchema(
            id=e.id,
            task_id=e.task_id,
            task_type=e.task_type,
            model_names=e.model_names,
            model_params=e.model_params,
            status=e.status,
            created_at=e.created_at,
            completed_at=e.completed_at,
            target_pred=e.target_pred,
            target_true=e.target_true,
            feature_importance=e.feature_importance,
            score_report=e.score_report,
        )