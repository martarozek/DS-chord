import hashlib


# Simple SHA-1 hash function as mentioned in CHORD protocol paper
# @Parameters: id
# @Returns: hashed id
def hash_id(id):
    sha1 = hashlib.sha1()
    sha1.update(("%s" % (id)).encode("utf-8"))
    return sha1.hexdigest()
