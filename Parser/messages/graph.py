import json
from services.split_service import split

def handle_graph_message(body):
    payload = json.loads(body)
    split(payload.get('graph_url'))
