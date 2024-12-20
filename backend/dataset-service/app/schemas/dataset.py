from datetime import datetime
from typing import Optional


def create_dataset_document(
    name: str,
    user_id: str,
    file_path: str,
    columns: list,
    data_types: list,
    num_rows: int,
    message: str,
    dataset_type: str,
    problem_type: Optional[str] = None,
    target_column: Optional[str] = None,
):
    return {
        "name": name,
        "user_id": user_id,
        "file_path": file_path,
        "type": dataset_type,
        "columns": columns,
        "data_types": data_types,
        "num_rows": num_rows,
        "created_at": datetime.now(),
        "message": message,
        "problem_type": problem_type,
        "target_column": target_column,
    }