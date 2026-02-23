# testing usage of the robot api via the robot_api_ex4 module 

import robot_api_ex4 as ur_api
import time
import pprint

ip_addr = '192.168.0.13'
myrobot = ur_api.robot_api(ip_addr)


# examples of getting information from the robot
print(myrobot.get_system_time().json())
time.sleep(0.1)
pprint.pprint(myrobot.get_all_modes())
time.sleep(0.1)
loaded_program = myrobot.get_loaded_program()
print(f"loaded program: {loaded_program.json()['name']}")
print(f"loaded program: {loaded_program.json()}")
time.sleep(0.1)
all_programs = myrobot.get_loaded_program_names()
print(f"all loaded programs : ")
pprint.pprint(all_programs.json())
time.sleep(0.1)

input("press enter to continue to upload urpx test...")
myrobot.upload_specific_urpx("def456",function_print_info=True)
time.sleep(0.1)
print(f"all loaded programs : ")
pprint.pprint(all_programs.json())
time.sleep(0.1)

# download the loaded urpx
input("press enter to download the currently loaded urpx file...")
file_name = loaded_program.json()['name']
myResult = myrobot.get_specific_urpx(file_name)
pprint.pprint(myResult.json())
# output_file_name = f"{file_name}_downloaded.urpx"
# with open(output_file_name, 'wb') as f:
#     f.write(myResult.content)
#     # known issue: the file is renamed on the PC, but when loaded to the robot, it still shows the original name

