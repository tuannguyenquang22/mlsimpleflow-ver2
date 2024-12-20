import asyncio
import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import requests

import aioredis

load_dotenv()

REDIS_URI = os.getenv("REDIS_URI", "redis://localhost:6379")

NOTIFICATION_CHANNEL = "notify"
KEY = "FROM_NOTIFY_20200563"
GATEWAY_URL = os.getenv("GATEWAY_URL")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

redis_client = aioredis.from_url(REDIS_URI)

SUBJECT = "[MLSIMPLEFLOW] Notification service"

def send_notify(
        subject: str,
        body: str,
        to_email: str,
        from_email: str,
        from_password: str,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 587
):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Bật TLS
        server.login(from_email, from_password)  # Login email
        server.send_message(msg)


async def main():
    print("[INFO]   notification-service: Ready to receive messages")
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(NOTIFICATION_CHANNEL)

    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            data = json.loads(message['data'].decode('utf-8'))
            from_service = data['from']
            to_user = data['to']
            to_user_email = requests.get(f"{GATEWAY_URL}/api/v1/users/email/{to_user}").text

            notify_message = data['message']
            print(f"[INFO]   notification-service: Received message from {from_service} to {to_user}: {notify_message}")
            send_notify(f"{SUBJECT} (from {from_service} service)", notify_message, to_user_email, SENDER_EMAIL, SENDER_PASSWORD )


asyncio.run(main())