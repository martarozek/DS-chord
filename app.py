import random
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from util import Address

class App:
    def __init__(self, ip: str, port: int) -> None:
        random.seed()
        self.ip = ip
        self.port = port
        self.nodes = []

    def pick_random_node(self):
        if len(self.nodes) == 0:
            return None
        else:
            random_node_index = random.randint(0, len(self.nodes) - 1)
            return self.nodes[random_node_index]

    def get(self, key: str) -> str:
        random_node = self.pick_random_node()
        with xmlrpc.client.ServerProxy("http://" + random_node.ip + ":" + random_node.port) as client:
            return client.look_up() #looks for the node with this key

    def put(self, key: str, value: str) -> None:
        print("Key " + key + " is added to " +  value)
        random_node = self.pick_random_node()
        with xmlrpc.client.ServerProxy("http://" + random_node.ip + ":" + random_node.port) as client:
            return client.assign() #assigns key to value

    def request_join(self, ip: str, port: int) -> str:
        random_node = self.pick_random_node()
        return random_node.ip, random_node.port



    def user_input(self):
        get_or_put = ""
        while True:
            get_or_put = input("Get(g) or put(p)?: ").lower()
            if get_or_put == "exit":
                break
            if get_or_put == "g":
                key = input("What is the key? ")
                self.get(key)
            elif get_or_put == "p":
                key = input("What is the key? ")
                value = input("What is the value? ")
                self.put(key, value)
            else:
                print("Option not available. Try again.")


    server = SimpleXMLRPCServer(("127.0.0.1", 8080))
    server.register_function(put, get)
    server.register_introspection_functions()


if __name__ == "__main__":
    a = App("127.0.0.1", 8080)
    a.user_input()
    print(a.pick_random_node())
