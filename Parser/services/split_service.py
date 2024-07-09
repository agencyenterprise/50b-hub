from protobuffer.Circuit_pb2 import Circuit
from services.protobuffer_service import json_to_protobuff

def split(graph: str):
    circuit = Circuit()
    circuit.ParseFromString(json_to_protobuff(graph))

    print(len(circuit.layers))

    for i, layer in enumerate(circuit.layers):
        print(i)
    # print(circuit.layers[0].gates[0])

    return None
