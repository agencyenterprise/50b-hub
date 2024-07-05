from protobuffer.Circuit_pb2 import Circuit

def split(graph: str):
    print(graph)
    circuit = Circuit()
    circuit.ParseFromString(graph)

    print(circuit.layers[0])

    return None
