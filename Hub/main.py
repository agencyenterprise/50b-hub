import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid

from messages.proof import handle_proof_message
from routes.proof_requests import router as ProofRequestRouter
from routes.users import router as UserRouter
from services.queue_service import PikaClient

load_dotenv()
app = FastAPI()

origins = [
  "http://localhost:3000",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

pika_client = PikaClient(os.environ.get('RABBITMQ_URL'))

app.include_router(UserRouter, tags=["User"], prefix="/users")
app.include_router(ProofRequestRouter, tags=["Circuit"], prefix="/proof_requests")

@app.on_event('startup')
async def startup():
  consumer_id = str(uuid.uuid4())
  loop = asyncio.get_running_loop()

  task = loop.create_task(pika_client.consume(consumer_id, 'proofs_queue', handle_proof_message, loop))
  await task
