import json

from fastapi import APIRouter


router = APIRouter(prefix="/v3.10")


@router.get("/metadata")
def get_machine_learning_model_metadata():
    with open("app/metadata/model.json") as f:
        data = json.load(f)
        f.close()
        return data