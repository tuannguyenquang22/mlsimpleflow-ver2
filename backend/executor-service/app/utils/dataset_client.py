import requests
from datetime import datetime
from app.core.config import DATASET_SERVICE_URL

DATASET_URL = DATASET_SERVICE_URL

def download_dataset(user_id, dataset_id, save_path = "./data"):
    message = ""
    headers = {
        "X-User-ID": user_id
    }
    response_info = requests.get(f"{DATASET_URL}/v1/datasets/{dataset_id}/info", headers=headers)
    if response_info.status_code != 200:
        message = "ERROR:Failed to get dataset info;"
        return message, None

    dataset_name = response_info.json()["name"]
    response_file = requests.get(f"{DATASET_URL}/v1/datasets/{dataset_id}/download", stream=True, headers=headers)
    file_path = f"{save_path}/{datetime.now().isoformat()}_{dataset_name}"
    with open(file_path, "wb") as f:
        for chunk in response_file.iter_content(chunk_size=2048):
            if chunk:
                f.write(chunk)

    message = "SUCCESS:Dataset downloaded;"
    return message, file_path


def get_dataset_info(user_id, dataset_id):
    headers = {
        "X-User-ID": user_id
    }
    response = requests.get(f"{DATASET_URL}/v1/datasets/{dataset_id}/info", headers=headers)
    return response.json()