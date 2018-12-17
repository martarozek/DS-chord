import unittest
import xmlrpc.client

from util import get_url
from config import APP_PORT, APP_IP

rounds = 100


def get_client(address: str):
    return xmlrpc.client.ServerProxy(address)


class TestNode(unittest.TestCase):
    """Assumption: there is an app running."""

    def test_scenario(self):
        """Assumption: there are some nodes running,
        """
        app = get_url(APP_IP, APP_PORT)

        for i in range(rounds):
            res = get_client(app).get(f"key{i}")
            self.assertEqual(f"value{i}", res)


if __name__ == "__main__":
    unittest.main()
