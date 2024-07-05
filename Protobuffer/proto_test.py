import domain.Circuit_pb2 as Circuit
import google.protobuf.json_format as json_format

def addGate(layer, type, input1, input2, input3):
    gate = layer.gates.add()
    gate.ttype = type

    input0 = gate.inputs.add()
    input0.inputs.append(input1)

    input1 = gate.inputs.add()
    input1.inputs.append(input2)
    input1.inputs.append(input3)

circuit = Circuit.Circuit()
layer0 = circuit.layers.add()
layer1 = circuit.layers.add()

#   10
#    +
# 3     7
# addGate(layer0, Circuit.Gate.GateType.ADD, 10, 3, 7)

#   10          12
#    +          *
# 3     7   2       6
# addGate(layer0, Circuit.Gate.GateType.ADD, 10, 3, 7)
# addGate(layer0, Circuit.Gate.GateType.MUL, 12, 2, 6)

#      10                12
#       +                 *
#   3        7        2        6
#   +        +        +        *
# 1   2    3   4    1   1    2   3
addGate(layer0, Circuit.Gate.GateType.ADD, 10, 3, 7)
addGate(layer0, Circuit.Gate.GateType.MUL, 12, 2, 6)

addGate(layer1, Circuit.Gate.GateType.ADD, 3, 1, 2)
addGate(layer1, Circuit.Gate.GateType.ADD, 7, 3, 4)
addGate(layer1, Circuit.Gate.GateType.ADD, 2, 1, 1)
addGate(layer1, Circuit.Gate.GateType.MUL, 6, 2, 3)

value = circuit.SerializeToString().decode('utf-8')
print(json_format.MessageToJson(circuit))

circuit1 = Circuit.Circuit()
circuit1.ParseFromString(value.encode('utf-8'))

print(circuit1.layers[0].gates)
# print(circuit1.layers[1])

# print(circuit1.layers[0].layer[0].inputs[0])
# print(circuit1.layers[0].layer[0].inputs[1])
# print(circuit1.layers[0].layer[1].inputs[0])
# print(circuit1.layers[0].layer[1].inputs[1])

# print(circuit1.layers[1].layer[0].inputs[0])
# print(circuit1.layers[1].layer[0].inputs[1])
