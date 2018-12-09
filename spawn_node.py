import sys
import subprocess
import socket



param1 = ["--ip", "localhost"]
param2 = ["--port", "8080"]
# subprocess.call(["python","node.py"] + param1 + param2, shell=False)

# subprocess.Popen(['python', 'param1', 'param2'])
# print(socket.gethostname())
# print(socket.gethostbyaddr(socket.gethostname()))

def get_ip_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
        PORT = str(s.getsockname()[1])
    except:
        IP = '127.0.0.1'
        PORT = '8080'
    finally:
        s.close()
    return IP, PORT



def spawn_node():
    f = open("app.out", "r")
    app_address = f.readline()
    f.close()
    print(app_address)


    print (get_ip_port())
    ip, port = get_ip_port()
    print(ip)
    print(port)

    param1 = ["--ip", ip]
    param2 = ["--port", port]
    param3 = ["--app", app_address]

    subprocess.call(["python3","application/node.py"] + param1 + param2 + param3, shell=False)


if __name__ == "__main__":
    spawn_node()
