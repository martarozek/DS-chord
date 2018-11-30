from xmlrpc.client import ServerProxy

from util import Address
from config import APP_PORT, APP_IP


def user_input(app):
    get_or_put = ""
    while True:
        get_or_put = input("Get(g) or put(p)?: ").lower()
        if get_or_put == "exit":
            break
        if get_or_put == "g":
            key = input("What is the key? ")
            print(type(key))
            return app.get(key)
        elif get_or_put == "p":
            key = input("What is the key? ")
            value = input("What is the value? ")
            return app.put(key, value)
        else:
            print("Option not available. Try again.")

if __name__ == '__main__':
    add = Address(APP_IP, APP_PORT)
    app = ServerProxy(add.get_merged())
    user_input(app)