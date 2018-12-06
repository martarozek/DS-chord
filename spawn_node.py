import sys
import subprocess
import socket



param1 = ["--ip", "localhost"]
param2 = ["--port", "8080"]
# subprocess.call(["python","node.py"] + param1 + param2, shell=False)

subprocess.Popen(['python', 'param1', 'param2'])
print(socket.gethostname())
print(socket.gethostbyaddr())