import hashlib


# Simple SHA-1 hash function as mentioned in CHORD protocol paper
# @Parameters: ip -> actual IP of the server
# @Returns: hashed IP of the server as a unique identifier
def hash_ip(ip):
    sha1 = hashlib.sha1()
    sha1.update(("%s" % (ip)).encode("utf-8"))
    hashedip = sha1.hexdigest()
    return hashedip
