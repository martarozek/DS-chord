import hashlib


# Simple SHA-1 hash function as mentioned in CHORD protocol paper
# @Parameters: id
# @Returns: hashed id
def hash_id(id: str) -> str:
    sha1 = hashlib.sha1()
    sha1.update(("%s" % (id)).encode("utf-8"))
    return sha1.hexdigest()


class Address:
    def __init__(self, ip: str, port: int) -> None:
        self.ip = ip
        self.port = port

    def get_merged(self, https=False) -> str:
        protocol = "https" if https else "http"
        return f"{protocol}://{self.ip}:{self.port}"
