# stream multiline urscript file to robot
# robot must be in remote control mode

# adding this: junk=s.recv(1024) for good practice

import socket
import time
HOST = "192.168.0.3" #IP address of the robot
PORT = 30001   # port 30001 is primary client interface
# port 30002 for secondary client interface also works

# open the socket, print an error to the console if it doesnt work
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    junk=s.recv(1024)
    # Open the file in binary append mode to put in a last \n
    with open("multiline_script.script", "ab") as f:
        f.write(b'\n')
    # Now open the file in binary read mode and proceed to stream it
    with open("multiline_script.script", "rb") as f:
        abc = f.read(1024)
        while abc:
            s.sendall(abc)
            abc = f.read(1024)
    junk=s.recv(1024)
    s.close()
except socket.error as e:
    print(f"Connection failed: {e}")

try:
    junk=s.recv(1024)
except:
    # already closed
    junk = 1
s.close()
