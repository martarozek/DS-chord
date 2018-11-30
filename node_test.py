import unittest
import xmlrpc.client

from util import get_url
from config import APP_PORT, APP_IP


def get_client():
    app_address = get_url(APP_IP, APP_PORT)

    return xmlrpc.client.ServerProxy(app_address)


class TestNode(unittest.TestCase):
    """Assumption: there is an app running."""

    def test_scenario(self):
        res = get_client().put("key", "value")
        self.assertEqual("value", res)

        res = get_client().get("key")
        self.assertEqual("value", res)

        res = get_client().put("blue", "orange")
        self.assertEqual("orange", res)

        res = get_client().get("key")
        self.assertEqual("value", res)

        res = get_client().get("blue")
        self.assertEqual("orange", res)


if __name__ == "__main__":
    unittest.main()
