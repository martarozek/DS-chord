import argparse
import sys
import threading
import time
from typing import Dict
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer

from util import generate_id, in_range, get_url
from config import LOGSIZE, SIZE


class Node:
    def __init__(self, ip: str, port: int, app_address: str = None) -> None:
        self.address = get_url(ip, port)
        self.ip = ip
        self.port = port
        self._id = generate_id(self.address)
        self._store = {}

        self._predecessor = ""
        self._finger = ["" for i in range(LOGSIZE)]

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

            if self._finger[0] == self.address:
                new_successor = self._predecessor
            else:
                successor = ServerProxy(self._finger[0])
                new_successor = successor.get_predecessor()

            if new_successor:
                new_id = generate_id(new_successor)
                old_id = generate_id(self._finger[0])

                if in_range(new_id, self._id, old_id, exclude_b=True):
                    self._finger[0] = new_successor

            if self._finger[0] == self.address:
                successor = self
            else:
                successor = ServerProxy(self._finger[0])

            # print(f"notifying {self._successor}")

            successor.notify(self.address)

    def _fix_fingers(self) -> None:
        next = 0
        while True:
            time.sleep(5)

            self._finger[next] = self.find_successor((self._id + 2**next) % SIZE)
            next = (next + 1) % LOGSIZE

    def get_predecessor(self) -> str:
        # print(f"get_predecessor, returning {self._predecessor}")
        return self._predecessor

    def notify(self, new_predecessor: str) -> bool:
        old_id = generate_id(self._predecessor)
        new_id = generate_id(new_predecessor)
        if not self._predecessor or in_range(new_id, old_id, self._id, exclude_b=True):
            self._predecessor = new_predecessor

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
        successor = self.address

        if self._finger[0] != self.address:
            successor_id = generate_id(self._finger[0])
            if in_range(id, self._id, successor_id):
                successor = self._finger[0]
            else:
                cpn_address = self.closest_preceding_node(id)
                cpn = ServerProxy(cpn_address)
                successor = cpn.find_successor(id)

        # print(f"find successor, returning: {successor}")
        return successor

    def closest_preceding_node(self, id: int) -> str:
        for i in range(LOGSIZE):
            finger = self._finger[LOGSIZE - i - 1]
            finger_id = generate_id(finger)
            if finger and in_range(finger_id, self._id, id, exclude_b=True):
                return finger
        return self.address

    def leave(self) -> None:
        app = ServerProxy(self._app)
        app.notify_leave(self.address)

        if self._predecessor and self._finger[0] != self.address:
            my_predecessor = ServerProxy(self._predecessor)
            my_predecessor.set_successor(self._finger[0])

            my_successor = ServerProxy(self._finger[0])
            my_successor.set_predecessor(self._predecessor)
            my_successor.takeover_store(self._store)

    def set_successor(self, address: str) -> str:
        self._finger[0] = address
        self._finger[0] = address

        return self._finger[0]

    def set_predecessor(self, address: str) -> str:
        self._predecessor = address

        return self._predecessor

    def takeover_store(self, store: Dict[str, str]) -> Dict[str, str]:
        self._store = {**self._store, **store}
        return self._store

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
        random_node = ServerProxy(ring_address)
        self._finger[0] = random_node.find_successor(self._id)
        # print(f"_join: {ring_address} {self._id} {self._successor}")

    def _create(self) -> None:
        self._finger[0] = self.address
        # print(f"_create: {self._id} {self._successor}")

    # diagnostics

    def get_id(self) -> int:
        return self._id

    def get_successor(self) -> (str, int):
        successor_id = generate_id(self._finger[0])
        return self._finger[0], successor_id

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
