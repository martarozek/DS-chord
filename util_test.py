import unittest
import random
from typing import Generator
from util import hash_key, Address


class TestHashMethods(unittest.TestCase):
    @staticmethod
    def _get_random_bits() -> Generator[int, None, None]:
        size = random.randrange(1, 1000)

        for _ in range(size):
            yield random.getrandbits(8)

    def test_sha1_similar(self):
        """ Test Similar SHA-1 Inputs
        Tests sets of messages with 1 bit of difference. Ensures that all
        messages produce unique hashes.
        """

        first_msg = bytearray(self._get_random_bits())
        modified_msg = bytearray()

        # Pick a random byte, modify it by one bit
        byte_to_modify = random.randrange(0, len(first_msg))

        for i, byte in enumerate(first_msg):
            augmentor = 1 if i == byte_to_modify else 0
            modified_msg.append(byte + augmentor)

        first_digest = str(first_msg)
        modified_digest = str(modified_msg)

        first = hash_key(first_digest)
        modified = hash_key(modified_digest)

        self.assertNotEqual(first, modified)

    def test_sha1_repeatable(self):
        """ Test SHA-1 Repeatability
        Runs the SHA-1 hashing function multiple times to ensure the same
        outcome for any identical message input.
        """
        msg = bytearray(self._get_random_bits())
        first_digest = str(msg)
        second_digest = str(msg)

        first_digest = hash_key(first_digest)
        second_digest = hash_key(second_digest)

        self.assertEqual(first_digest, second_digest)


class TestAddress(unittest.TestCase):
    def test_get_merged(self):
        add = Address("localhost", 4242)

        merged = add.get_merged()

        self.assertEqual("http://localhost:4242", merged)

    def test_from_merged(self):
        merged = "http://localhost:4242"

        address = Address.from_merged(merged)

        self.assertEqual("localhost", address.ip)
        self.assertEqual(4242, address.port)


if __name__ == "__main__":
    unittest.main()
