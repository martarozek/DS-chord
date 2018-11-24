import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import util
import sys


class node:
    """ Main node class representing 
    a node in our system
    """

    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port

    def look_up(self) -> None:
        return

    def join(self) -> None:
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


def runServer() -> None:
    n = node("localhost", 8000)
    server = SimpleXMLRPCServer((n.ip, n.port))
    server.register_instance(n)

    print("Serving XML-RPC on localhost port 8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)


if __name__ == "__main__":
    runServer()
