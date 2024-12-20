import json

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

from app.schemas.task_schema import TaskSchema
from app.utils.scheduler import schedule_task, execute_task

from app.services.task_service import TaskService
from app import deps


router = APIRouter(prefix="/v1")


class CreateTaskRequest(BaseModel):
    name: str
    task_type: str
    dataset_id: str
    model_names: Optional[List[str]] = None
    model_params: Optional[List[dict]] = None
    cron_expression: Optional[str] = None


class UpdateTaskRequest(BaseModel):
    model_params: Optional[List[dict]] = None
    cron_expression: Optional[str] = None


@router.post("/tasks")
async def create_task(task: CreateTaskRequest, user_id: str = Depends(deps.get_user_id)):
    try:
        task_id = await TaskService.create_task(
            name=task.name,
            user_id=user_id,
            task_type=task.task_type,
            dataset_id=task.dataset_id,
            model_names=task.model_names,
            model_params=[json.dumps(tp) for tp in task.model_params],
            cron_expression=task.cron_expression,
        )

        if task.cron_expression:
            schedule_task(task_id=task_id, user_id=user_id, cron_expression=task.cron_expression)

        return {"detail": "Task created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/{task_id}", response_model=TaskSchema)
async def get_task(task_id: str, user_id: str = Depends(deps.get_user_id)):
    try:
        task = await TaskService.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found.")
        return TaskSchema.from_entity(task)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks/{task_id}/run")
async def run_task(task_id: str, user_id: str = Depends(deps.get_user_id)):
    try:
        task = await TaskService.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found.")
        await execute_task(task.id, user_id)
        return {"detail": "Task run successfully."}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks")
async def get_all_tasks(user_id: str = Depends(deps.get_user_id)):
    try:
        tasks = await TaskService.get_all(user_id)
        if not tasks:
            return []
        return [TaskSchema.from_entity(t) for t in tasks]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tasks/{task_id}")
async def update_task(task_id: str, updates: UpdateTaskRequest, user_id: str = Depends(deps.get_user_id)):
    try:
        task = {
            "model_params": [],
            "cron_expression": updates.cron_expression,
        }
        for param in updates.model_params:
            task["model_params"].append(json.dumps(param))

        schedule_task(task_id, user_id, task["cron_expression"])
        await TaskService.update_task(task_id, task)
        return {"detail": "Task updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))