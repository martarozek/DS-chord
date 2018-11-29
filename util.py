import hashlib
from config import SIZE


def hash_key(key: str) -> str:
    sha1 = hashlib.sha1()
    sha1.update(f"{key}".encode("utf-8"))
    return sha1.hexdigest()


def generate_id(key: str) -> int:
    return int(hash_key(key), 16) % SIZE


def in_range(id: int, a: int, b: int) -> bool:
    if a < b:
        return a < id <= b
    return id > a or id <= b


class Protocol:
    HTTP = "http"
    HTTPS = "https"


class Address:
    def __init__(self, ip: str = "", port: int = 0) -> None:
        self._ip = ip
        self._port = port

    @classmethod
    def from_merged(cls: "Address", merged: str) -> "Address":
        proto = Protocol.HTTP if Protocol.HTTP in merged else Protocol.HTTPS
        merged = merged.replace(f"{proto}://", "")
        split = merged.split(":")
        return Address(split[0], int(split[1]))

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def is_empty(self) -> bool:
        return not self._ip

    def __str__(self):
        return self.get_merged()

    def __bool__(self):
        return not self.is_empty

    def get_merged(self, https=False) -> str:
        protocol = Protocol.HTTPS if https else Protocol.HTTP
        return f"{protocol}://{self._ip}:{self._port}"

    def get_id(self) -> int:
        if not self._ip or not self._port:
            return 0
        return generate_id(self.get_merged())

    def __eq__(self, other) -> bool:
        return self._ip == other.ip and self._port == other.port
