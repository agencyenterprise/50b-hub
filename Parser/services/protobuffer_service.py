def json_to_protobuff(data: str):
    return bytes(data, 'utf-8').decode("unicode_escape").encode()

def protobuff_to_json(data: bytes):
    return data.decode("unicode_escape")
