def get_key():
    key_to_get = input("The key? ")
    print(key_to_get)


def put_key_value():
    key_to_put = input("The key to put? ")
    value_to_put = input("The value to put? ")
    print("Key is: " + key_to_put + "value is" + value_to_put)


get_or_put = ""
while get_or_put != "exit":
        get_or_put = input("Get(g) or put(p)?: ").lower()
        if get_or_put == "g":
            get_key()
        elif get_or_put == "p":
            put_key_value()
        else:
            print("Option not available. Try again.")

