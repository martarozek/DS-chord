def getKey():
    keyToGet = input("The key? ")
    print(keyToGet)


def putKeyValue():
    keyToPut = input("The key to put? ")
    valueToPut = input("The value to put? ")
    print("Key is: " + keyToPut + "value is" + valueToPut)


get_or_put = ""
while get_or_put != "exit":
        get_or_put = input("Get(g) or put(p)?: ").lower()
        if get_or_put == "g":
            getKey()
        elif get_or_put == "p":
            putKeyValue()
        else:
            print("Option not available. Try again.")

