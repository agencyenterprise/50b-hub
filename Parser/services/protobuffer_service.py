def json_to_protobuff(data: str):
    return bytes(data, 'utf-8').decode("unicode_escape").encode()
