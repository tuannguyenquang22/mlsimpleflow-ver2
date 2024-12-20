from fastapi import APIRouter, Request, Depends, Response, HTTPException
from starlette.datastructures import UploadFile
import httpx
from app.core.config import settings
from app import models
from app.api import deps

router = APIRouter()

@router.post("/{path:path}")
async def proxy_dataset_service(
    path: str,
    request: Request,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    try:
        content_type = request.headers.get("content-type", "")
        headers = {
            "X-User-ID": str(current_user.id),
        }
        async with httpx.AsyncClient() as client:
            if "multipart/form-data" in content_type:
                form = await request.form()
                form_data = {k: v for k, v in form.items() if not isinstance(v, UploadFile)}
                files = {
                    k: (file.filename, await file.read(), file.content_type)
                    for k, file in form.items()
                    if isinstance(file, UploadFile)
                }
                proxy = await client.post(f"{settings.DATASET_SERVICE_URL}/{path}", headers=headers, data=form_data, files=files)
            elif "application/x-www-form-urlencoded" in content_type:
                data = await request.form()
                proxy = await client.post(f"{settings.DATASET_SERVICE_URL}/{path}", headers=headers, data=data)
            else:
                data = await request.body()
                proxy = await client.post(f"{settings.DATASET_SERVICE_URL}/{path}", headers=headers, content=data)
        response = Response(content=proxy.content, status_code=proxy.status_code)
        return response
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.get("/{path:path}")
async def proxy_dataset_service(
    path: str,
    request: Request,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    try:
        headers = {
            "X-User-ID": str(current_user.id),
        }
        async with httpx.AsyncClient() as client:
            proxy = await client.get(f"{settings.DATASET_SERVICE_URL}/{path}", headers=headers)
        response = Response(content=proxy.content, status_code=proxy.status_code)
        return response
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))