import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
import os
import uuid

from messages.verification import handle_verification_message
from routes.proof_requests import router as ProofRequestRouter
from routes.users import router as UserRouter
from services.queue_service import PikaClient

load_dotenv()
app = FastAPI()
pika_client = PikaClient(os.environ.get('RABBITMQ_URL'))

app.include_router(UserRouter, tags=["User"], prefix="/users")
app.include_router(ProofRequestRouter, tags=["Circuit"], prefix="/proof_requests")

@app.on_event('startup')
async def startup():
  consumer_id = str(uuid.uuid4())
  loop = asyncio.get_running_loop()

  task = loop.create_task(pika_client.consume(consumer_id, 'verifications_queue', handle_verification_message, loop))
  await task
