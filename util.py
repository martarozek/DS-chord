import hashlib
from config import SIZE

# Simple SHA-1 hash function as mentioned in CHORD protocol paper
# @Parameters: id
# @Returns: hashed id
def hash_id(id: str) -> str:
    sha1 = hashlib.sha1()
    sha1.update(("%s" % (id)).encode("utf-8"))
    return sha1.hexdigest()

def generate_id(key: str) -> int:
    return int(hash_id(key), 16) % SIZE


class Address:
    def __init__(self, ip: str='', port: int=0) -> None:
        self.ip = ip
        self.port = port

    def get_merged(self, https=False) -> str:
        protocol = "https" if https else "http"
        return f"{protocol}://{self.ip}:{self.port}"

    @staticmethod
    def from_merged(combined_address: str) -> 'Address':
        new_set = ''
        if "http" in combined_address:
            new_set = combined_address.replace("http://", "")
        else:
            new_set = combined_address.replace("https://", "")
        splitter = new_set.split(":")
        return Address(splitter[0], int(splitter[1]))

    def is_empty(self) -> bool:
        return not self.ip

    def get_id(self) -> int:
        if not self.ip:
            return None
        return generate_id(self.get_merged())

    def __eq__(self, other) -> bool:
        return self.ip == other.ip and self.port == other.port

