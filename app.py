import random
import sys
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from util import Address
from node import Node

class App:
    def __init__(self, ip: str, port: int) -> None:
        random.seed()
        self.address = Address(ip, port)
        self.nodes = []

    def pick_random_node(self) -> str:
        if len(self.nodes) == 0:
            return ''
        else:
            random_node_index = random.randint(0, len(self.nodes) - 1)
            return self.nodes[random_node_index]

    def get(self, key: str) -> str:
        random_node = self.pick_random_node()
        with xmlrpc.client.ServerProxy(random_node) as client:
            return client.get(key) #looks for the node with this key

    def put(self, key: str, value: str) -> str:
        print("Key " + key + " is added to " +  value)
        random_node = self.pick_random_node()
        with xmlrpc.client.ServerProxy(random_node) as client:
            return client.put(key, value) #assigns key to value

    def request_join(self, address: str) -> str:
        return self.pick_random_node()

    def confirm_join(self, address: str) -> bool:
        self.nodes.append(address)
        return True

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



def run_server():
    app = App("localhost", 8080)
    server = SimpleXMLRPCServer((app.address.ip, app.address.port))
    server.register_instance(app)

    print("Serving XML-RPC on %s port %s" % (app.address.ip, app.address.port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)

if __name__ == "__main__":
    # app = App("127.0.0.1", 8080)
    # app.user_input()
    # print(app.pick_random_node())
    run_server()
