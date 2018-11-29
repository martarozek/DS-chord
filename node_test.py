from util import *
import xmlrpc.client


# Address tests based on id as well
address_1 = Address("localhost", 8001)
address_2 = Address("localhost", 8080)
address_3 = Address("localhost", 9000)


print(address_1.get_id())
print(address_2.get_id())
print(address_3.get_id())


# Functionality test for simple put/get into a node
node = xmlrpc.client.ServerProxy(address_1.get_merged())
node.put("marta", "marios")
print(node.get("marta"))


