import pika


AMQP_URL = 'amqps://mekfotvs:5cAFiGV-rHz2VWyi1K42EonlbfYihC4p@jackal.rmq.cloudamqp.com/mekfotvs'
GRAPHS_QUEUE = 'graphs_queue'

parameters = pika.URLParameters(AMQP_URL)

def publish_proof_request(message_body: str):
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue=GRAPHS_QUEUE)

    channel.basic_publish(exchange='',
                          routing_key=GRAPHS_QUEUE,
                          body=message_body)
    connection.close()
