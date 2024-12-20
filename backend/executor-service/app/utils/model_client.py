from typing import Optional, List
from app.core.config import MODEL_SERVICE_URL

import requests

MODEL_URL = MODEL_SERVICE_URL

def get_task_info(user_id, task_id):
    headers = {
        "X-User-ID": user_id
    }
    response = requests.get(f"{MODEL_URL}/v1/tasks/{task_id}", headers=headers)
    return response.json()


def create_result(user_id, task_id, task_type, model_names, model_params):
    headers = {
        "X-User-ID": user_id
    }

    body = {
        "task_id": task_id,
        "task_type": task_type,
        "model_names": model_names,
        "model_params": model_params
    }

    response = requests.post(f"{MODEL_URL}/v1/results", json=body, headers=headers)
    if response.status_code != 200:
        return None
    return response.json()


def update_result(
    user_id: str,
    result_id: str,
    status: str,
    completed_at,
    target_pred: Optional[List] = None,
    target_true: Optional[List] = None,
    score_report: Optional[str] = None,
):
    headers = {
        "X-User-ID": user_id
    }

    body = {
        "completed_at": completed_at,
        "status": status,
    }

    if status == "COMPLETED":
        body["target_pred"] = target_pred
        body["target_true"] = target_true
        body["score_report"] = score_report

    response = requests.put(f"{MODEL_URL}/v1/results/{result_id}/", json=body, headers=headers)
    if response.status_code != 200:
        return None
    return response.json()


