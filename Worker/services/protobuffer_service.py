def jsonToProtobuff(data: str):
    return bytes(data, 'utf-8').decode("unicode_escape").encode()
