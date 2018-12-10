import random
import sys
from typing import List
from xmlrpc.client import ServerProxy, Fault
from xmlrpc.server import SimpleXMLRPCServer

from util import get_url
from config import APP_PORT, APP_IP, _DEBUG
from spawn_node import get_ip_port


class App:
    def __init__(self, ip: str, port: int) -> None:
        self._address = get_url(ip, port)
        self.ip = ip
        self.port = port
        self._nodes = []
        random.seed()

    def get(self, key: str) -> str:
        random_node = self._pick_random_node()
        if not random_node:
            raise Fault(500, "No nodes available")

        with ServerProxy(random_node) as node:
            # print(f"get {key}, node: {random_node}")
            return node.get(key)

    def put(self, key: str, value: str) -> str:
        random_node = self._pick_random_node()
        if not random_node:
            raise Fault(500, "No nodes available")

        with ServerProxy(random_node) as node:
            # print(f"put {key} {value}, node: {random_node}")
            return node.put(key, value)

    def request_join(self, address: str) -> str:
        return self._pick_random_node()

    def confirm_join(self, address: str) -> bool:
        self._nodes.append(address)
        return True

    def notify_leave(self, address: str) -> bool:
        if address in self._nodes:
            self._nodes.remove(address)
            return True
        return False

    def _pick_random_node(self) -> str:
        if len(self._nodes) == 0:
            return ""
        else:
            random_node_index = random.randint(0, len(self._nodes) - 1)
            return self._nodes[random_node_index]

    # diagnostics

    def get_nodes(self) -> List[str]:
        return self._nodes

    # end diagnostics

    def run_server(self):
        server = SimpleXMLRPCServer((self.ip, self.port))

        server.register_instance(self)

        server.serve_forever()


if __name__ == "__main__":
    # DAS 4 Config
    # app = App(APP_IP, APP_PORT)

    if _DEBUG:
        app = App(APP_IP, APP_PORT)
    else:
        ip, port = get_ip_port()
        f = open("app.out", "w+")
        f.write(f"http://{ip}:{port}")
        f.close()
        app = App(ip, int(port))

    # print(f"Serving App on {APP_IP} port {APP_PORT}")
    try:
        app.run_server()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)
