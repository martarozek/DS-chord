from util import *
from node import Node
import xmlrpc.client


# Address tests based on id as well
address_1 = Address("localhost", 8000)
address_2 = Address("localhost", 8080)
address_3 = Address("localhost", 9000)


print(address_1.get_id())
print(address_2.get_id())
print(address_3.get_id())


# Functionality test for simple put/get into a node
""" node = xmlrpc.client.ServerProxy(address_1.get_merged())
node.put("marta", "marios")
print(node.get("marta")) """



# Functionality test for -> Address.from_merged - function
address_new_1 = address_1.get_merged()
address_new_2 = address_1.from_merged(address_new_1)
# print (address_new_2.ip)