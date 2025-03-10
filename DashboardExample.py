# Dashboard Example (PolyScope 5)
# more information can be found here:
# https://www.universal-robots.com/articles/ur/dashboard-server-e-series-port-29999/ 
# https://academy.universal-robots.com/video-tutorials/ 
### urscript secion
##### dashboard video

# import python libs for SocketTCP and time
import socket
import time

# initialize conection info
ROBOT_IP = "192.168.0.3"   # replace with the robot's IP adddress
DASHBOARD_PORT = 29999     # must be port 29999
DESIRED_URP = "leftright.urp"  # replace with the target .urp filename

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # open the connection
        s.connect((ROBOT_IP, DASHBOARD_PORT))

        # receive initial response
        response =s.recv(1024).decode()
        print(response)

        # check if in remote mode
        s.sendall("is in remote control\n".encode("utf-8"))
        response =s.recv(1024).decode()
        print("remote mode check: "+response)
        if ("false" in response):
            raise Exception("Robot is not in remote mode, exiting")

        # check safety status
        s.sendall("safetystatus\n".encode("utf-8"))
        response =s.recv(1024).decode()
        print("safety status check: "+response)
        if not("NORMAL" in response):
            raise Exception("Safety status must be addressed before proceeding")

        # check current arm power state
        s.sendall("robotmode\n".encode("utf-8"))
        response =s.recv(1024).decode()
        print(response)

        if not("RUNNING" in response): # need to turn on the arm
            
            # turn on the arm
            s.sendall("power on\n".encode("utf-8"))
            # wait for status == IDLE
            while not("IDLE" in response):
                s.sendall("robotmode\n".encode("utf-8"))
                response =s.recv(1024).decode()
                print(response)
                time.sleep(2.5)
            # send brake release command
            s.sendall("brake release\n".encode("utf-8"))
            # wait for status == POWER_ON
            while not("RUNNING" in response):
                s.sendall("robotmode\n".encode("utf-8"))
                response =s.recv(1024).decode()
                print(response)
                time.sleep(2.5)
        
        # now that arm is on, check the loaded program and load the right one
        s.sendall("get loaded program\n".encode("utf-8"))
        response =s.recv(1024).decode()
        print(response)
        while not(DESIRED_URP in response):
            s.sendall(("load "+DESIRED_URP+"\n").encode("utf-8"))
            response =s.recv(1024).decode()
            if (("File not found")in response):
                raise Exception(DESIRED_URP+": file could not be found")
            print(response)
            time.sleep(2.5)

        # send the play command
        s.sendall("play\n".encode("utf-8"))
        response =s.recv(1024).decode()
        print(response)

except Exception as e:
    print(f'an error occured: {e}')
