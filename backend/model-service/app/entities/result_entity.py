from typing import Optional
from datetime import datetime


class ResultEntity:
    def __init__(self,
        user_id: str,
        task_id: str,
        task_type: str,
        model_names: list,
        model_params: list,
        status: str = "PENDING",
        created_at: Optional[datetime] = None,

        # This will create after execute
        completed_at: Optional[datetime] = None,
        target_pred: Optional[list] = None,
        target_true: Optional[list] = None,
        feature_importance: Optional[list] = None,
        score_report: Optional[str] = None,

        _id: Optional[str] = None,
    ):
        self.id = _id
        self.user_id = user_id
        self.task_id = task_id
        self.task_type = task_type
        self.model_names = model_names
        self.model_params = model_params
        self.status = status
        self.created_at = created_at or datetime.now().isoformat()
        self.completed_at = completed_at
        self.target_pred = target_pred
        self.target_true = target_true
        self.feature_importance = feature_importance
        self.score_report = score_report

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "task_id": self.task_id,
            "task_type": self.task_type,
            "model_names": self.model_names,
            "model_params": self.model_params,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at if self.completed_at else None,
            "target_pred": self.target_pred if self.target_pred else None,
            "target_true": self.target_true if self.target_true else None,
            "feature_importance": self.feature_importance if self.feature_importance else None,
            "score_report": self.score_report if self.score_report else None,
        }