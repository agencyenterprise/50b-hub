import base64

def json_to_protobuff(data: str):
    return base64.b64decode(data)

def protobuff_to_json(data: bytes):
    return base64.b64encode(data).decode()
