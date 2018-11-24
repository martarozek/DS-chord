import hashlib


# Simple SHA-1 hash function as mentioned in CHORD protocol paper
# @Parameters: ip -> actual IP of the server
# @Returns: hashed IP of the server as a unique identifier
def hash_ip(ip):
    sha1 = hashlib.sha1()
    sha1.update(('%s' % (ip)).encode('utf-8'))
    hashedip = sha1.hexdigest()
    return hashedip


# Test SHA-1 hash function
def hash_test():
    # Test
    print (hash_ip('marios'))
    print (hash_ip('marta'))
    print (hash_ip('tasos'))
    print (hash_ip('davide'))

# Send Message
def send_msg(msg):
    return

# Return Message
def receive_msg():
    return




