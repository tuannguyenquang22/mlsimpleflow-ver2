from fastapi import FastAPI
from app.routers import dataset

app = FastAPI(
    title="MLSimpleflow Dataset Service"
)

app.include_router(dataset.router)
