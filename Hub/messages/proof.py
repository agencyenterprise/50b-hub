import json

async def handle_proof_message(body, consumer_id):
    payload = json.loads(body)
    print(payload.get("proof_request_id"))
    print(payload.get("chunk_id"))
    print(payload.get("proof"))
