import argparse
import sys
import threading
import time
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
        self._finger = {}

        self._app = app_address

        # threads change self._successor, self._predecessor and self._finger
        self._mutex = threading.Lock()

        stabilize = threading.Thread(target=self._stabilize, daemon=True)
        stabilize.start()

        fix_fingers = threading.Thread(target=self._fix_fingers, daemon=True)
        fix_fingers.start()

        self._join_or_create(self._app)

    def _stabilize(self) -> None:
        while True:
            time.sleep(5)

            self._mutex.acquire()

            if self._successor == self.address:
                new_successor = self._predecessor
            else:
                successor = ServerProxy(self._successor)
                new_successor = successor.get_predecessor()

            if new_successor:
                new_id = generate_id(new_successor)
                old_id = generate_id(self._successor)

                if in_range(new_id, self._id, old_id):
                    self._successor = new_successor

            if self._successor == self.address:
                successor = self
            else:
                successor = ServerProxy(self._successor)

            # print(f"notifying {self._successor}")

            self._mutex.release()

            successor.notify(self.address)

    def _fix_fingers(self) -> None:
        while True:
            time.sleep(0.5)

    def get_predecessor(self) -> str:
        # print(f"get_predecessor, returning {self._predecessor}")
        return self._predecessor

    def notify(self, new_predecessor: str) -> bool:
        self._mutex.acquire()

        old_id = generate_id(self._predecessor)
        new_id = generate_id(new_predecessor)
        if not self._predecessor or in_range(new_id, old_id, self._id):
            self._predecessor = new_predecessor

        self._mutex.release()
        # print(f"got notified, current predecessor {self._predecessor}")
        return True

    def get(self, key: str) -> str:
        node_address = self._look_up(key)

        if node_address == self.address:
            node = self
        else:
            node = ServerProxy(node_address)

        return node.get_final(key)

    def put(self, key: str, value: str) -> str:
        node_address = self._look_up(key)

        if node_address == self.address:
            node = self
        else:
            node = ServerProxy(node_address)

        return node.put_final(key, value)

    def find_successor(self, id: int) -> str:
        self._mutex.acquire()
        successor = self.address

        if self._successor != self.address:
            successor_id = generate_id(self._successor)
            if in_range(id, self._id, successor_id):
                successor = self._successor
            else:
                my_successor = ServerProxy(self._successor)
                successor = my_successor.find_successor(id)
        self._mutex.release()

        # print(f"find successor, returning: {successor}")
        return successor

    def closest_preceding_node(self, id: int) -> str:
        pass

    def leave(self) -> None:
        app = ServerProxy(self._app)
        app.notify_leave(self.address)

        self._mutex.acquire()
        if self._predecessor and self._successor != self.address:
            my_predecessor = ServerProxy(self._predecessor)
            my_predecessor.set_successor(self._successor)

            my_successor = ServerProxy(self._successor)
            my_successor.set_predecessor(self._predecessor)
        self._mutex.release()

    def set_successor(self, address: str) -> str:
        self._mutex.acquire()
        self._successor = address
        self._mutex.release()

        return self._successor

    def set_predecessor(self, address: str) -> str:
        self._mutex.acquire()
        self._predecessor = address
        self._mutex.release()

        return self._predecessor

    def _look_up(self, key: str) -> str:
        res = self.find_successor(generate_id(key))

        return res

    def get_final(self, key: str) -> str:
        # print(f"get {key}")
        if key in self._store:
            return self._store[key]
        return ""

    def put_final(self, key: str, value: str) -> str:
        # print(f"put {key} {value}")
        self._store[key] = value
        return self._store[key]

    def _join_or_create(self, app_address: str) -> None:
        app = ServerProxy(app_address)
        ring_address = app.request_join(self.address)

        if ring_address:
            self._join(ring_address)
        else:
            self._create()

    def _join(self, ring_address: str) -> None:
        self._mutex.acquire()
        random_node = ServerProxy(ring_address)
        self._successor = random_node.find_successor(self._id)
        self._mutex.release()
        # print(f"_join: {ring_address} {self._id} {self._successor}")

    def _create(self) -> None:
        self._mutex.acquire()
        self._successor = self.address
        self._mutex.release()
        # print("-- Ring Created -- Initial Node -- ")

    # diagnostics

    def get_id(self) -> int:
        return self._id

    def get_successor(self) -> (str, int):
        self._mutex.acquire()
        successor_id = generate_id(self._successor)
        self._mutex.release()
        return self._successor, successor_id

    def get_store(self) -> Dict[str, str]:
        return self._store

    def del_store(self) -> bool:
        self._store = {}
        return True

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
        node.leave()
        sys.exit(0)
