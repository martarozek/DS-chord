import xmlrpc.client
from app import get, put

with xmlrpc.client.ServerProxy("http://127.0.0.1:8080/") as proxy:
    print(proxy.put(1, "2"))

get_or_put = ""

while True:
    get_or_put = input("Get(g) or put(p)?: ").lower()
    if get_or_put == "exit":
        break
    if get_or_put == "g":
        get()
    elif get_or_put == "p":
        put()
    else:
        print("Option not available. Try again.")
