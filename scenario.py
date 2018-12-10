import argparse
import random, string
from xmlrpc.client import ServerProxy
from util import get_url
from config import APP_PORT, APP_IP, _DEBUG
from spawn_node import get_ip_port

# function for create a random value
def randomword():
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(10))


def scenario(app, get_num: int, put_num: int) -> None:
    for i in range(put_num):
        app.put(i, randomword())
    
    with open("scenario.txt", 'w+') as output:
        for i in range(get_num):
            output.write(f"{i} value = {app.get(i)}\n")
    output.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start new test setting the scenario.")
    parser.add_argument(
        "--get", type=int, default=0, required=False, help="number of the get calls"
    )
    parser.add_argument(
        "--put", type=int, default=0, required=False, help="number of put calls"
    )

    if _DEBUG:
        args = parser.parse_args()
        app = ServerProxy(get_url(APP_IP, APP_PORT))
        scenario(app, args.get, args.put)
    else:    
        # READ FILE FOR APP IP+PORT
        f = open("app.out", "r")
        app_address = f.readline()
        f.close()
        print(app_address)

        args = parser.parse_args()
        app = ServerProxy(app_address)
        scenario(app, args.get, args.put)

