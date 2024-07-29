import json

async def handle_verification_message(body, consumer_id):
    payload = json.loads(body)
    print("request " + payload.get("proof_request_id"))
    print(payload.get("proof"))
    print(payload.get("verification"))
