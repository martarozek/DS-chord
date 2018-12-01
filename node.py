import argparse
import sys
from typing import Dict
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer

from util import generate_id, in_range, get_url


class Node:
    def __init__(self, ip: str, port: int, app_address: str = None) -> None:
        self.address = get_url(ip, port)
        self.ip = ip
        self.port = port
        self._id = generate_id(self.address)
        self._store = {}

        self._successor = ""
        self._predecessor = ""

        self._app = app_address

        # start the stabilize and fixfingers daemons
        self._daemons = []
        self._join_or_create(self._app)

    def _stabilize(self) -> None:
        # x = successor.predecessor
        x = self._successor
        if not x:
            return

        succ = ServerProxy(x)
        pred = succ._stabilize_get_successors_predecessor()
        if pred:
            pred_id = generate_id(pred)

            if pred_id == self._id:
                return
            if in_range(pred_id, self._id, generate_id(self._successor)):
                return
        return

    def _stabilize_get_successors_predecessor(self) -> str:
        if self._predecessor:
            return self._predecessor
        print("STABILIZE_GET_SUCCESSORS_PREDECESSOR = PREDECESSOR NOT FOUND")
        return ""

    def get(self, key: str) -> str:
        node_address = self._look_up(key)

        if node_address == self.address:
            return self._get(key)

        node = ServerProxy(node_address)
        return node.get(key)

    def put(self, key: str, value: str) -> str:
        node_address = self._look_up(key)

        if node_address == self.address:
            return self._put(key, value)

        node = ServerProxy(node_address)
        return node.put(key, value)

    def find_successor(self, id: int) -> str:
        if not self._successor:
            print(f"find successor, returning self: {self.address}")
            return self.address

        successor_id = generate_id(self._successor)
        if in_range(id, self._id, successor_id):
            return self._successor
        else:
            my_successor = ServerProxy(self._successor)
            return my_successor.find_successor(id)

    # TBD
    def find_predecessor(self, id: str) -> str:
        return ""

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

            ring_address = app.request_join(self.address)
            if ring_address:
                self._join(ring_address)
            else:
                self._create()

    def _join(self, ring_address: str) -> None:
        random_node = ServerProxy(ring_address)
        self._successor = random_node.find_successor(self._id)
        print(f"_join: {ring_address} {self._id} {self._successor}")

    def _create(self) -> None:
        print("-- Ring Created -- Initial Node -- ")
        return

    # diagnostics

    def get_id(self) -> int:
        return self._id

    def get_successor(self) -> (str, int):
        return self._successor, generate_id(self._successor)

    def get_store(self) -> Dict[str, str]:
        return self._store

    # end diagnostics

    def run_server(self) -> None:
        app = ServerProxy(self._app)
        app.confirm_join(self.address)

        server = SimpleXMLRPCServer((self.ip, self.port))
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
        "--port", type=int, default="8080", required=False, help="port of the node"
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
    print(f"Serving Node on {args.ip} port {args.port}")

    try:
        node.run_server()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)
