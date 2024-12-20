from fastapi import FastAPI
from app.utils.scheduler import scheduler
from app.routers import task, result, metadata
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    print("Scheduler started.")
    try:
        yield
    finally:
        # Actions to perform on shutdown
        scheduler.shutdown()
        print("Scheduler shut down.")

app = FastAPI(lifespan=lifespan, title="MLSimpleflow Model Service")
app.include_router(task.router)
app.include_router(result.router)
app.include_router(metadata.router)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


