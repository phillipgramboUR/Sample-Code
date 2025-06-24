# Dashboard Example (PolyScope 5)
# specifically for resetting a protective stop
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
            print("safety status isnt NORMAL, response is: "+response)
            # check if in protective stop
            if("PROTECTIVE_STOP" in response):
                # close popup
                s.sendall("close safety popup\n".encode("utf-8"))
                response =s.recv(1024).decode()
                print("closing safety popup, command sent, response is: "+response)
                time.sleep(0.1)
                # unlock protective stop
                s.sendall("unlock protective stop\n".encode("utf-8"))
                response =s.recv(1024).decode()
                print("p-stop unlocking, command sent, response is: "+response)
                # see if it is working
                if not("Protective stop releasing" in response):
                    raise Exception("error releasing protective stop: "+response)
                else:
                    while not("NORMAL" in response):
                        s.sendall("safetystatus\n".encode("utf-8"))
                        response =s.recv(1024).decode()
                        time.sleep(0.1)

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

                        # Uncoment the below to play the program 
                        # send the play command
                        # s.sendall("play\n".encode("utf-8"))
                        # response =s.recv(1024).decode()
                        # print(response)

            else:
                raise Exception("safety isnt normal, but not in a protective stop: "+response)
        



except Exception as e:
    print(f'an error occured: {e}')
