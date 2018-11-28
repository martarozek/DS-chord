from util import *
from node import Node
import xmlrpc.client

address_1 = Address('localhost', 8000)
address_2 = Address('localhost', 8080)
address_3 = Address('localhost', 9000)


print(address_1.get_id())
print(address_2.get_id())
print(address_3.get_id())


node = xmlrpc.client.ServerProxy(address_1.get_merged())
node.put('marta', 'marios')
print(node.get('marta'))
