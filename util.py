import hashlib
from config import SIZE


class Protocol:
    HTTP = "http"
    HTTPS = "https"


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


def get_url(ip: str, port: int, https: bool = False) -> str:
    protocol = Protocol.HTTPS if https else Protocol.HTTP
    return f"{protocol}://{ip}:{port}"
