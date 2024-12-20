import asyncio
import time

from app.tune import tune_params
from app.utils.redis_client import redis_client
from app.core.config import EXECUTE_CHANNEL
from app.utils import model_client, dataset_client
from app.train import train
from datetime import datetime
import json
import os


async def main():
    print("[INFO]   executor-service: Ready to receive messages")
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(EXECUTE_CHANNEL)
    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            data = message['data'].decode('utf-8')
            data_dict = json.loads(data)

            task_id = data_dict['task_id']
            user_id = data_dict['user_id']

            print(f"[INFO]   executor-service: Received task {task_id} by user {user_id}")
            task = model_client.get_task_info(user_id, task_id)
            dataset = dataset_client.get_dataset_info(user_id, task['dataset_id'])
            message, downloaded_file = dataset_client.download_dataset(user_id, dataset['id'])

            print("[INFO]   executor-service: Training")
            create_response = model_client.create_result(
                user_id=user_id,
                task_id=task_id,
                task_type=task["task_type"],
                model_names=task["model_names"],
                model_params=task["model_params"],
            )
            result_id = create_response["result_id"]

            try:
                if task["task_type"] == "train":
                    score_report, y_true, y_pred = train(
                        file_path=downloaded_file,
                        task=task,
                        dataset=dataset,
                    )

                elif task["task_type"] == "tune":
                    score_report, y_true, y_pred = tune_params(
                        file_path=downloaded_file,
                        task=task,
                        dataset=dataset,
                    )

                completed_at = datetime.now().isoformat()
                print(f"[INFO]   executor-service: Training completed at: {completed_at}")
                model_client.update_result(
                    result_id=result_id,
                    user_id=user_id,
                    status="COMPLETED",
                    completed_at=completed_at,
                    target_true=y_true,
                    target_pred=y_pred,
                    score_report=json.dumps(score_report),
                )

            except Exception as e:
                time.sleep(3)
                message = model_client.update_result(
                    user_id=user_id,
                    result_id=result_id,
                    status="FAILED",
                    completed_at=datetime.now().isoformat(),
                )
                print(f"[ERROR]  executor-service: {e}; {message}")
            finally:
                os.remove(downloaded_file)


asyncio.run(main())