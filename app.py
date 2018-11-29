import random
import sys
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer

from util import Address
from config import APP_PORT, APP_IP


class App:
    def __init__(self, ip: str, port: int) -> None:
        self._address = Address(ip, port)
        self._nodes = []
        random.seed()

    def get(self, key: str) -> str:
        random_node = self._pick_random_node()
        with ServerProxy(random_node) as node:
            return node.get(key)

    def put(self, key: str, value: str) -> str:
        random_node = self._pick_random_node()
        with ServerProxy(random_node) as node:
            return node.put(key, value)

    def request_join(self, address: str) -> str:
        return self._pick_random_node()

    def confirm_join(self, address: str) -> bool:
        self._nodes.append(address)
        return True

    def _pick_random_node(self) -> str:
        if len(self._nodes) == 0:
            return ""
        else:
            random_node_index = random.randint(0, len(self._nodes) - 1)
            return self._nodes[random_node_index]

    def run_server(self):
        server = SimpleXMLRPCServer((self._address.ip, self._address.port))
        server.register_function(self.get)
        server.register_function(self.put)
        server.register_function(self.request_join)
        server.register_function(self.confirm_join)
        print("Serving XML-RPC on %s port %s" % (app._address.ip, app._address.port))
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


if __name__ == "__main__":
    app = App(APP_IP, APP_PORT)
    app.run_server()
