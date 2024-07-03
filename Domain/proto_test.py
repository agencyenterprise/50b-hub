import generated.domain_pb2 as domain

log = domain.Log()
log.service = "test service"
log.instance = "test instance"

value = log.SerializeToString()

print(value)

log2 = domain.Log()
log2.ParseFromString(value)

print(log2.service)
print(log2.instance)