import sys
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer

from util import *
from configurations import *


class Node:
    """ Main node class representing 
    a node in our system
    """

    def __init__(self, address: str, port: int, remote_address: str = None) -> None:
        self.address = address
        self.port = port
        self.id = self.generate_id("%s:%s" % (self.address, str(self.port)))
        
        # Set successor / predecessor
        # self.successor = None
        # self.predecessor = None

        # The Node upon initialization should seek
        # to join a ring or create one
        self.join(remote_address)

    def generate_id(self, value: str) -> str:
        return int(hash_id(value), 16) % SIZE

    def look_up(self, key: str) -> None:
        return

    def join(self, remote_address: str) -> None:
        # My logic here is the following:
        # The remote_address is the app.py
        # You request from the app, an ip+port so you can join an existing ring or create a new
        # Otherwise, you cannot join
        if remote_address:
            proxy = xmlrpc.client.ServerProxy(remote_address)
            # ring_address = proxy.request_join(self.address, self.port) not implemented yet
            ring_address = "http://localhost:8000/"
            if ring_address:
                print(proxy.add(3, 2))
            else:
                self.create()
        else:
            return

        return

    def create(self) -> None:
        return

    # Trivial function only for testing server/client calls
    def add(self, a: int, b: int) -> int:
        return a + b


"""
1. Initialize a node and a server
2. Register node instance to server
3. Server the server's main loop
4. Exit on Control-C 
"""


def run_server() -> None:
    if len(sys.argv) < 3:
        n = Node("localhost", 8000)
    elif len(sys.argv) == 3:
        n = Node(sys.argv[1], int(sys.argv[2]))
    elif len(sys.argv) == 4:
        # Most common case -> you give a localhost and a port as your "joining address"
        # The third argument is the app.py address + port where you ask to join a ring
        n = Node(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    else:
        print("\nInvalid number of arguments")
        sys.exit(0)

    server = SimpleXMLRPCServer((n.address, n.port))
    server.register_instance(n)

    print("Serving XML-RPC on localhost port %s" % n.port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)


if __name__ == "__main__":
    run_server()
