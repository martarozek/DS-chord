def user_input():
    get_or_put = ""
    while True:
        get_or_put = input("Get(g) or put(p)?: ").lower()
        if get_or_put == "exit":
            break
        if get_or_put == "g":
            key = input("What is the key? ")
            self.get(key)
        elif get_or_put == "p":
            key = input("What is the key? ")
            value = input("What is the value? ")
            self.put(key, value)
        else:
            print("Option not available. Try again.")
