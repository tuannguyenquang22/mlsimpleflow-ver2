import asyncio
import json
from app.database import redis_client, PREPROCESSING_CHANNEL
from app.preprocessing import execute


async def main():
    print("[INFO]   preprocessing-service: Ready to receive messages")
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(PREPROCESSING_CHANNEL)

    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            data = json.loads(message['data'].decode('utf-8'))
            user_id = data['user_id']
            dataset_id = data['dataset_id']
            use_columns = data['use_columns']
            desired_data_type = data['desired_data_type']
            target = data['target_column']

            desired_dtype: dict = {}
            for i in range(len(use_columns)):
                desired_dtype[use_columns[i]] = desired_data_type[i]

            execute_result = execute(user_id, dataset_id, use_columns, target, desired_dtype)
            print(execute_result)


asyncio.run(main())