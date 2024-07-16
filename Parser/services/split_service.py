import os
import json
from protobuffer.Circuit_pb2 import Circuit
from services.protobuffer_service import json_to_protobuff, protobuff_to_json
from services.queue_service import PikaClient

async def split(proof_request_id: str, proof_provider: str, circuit_url: str):
    circuit = ""

    with open(circuit_url, "rb") as f:
        circuit = f.read()

    if proof_provider == "Dohko":
        await split_dohko(proof_request_id, proof_provider, circuit)
    else:
        await split_generic(proof_request_id, proof_provider, circuit)

    return None

async def split_dohko(proof_request_id: str, proof_provider: str, circuit: bytes):
    pika_client = PikaClient(os.environ.get('RABBITMQ_URL'))

    await pika_client.publish("chunks_queue", json.dumps({
        "proof_request_id": proof_request_id,
        "proof_provider": proof_provider,
        "chunk_id": 0,
        "chunk": protobuff_to_json(circuit),
    }))

async def split_generic(proof_request_id: str, proof_provider: str, circuit: bytes):
    circuit = Circuit()
    circuit.ParseFromString(json_to_protobuff(circuit))

    pika_client = PikaClient(os.environ.get('RABBITMQ_URL'))

    for i, layer in enumerate(circuit.layers):
        circuit_result = Circuit()
        circuit_result.layers.extend([layer])

        await pika_client.publish("chunks_queue", json.dumps({
            "proof_request_id": proof_request_id,
            "proof_provider": proof_provider,
            "chunk_id": i,
            "chunk": protobuff_to_json(circuit_result.SerializeToString()),
        }))
