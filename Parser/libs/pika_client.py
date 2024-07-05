import aio_pika
import json

class PikaClient:
    def __init__(self, rabbit_url):
        self.rabbit_url = rabbit_url

    async def consume(self, queue_name, callback, loop):
        connection = await aio_pika.connect_robust(self.rabbit_url, loop=loop)
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name)

        async def process_incoming_message(message):
            body = message.body

            if body:
                await message.ack()
                callback(body)

        await queue.consume(process_incoming_message)

        return connection
    