import unittest
import xmlrpc.client

from util import get_url, generate_id
from config import APP_PORT, APP_IP

app = get_url(APP_IP, APP_PORT)


def get_client(address: str):
    return xmlrpc.client.ServerProxy(address)


class TestNode(unittest.TestCase):
    """Assumption: there is an app running."""

    def test_scenario(self):
        """Assumption: there are two nodes running,
        localhost:8042, localhost:8044
        """

        res = get_client(app).get_nodes()
        self.assertCountEqual(["http://localhost:8042", "http://localhost:8044"], res)

        # res = get_client('http://localhost:8042').get_successor()
        # self.assertEqual(('http://localhost:8044', 18), res)
        # res = get_client('http://localhost:8044').get_successor()
        # self.assertEqual(('http://localhost:8042', 33), res)

        res = get_client(app).put("key", "value")
        self.assertEqual("value", res)

        res = get_client(app).get("key")
        self.assertEqual("value", res)

        key_id = generate_id("key")
        self.assertEqual(30, key_id)
        self.assertEqual(33, generate_id("http://localhost:8042"))
        self.assertEqual(18, generate_id("http://localhost:8044"))

        res = get_client("http://localhost:8042").get_store()
        self.assertEqual({"key": "value"}, res)

        res = get_client("http://localhost:8044").get_store()
        self.assertEqual({}, res)

        # second put/get
        res = get_client(app).put("apple", "banana")
        self.assertEqual("banana", res)

        res = get_client(app).get("apple")
        self.assertEqual("banana", res)

        key_id = generate_id("apple")
        self.assertEqual(0, key_id)

        # res = get_client('http://localhost:8042').get_store()
        # self.assertEqual({'key': 'value'}, res)
        #
        # res = get_client('http://localhost:8044').get_store()
        # self.assertEqual({'apple': 'banana'}, res)


if __name__ == "__main__":
    unittest.main()
