import os
from typing import Optional

from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends
from fastapi.responses import FileResponse
from app.utils.file_storage import save_dataset_file
from app.services.dataset_service import (
    insert_dataset,
    get_dataset_info,
    delete_dataset,
    get_dataset_file_path,
    publish_preprocessing_dataset,
    get_dataset_by_type
)
from app.utils.csv_utils import get_csv_metadata
from app.models.dataset import DatasetInfo
from app import deps


router = APIRouter(prefix="/v1", tags=["v1"])


@router.post("/datasets/upload")
async def upload_dataset(
    dataset_type: str = Form(...),
    message: Optional[str] = Form(default=None),
    problem_type: Optional[str] = Form(default=None),
    target_column: Optional[str] = Form(default=None),
    file: UploadFile = File(...),
    user_id: str = Depends(deps.get_user_id)
):
    try:
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are supported.")

        file_path = save_dataset_file(file)
        columns, data_types, num_rows = get_csv_metadata(file_path)
        dataset_name = file.filename

        if message is None or message == "":
            message = f"INFO:This is raw dataset."

        if problem_type is None or problem_type == "":
            problem_type = "UNKNOWN"

        await insert_dataset(
            dataset_name,
            user_id,
            file_path,
            columns,
            data_types,
            num_rows,
            message,
            dataset_type,
            problem_type,
            target_column,
        )
        return {"detail": "OK."}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/datasets/{dataset_id}/info", response_model=DatasetInfo)
async def get_info(
    dataset_id: str,
    user_id: str = Depends(deps.get_user_id)
):
    try:
        data = await get_dataset_info(dataset_id)
        if data is None:
            raise HTTPException(status_code=404, detail="Dataset not found.")
        return DatasetInfo(**data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/datasets/{dataset_id}")
async def remove_dataset(dataset_id: str, user_id: str = Depends(deps.get_user_id)):
    try:
        success = await delete_dataset(dataset_id)
        if not success:
            raise HTTPException(status_code=404, detail="Dataset not found or already deleted.")
        return {"detail": "Dataset deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/datasets/{dataset_id}/download")
async def download_dataset(dataset_id: str, user_id: str = Depends(deps.get_user_id)):
    try:
        file_path = await get_dataset_file_path(dataset_id)
        if file_path is None:
            raise HTTPException(status_code=404, detail="Dataset not found.")

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Dataset file not found.")

        return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/datasets/{dataset_id}/preprocessing")
async def preprocessing_dataset(
    dataset_id: str,
    target_column: str = Form(...),
    use_columns: Optional[list] = Form(default=None),
    desired_data_types: Optional[list]= Form(default=None),
    user_id: str = Depends(deps.get_user_id)
):
    try:
        if use_columns is None and desired_data_types is None:
            dataset_info = await get_dataset_info(dataset_id)
            columns = dataset_info["columns"]
            data_types = dataset_info["data_types"]

        elif use_columns is not None and desired_data_types is not None:
            if len(use_columns) != len(desired_data_types):
                return HTTPException(status_code=400, detail="The number of columns to use and desired data types must be the same.")
            else:
                if len(use_columns) == 1:
                    return HTTPException(status_code=400, detail="At least two columns must be used.")

                columns = use_columns
                data_types = desired_data_types
        else:
            return HTTPException(status_code=400, detail="At least one of use_columns or desired_data_types must be provided.")

        if target_column not in columns:
            return HTTPException(status_code=400, detail="The target column must be included in the columns to use.")

        await publish_preprocessing_dataset(user_id, dataset_id, columns, target_column, data_types)
        return {"detail": "OK."}
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail=str(e))


@router.get("/datasets/{dataset_type}")
async def get_type(dataset_type: str, user_id: str = Depends(deps.get_user_id)):
    try:
        datasets =  await get_dataset_by_type(dataset_type)
        if datasets is None:
            raise HTTPException(status_code=404, detail="Dataset not found.")
        dataset_infos = []
        for d in datasets:
            dataset_infos.append(DatasetInfo(**d))

        return dataset_infos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))