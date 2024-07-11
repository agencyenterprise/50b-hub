import json
from services.proof_service import generate_proof

async def handle_chunk_message(body, consumer_id):
    payload = json.loads(body)
    await generate_proof(consumer_id, payload.get("proof_request_id"), payload.get("chunk_id"), payload.get("chunk"))
