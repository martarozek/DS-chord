import xmlrpc.client

s = xmlrpc.client.ServerProxy("http://localhost:8000")
print(s.add(2, 3))
