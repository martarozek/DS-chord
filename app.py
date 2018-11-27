import random
from xmlrpc.server import SimpleXMLRPCServer


ip = ""
nodes = []


def pick_random_node():
    if len(nodes) == 0:
        return "Null"
    random_node_index = random.randint(1, len(nodes))
    print(nodes[random_node_index])


def get(key: int) -> str:
    return ip


def put(key: int, value: str) -> None:
    print("Key is added to value")


def request_join(ip: str, port: int) -> str:
    if nodes:
        return pick_random_node()
    else:
        return "None"


class NodeInfo:
    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port


server = SimpleXMLRPCServer(("127.0.0.1", 8080))
server.register_function(put, "put")
server.register_introspection_functions()
