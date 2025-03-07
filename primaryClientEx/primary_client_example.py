# sample usage of UR Primary Client Interface 
# https://docs.universal-robots.com/tutorials/communication-protocol-tutorials/primary-secondary-guide.html
import socket
import time
HOST = "192.168.0.3"  # SET YOUR ROBOTS'S IP ADDRESS HERE
PORT = 30001          # use port 30002 instead for Secondary Client Interface

# This sample pulses digital out 7 on and off at 1Hz
while(True):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    myURScript = "set_digital_out(7, True)" + "\n"
    s.send((myURScript).encode())
    data = s.recv(1024)
    s.close()
    print ("Received", repr(data))
    time.sleep(1)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    myURScript = "set_digital_out(7, False)" + "\n"
    s.send((myURScript).encode())
    data = s.recv(1024)
    s.close()
    print ("Received", repr(data))
    time.sleep(1)



