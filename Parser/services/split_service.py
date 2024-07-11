import os
import json
from protobuffer.Circuit_pb2 import Circuit
from services.protobuffer_service import json_to_protobuff, protobuff_to_json
from services.queue_service import PikaClient

async def split(proof_request_id: str, graph: str):
    circuit = Circuit()
    circuit.ParseFromString(json_to_protobuff(graph))

    pika_client = PikaClient(os.environ.get('RABBITMQ_URL'))

    for i, layer in enumerate(circuit.layers):
        circuit_result = Circuit()
        circuit_result.layers.extend([layer])

        await pika_client.publish("chunks_queue", json.dumps({
            'proof_request_id': proof_request_id,
            'chunk_id': i,
            'chunk': protobuff_to_json(circuit_result.SerializeToString()),
        }))

    return None
