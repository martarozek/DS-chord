import sys
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer

from util import hash_id, generate_id, Address
from config import SIZE


class Node:
    """ Main node class representing 
    a node in our peer-2-peer system
    """

    def __init__(self, ip: str, port: int, remote_address: str = None) -> None:
        self.address = Address(ip, port)
        self.id = self.address.get_id()

        # Set successor / predecessor
        self.successor = Address()
        # self.predecessor = None

        # Key value store
        self._store = {}

        # The Node upon initialization should seek
        # to join a ring or create one
        self._join(remote_address)

    # Client gives you a key
    #
    def look_up(self, key: str) -> str:
        id = generate_id(key)

        return  self.find_successor(id)

    def get(self, key: str) -> str:
        node_address = self.look_up(key)
        node = xmlrpc.client.ServerProxy(node_address.get_merged())

        return node._get(key)

    def put(self, key: str, value: str) -> None:
        node_address = self.look_up(key)
        node = xmlrpc.client.ServerProxy(node_address.get_merged())

        node._put(key, value)

    def _get(self, key: str) -> str:
        if key in self._store:
            return self._store[key]
        return None

    def _put(self, key: str, value: str) -> None:
        self._store[key] = value

    def in_range(self, id: int, a: int, b: int) -> bool:
        if a < b:
            return id > a and id <= b
        return id > a or id <= b

    def find_successor(self, id: str) -> Address:

        if not self.successor:
            return self.address

        succ_id = self.successor.get_id()
        if self.in_range(id, self.id, succ_id):
            return self.successor
        else:
            node = xmlrpc.client.ServerProxy(self.successor.get_merged())
            return node.find_successor(id)

    def find_predecessor(self, id: str) -> "Node":
        return

    def _join(self, remote_address: str) -> None:
        # My logic here is the following:
        # The remote_address is the app.py
        # You request from the app, an ip+port so you can join an existing ring or create a new
        # Otherwise, you cannot join
        if remote_address:
            app = xmlrpc.client.ServerProxy(remote_address)

            # Get a Node's address from the APP
            ring_address = app.request_join(self.address)
            # ring_address = "http://localhost:8000/"
            if ring_address:
                # Join
                node = xmlrpc.client.ServerProxy(ring_address.get_merged())
                self.successor = node.find_successor(self.id)
            else:
                self._create()
        else:
            return

        return

    # In case a node joins or creates a ring
    # It should send a confirmation to the APP
    def _create(self) -> None:
        # Message the APP
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

    server = SimpleXMLRPCServer((n.address.ip, n.address.port))
    server.register_instance(n)

    print("Serving XML-RPC on %s port %s" % (n.address.ip, n.address.port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)


if __name__ == "__main__":
    run_server()
