import xmlrpc.client

from config import APP_IP, APP_PORT

store = xmlrpc.client.ServerProxy((APP_IP, APP_PORT))
print(store.put("a", "b"))
