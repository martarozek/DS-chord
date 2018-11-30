import argparse
import sys
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer

from util import generate_id, in_range, Address


class Node:
    def __init__(self, ip: str, port: int, app_address: str = None) -> None:
        self.address = Address(ip, port)
        self._id = self.address.get_id()
        self._store = {}

        self._successor = Address()
        self._predecessor = Address()

        self._app = app_address

        # start the stabilize and fixfingers daemons
        self._join_or_create(self._app)

    def get(self, key: str) -> str:
        node_address = self._look_up(key)

        if node_address == self.address.get_merged():
            return self._get(key)

        node = ServerProxy(node_address)
        return node.get(key)

    def put(self, key: str, value: str) -> str:
        node_address = self._look_up(key)

        if node_address == self.address.get_merged():
            return self._put(key, value)

        node = ServerProxy(node_address)
        return node.put(key, value)

    def find_successor(self, id: int) -> str:
        if not self._successor:
            return self.address.get_merged()

        successor_id = self._successor.get_id()
        if in_range(id, self._id, successor_id):
            return self._successor.get_merged()
        else:
            my_successor = ServerProxy(self._successor.get_merged())
            return my_successor.find_successor(id)

    # TBD
    def find_predecessor(self, id: str) -> str:
        return Address().get_merged()

    def _look_up(self, key: str) -> str:
        return self.find_successor(generate_id(key))

    def _get(self, key: str) -> str:
        if key in self._store:
            return self._store[key]
        return ""

    def _put(self, key: str, value: str) -> str:
        self._store[key] = value
        return self._store[key]

    def _join_or_create(self, app_address: str) -> None:
        if not app_address:
            print("Remote Address not specified! -- Find the app!")
        else:
            app = ServerProxy(app_address)

            ring_address = app.request_join(self.address.get_merged())
            if ring_address:
                self._join(ring_address)
            else:
                self._create()

    def _join(self, ring_address: str) -> None:
        random_node = ServerProxy(ring_address)
        self._successor = Address.from_merged(random_node.find_successor(self._id))

    def _create(self) -> None:
        print ("-- Ring Created -- Initial Node -- ")
        return

    def run_server(self) -> None:
        app = ServerProxy(self._app)
        app.confirm_join(self.address.get_merged())

        server = SimpleXMLRPCServer((self.address.ip, self.address.port))
        server.register_instance(self)
        server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a Chord node.")
    parser.add_argument(
        "--ip",
        type=str,
        default="localhost",
        required=False,
        help="ip address of the node",
    )
    parser.add_argument(
        "--port", type=int, default="8080", required=False,
        help="port of the node"
    )
    parser.add_argument(
        "--app",
        type=str,
        default="http://localhost:8000",
        required=False,
        help="address of the app, {protocol}://{ip}:{port}",
    )

    args = parser.parse_args()
    node = Node(args.ip, args.port, args.app)
    print(f"Serving XML-RPC on {node.address.ip} port {node.address.port}")

    try:
        node.run_server()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)
