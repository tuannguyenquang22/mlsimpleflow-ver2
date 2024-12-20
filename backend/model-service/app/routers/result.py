from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel

from app.schemas.result_schema import ResultSchema
from app.services.result_service import ResultService
from app import deps


router = APIRouter(prefix="/v1")


class CreateResultRequest(BaseModel):
    task_id: str
    task_type: str
    model_names: List[str]
    model_params: Optional[List[str]] = None


class UpdateResultRequest(BaseModel):
    status: str
    completed_at: Optional[datetime] = None
    target_pred: Optional[list] = None
    target_true: Optional[list] = None
    feature_importance: Optional[list] = None
    score_report: Optional[str] = None


@router.get("/results")
async def get_all(user_id: str = Depends(deps.get_user_id)):
    try:
        results = await ResultService.get_all(user_id)
        return [ResultSchema.from_entity(result) for result in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results/{result_id}")
async def get_result_by_id(result_id: str, user_id: str = Depends(deps.get_user_id)):
    try:
        result = await ResultService.get_result_by_id(result_id)
        if not result:
            raise HTTPException(status_code=404, detail="Result not found.")
        return ResultSchema.from_entity(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/results")
async def create_result(req: CreateResultRequest, user_id: str = Depends(deps.get_user_id)):
    try:
        result_id = await ResultService.create_result(
            task_id=req.task_id,
            task_type=req.task_type,
            model_names=req.model_names,
            model_params=req.model_params,
            user_id=user_id,
        )
        return {"detail": "Result created successfully.", "result_id": result_id}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/results/{result_id}")
async def update_result(result_id: str, req: UpdateResultRequest, user_id: str = Depends(deps.get_user_id)):
    try:
        updates = req.model_dump()
        result = await ResultService.update_result(result_id, updates)
        if result:
            return {"detail": "Result updated successfully."}
        else:
            raise HTTPException(status_code=404, detail="Result not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
