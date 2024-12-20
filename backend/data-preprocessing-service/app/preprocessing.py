import os

import requests
import pandas as pd
from app.core import preprocessing_dataset
from app.config import DATASET_SERVICE_URL


def download_dataset(user_id: str, dataset_id: str, save_path: str = "./data/raw"):
    save_file = ""
    try:
        headers = {
            "X-User-ID": user_id,
        }
        response_info = requests.get(f"{DATASET_SERVICE_URL}/v1/datasets/{dataset_id}/info", headers=headers)
        if response_info.status_code == 200:
            dataset_name = response_info.json()["name"]
            save_file = f"{save_path}/{dataset_name}"
    except requests.exceptions.RequestException as e:
        message = f"ERROR:Failed to get dataset {dataset_id}: {e}"
        return "ERROR", message

    try:
        response = requests.get(f"{DATASET_SERVICE_URL}/v1/datasets/{dataset_id}/download", stream=True, headers=headers)
        response.raise_for_status()  # Ensure we catch HTTP errors
        with open(save_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return "SUCCESS", save_file.split("/")[-1]

    except requests.exceptions.RequestException as e:
        message = f"ERROR:Failed to download dataset {dataset_id}: {e}"
        return "ERROR", message


def upload_dataset(user_id: str, file_path: str, messages: str, problem_type: str, target_column: str):
    headers = {
        "X-User-ID": user_id,
    }
    url = f"{DATASET_SERVICE_URL}/v1/datasets/upload"
    files = {
        "file": (file_path.split("/")[-1], open(file_path, "rb"), "text/csv"),
    }
    data = {
        "dataset_type": "preprocessed",
        "message": messages,
        "problem_type": problem_type,
        "target_column": target_column,
    }

    response = requests.post(url, files=files, data=data, headers=headers)
    if response.status_code == 200:
        print("Upload successful:", response.json())
    else:
        print("Upload failed:", response.status_code, response.text)


def execute(user_id: str, dataset_id: str, use_columns: list, target: str, desired_dtype: dict):
    notify_result = {
        "dataset_id": dataset_id,
        "status": "",
        "message": "",
    }

    status, data = download_dataset(user_id, dataset_id)
    if status == "ERROR":
        notify_result["status"] = status
        notify_result["message"] = data
        return notify_result

    try:
        df = pd.read_csv(f"./data/raw/{data}", usecols=use_columns)
    except Exception as e:
        notify_result["status"] = "ERROR"
        notify_result["message"] = f"ERROR:Failed to read dataset {dataset_id}: {e}"
        return notify_result

    df, messages, trainable, problem_type = preprocessing_dataset(df, target, desired_dtype)
    if not trainable:
        notify_result["status"] = "ERROR"
        notify_result["message"] = messages
        return notify_result

    df.to_csv(f"./data/preprocessed/{data}", index=False)
    upload_dataset(user_id, f"./data/preprocessed/{data}", messages, problem_type, target)

    notify_result["status"] = "SUCCESS"
    notify_result["message"] = messages

    os.remove(f"./data/raw/{data}")
    os.remove(f"./data/preprocessed/{data}")

    return notify_result



