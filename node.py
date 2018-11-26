import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import util
import sys


class Node:
    """ Main node class representing 
    a node in our system
    """

    def __init__(self, address: str, port: int, remote_address: str = None) -> None:
        self.address = address
        self.port = port

        # Set successor / predecessor
        # self.successor = None
        # self.predecessor = None

        # The Node upon initialization should seek 
        # to join a ring or create one
        self.join(remote_address)

    def look_up(self, key: str) -> None:
        return

    def join(self, remote_address: str) -> None:
        
        if remote_address:
            return
        else:
            return

        return

    def create(self) -> None:
        return

    def add(self, a: int, b: int) -> int:
        return a + b


"""
1. Initialize a node and a server
2. Register node instance to server
3. Server the server's main loop
4. Exit on Control-C 
"""


def run_server() -> None:
    n = Node("localhost", 8000)
    server = SimpleXMLRPCServer((n.address, n.port))
    server.register_instance(n)

    print("Serving XML-RPC on localhost port 8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)


if __name__ == "__main__":
    run_server()
