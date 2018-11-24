import unittest
import random
from util import hash_id


class TestHashMethods(unittest.TestCase):
    def test_sha1_similar(self):
        """ Test Similar SHA-1 Inputs
        Tests sets of messages with 1 bit of difference. Ensures that all
        messages produce unique hashes.
        """

        first_msg = bytearray(get_random_bytes())
        modified_msg = bytearray()

        # Pick a random byte, modify it by one bit
        byte_to_modify = random.randrange(0, len(first_msg))

        for i, byte in enumerate(first_msg):
            augmentor = 1 if i == byte_to_modify else 0
            modified_msg.append(byte + augmentor)

        first_digest = bytes(first_msg)
        modified_digest = bytes(modified_msg)

        first = hash_id(first_digest)
        modified = hash_id(modified_digest)

        self.assertNotEqual(first, modified)

    def test_sha1_repeatable(self):
        """ Test SHA-1 Repeatability
        Runs the SHA-1 hashing function multiple times to ensure the same
        outcome for any identical message input.
        """
        msg = bytearray(get_random_bytes())
        first_digest = bytes(msg)
        second_digest = bytes(msg)

        first_digest = hash_id(first_digest)
        second_digest = hash_id(second_digest)

        self.assertEqual(first_digest, second_digest)


def get_random_bytes():
    """Get Random Bytes
    Generates a sequence of random bits of a random size between 1 and 1000
    bits in the sequence.
    Returns:
        A stream of random bytes.
    """
    size = random.randrange(1, 1000)

    for _ in range(size):
        yield random.getrandbits(8)


if __name__ == "__main__":
    unittest.main()
