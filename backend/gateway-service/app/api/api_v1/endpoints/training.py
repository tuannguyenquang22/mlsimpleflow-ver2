import json

from fastapi import APIRouter, Request, Depends, Response, HTTPException
import httpx
from app.core.config import settings
from app import models
from app.api import deps


router = APIRouter()


@router.post("/{path:path}")
async def proxy_training_service(
    path: str,
    request: Request,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    try:
        headers = {
            "X-User-ID": str(current_user.id),
        }
        async with httpx.AsyncClient() as client:
            try:
                data = await request.json()
            except Exception:
                data = None

            if not data:
                proxy = await client.post(f"{settings.MODEL_SERVICE_URL}/{path}", headers=headers)
            else:
                proxy = await client.post(f"{settings.MODEL_SERVICE_URL}/{path}", headers=headers, json=data)
        response = Response(content=proxy.content, status_code=proxy.status_code)
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=403, detail=str(e))
    

@router.get("/{path:path}")
async def proxy_training_service(
        path: str,
        request: Request,
        current_user: models.User = Depends(deps.get_current_active_user),
):
    try:
        headers = {
            "X-User-ID": str(current_user.id),
        }
        async with httpx.AsyncClient() as client:
            proxy = await client.get(f"{settings.MODEL_SERVICE_URL}/{path}", headers=headers)
        response = Response(content=proxy.content, status_code=proxy.status_code)
        return response
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
