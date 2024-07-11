import json
from services.split_service import split

async def handle_graph_message(body, consumer_id):
    payload = json.loads(body)
    await split(payload.get("proof_request_id"), payload.get("graph_url"))
