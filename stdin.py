from xmlrpc.client import ServerProxy

from util import get_url
from config import APP_PORT, APP_IP


if __name__ == "__main__":
    app = ServerProxy(get_url(APP_IP, APP_PORT))
    while True:
        get_or_put = input("Get(g) or put(p)?: ").lower()
        if get_or_put == "exit":
            break
        if get_or_put == "g":
            key = input("What is the key? ")
            print(app.get(key))
        elif get_or_put == "p":
            key = input("What is the key? ")
            value = input("What is the value? ")
            print(app.put(key, value))
        else:
            print("Option not available. Try again.")
