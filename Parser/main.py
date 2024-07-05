import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
import os
from libs.pika_client import PikaClient
from services.split_service import split

load_dotenv()
app = FastAPI()
pika_client = PikaClient(os.environ.get('RABBITMQ_URL'))

@app.get("/") 
async def main_route():
  return {"message": "Hey, It is me Parser: " + os.environ.get('RABBITMQ_URL')}

@app.on_event('startup')
async def startup():
  loop = asyncio.get_running_loop()

  def callback(body):
    # print(f" [x] Received {body}")
    split(body)


  task = loop.create_task(pika_client.consume('graphs_queue', callback, loop))
  await task
