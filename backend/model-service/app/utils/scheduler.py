import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.core.config import EXECUTE_CHANNEL
import json

from app.utils.redis_client import redis_client

scheduler = AsyncIOScheduler()


async def execute_task(task_id: str, user_id: str):
    try:
        data = {
            "task_id": task_id,
            "user_id": user_id,
        }
        data_encoded = json.dumps(data).encode("utf-8")
        await redis_client.publish(channel=EXECUTE_CHANNEL, message=data_encoded)
    except Exception as e:
        print(f"Failed when executing task {task_id}: {e}")


def schedule_task(task_id: str, user_id: str, cron_expression: str):
    job_id = f"task_{task_id}"
    try:
        scheduler.remove_job(job_id)
    except:
        pass
    if not cron_expression:
        return
    trigger = CronTrigger.from_crontab(cron_expression)
    scheduler.add_job(lambda: asyncio.run(execute_task(task_id, user_id)), trigger=trigger, id=job_id, replace_existing=True)
