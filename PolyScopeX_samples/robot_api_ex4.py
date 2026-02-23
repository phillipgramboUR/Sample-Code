# ##########################
# Universal Robots Robot API
# Phillip Grambo | pgra@universal-robots.com | Jan 2026
# requires 'requests' package, do so with:
# pip install requests
# 
# https://www.universal-robots.com/articles/ur/release-notes/release-note-software-version-1011x/
# you can verify API docs on the robot by going to  http://[ROBOT-IP]/universal-robots/robot-api/docs in a broswer
# based on the docs for polyscopeX v10.12
##########################

# imports
import requests
import time
import pprint
import os


# define class object for robot API
class robot_api:
    def __init__(self, IPADDR, object_print_info=False):
        self.ROBOT_IP_ADDR = IPADDR
        self.object_print_info = object_print_info 
        # object_print_info is for dumping info to console. useful for debugging/testing but unwanted in production
        

        # url components
        # base url
        self.BASE_URL = f"http://{self.ROBOT_IP_ADDR}/universal-robots/robot-api"

        # license domain
        self.LICENSE_DOMAIN = "/license/v1/license/"

        # system domains
        self.SYSTEM_TIME_DOMAIN = "/system/v1/system-time"
        self.SYSTEM_OPERATING_MODE_DOMAIN = "/system/v1/operationalmode"
        self.SYSTEM_CONTROL_MODE_DOMAIN = "/system/v1/controlmode"

        # state domains
        self.STATE_DOMAIN = "/robotstate/v1/state"
        self.SAFETY_MODE_DOMAIN = "/robotstate/v1/safetymode"
        self.ROBOT_MODE_DOMAIN = "/robotstate/v1/robotmode"

        # program domains
        self.PROGRAM_DOMAIN = "/program/v1/state"
        self.PROGRAM_LOADED_DOMAIN = "/program/v1/loaded"

        # programs domain
        self.PROGRAMS_DOMAIN = "/programs/v1/"

    # function for toggleable printing to console
    def print_results(self, data, print_info=None):
        if print_info is None:
            print_info = self.object_print_info
        if print_info:
            if isinstance(data, dict):
                pprint.pprint(data)
            else:
                print(data)

    ############################################
    # ----- define functions for actions ----- #
    ############################################

    ############################################    
    # system domain actions
    def get_system_time(self, function_print_info=None):
        # gets the current system time on the robot
        if function_print_info is None:
            function_print_info = self.object_print_info
        url = f"{self.BASE_URL}{self.SYSTEM_TIME_DOMAIN}"
        response = requests.get(url)
        self.print_results(f"Get System Time - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def get_operating_mode(self, function_print_info=None):
        # should return either MANUAL or AUTOMATIC
        if function_print_info is None:
            function_print_info = self.object_print_info
        url = f"{self.BASE_URL}{self.SYSTEM_OPERATING_MODE_DOMAIN}"
        response = requests.get(url)
        self.print_results(f"Get Operating Mode - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def get_control_mode(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        # should return either LOCAL or REMOTE
        url = f"{self.BASE_URL}{self.SYSTEM_CONTROL_MODE_DOMAIN}"
        response = requests.get(url)
        self.print_results(f"Get Control Mode - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response


    ############################################    
    # state domain actions
    def power_on(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        url = f"{self.BASE_URL}{self.STATE_DOMAIN}"
        payload = {"action": "POWER_ON"}
        response = requests.put(url, json=payload)
        self.print_results(f"Power On - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def power_off(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        url = f"{self.BASE_URL}{self.STATE_DOMAIN}"
        payload = {"action": "POWER_OFF"}
        response = requests.put(url, json=payload)
        self.print_results(f"Power Off - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def brake_release(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        url = f"{self.BASE_URL}{self.STATE_DOMAIN}"
        payload = {"action": "BRAKE_RELEASE"}
        response = requests.put(url, json=payload)
        self.print_results(f"Brake Release - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def restart_safety(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        # ------ this powers the arm off ------- #
        url = f"{self.BASE_URL}{self.STATE_DOMAIN}"
        payload = {"action": "RESTART_SAFETY"}
        response = requests.put(url, json=payload)
        self.print_results(f"Restart Safety - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def unlock_protective_stop(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        url = f"{self.BASE_URL}{self.STATE_DOMAIN}"
        payload = {"action": "UNLOCK_PROTECTIVE_STOP"}
        response = requests.put(url, json=payload)
        self.print_results(f"Unlock Protective Stop - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def get_safety_mode(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        # should return one of [NORMAL, REDUCED,  PROTECTIVE_STOP, EMERGENCY_STOP, FAULT]
        url = f"{self.BASE_URL}{self.SAFETY_MODE_DOMAIN}"
        response = requests.get(url)
        self.print_results(f"Get Safety Mode - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def get_robot_mode(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        # should return one of [NO_CONTROLLER, DISCONNECTED, CONFIRM_SAFETY, BOOTING, POWER_OFF, POWER_ON, IDLE, BACKDRIVE, RUNNING, UPDATING]
        url = f"{self.BASE_URL}{self.ROBOT_MODE_DOMAIN}"
        response = requests.get(url)
        self.print_results(f"Get Robot Mode - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response

    
    ############################################    
    # program domain actions
    def get_program_state(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        # should return either PLAYING, PAUSED, or STOPPED
        url = f"{self.BASE_URL}{self.PROGRAM_DOMAIN}"
        response = requests.get(url)
        self.print_results(f"Get Program State - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def play_program(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        # starts the program running on the robot
        url = f"{self.BASE_URL}{self.PROGRAM_DOMAIN}"
        payload = {"action": "play"}
        response = requests.put(url, json=payload)
        self.print_results(f"Play Program - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def pause_program(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        # pauses the program running on the robot
        url = f"{self.BASE_URL}{self.PROGRAM_DOMAIN}"
        payload = {"action": "pause"}
        response = requests.put(url, json=payload)
        self.print_results(f"Pause Program - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def resume_program(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        # resumes the paused program on the robot
        url = f"{self.BASE_URL}{self.PROGRAM_DOMAIN}"
        payload = {"action": "resume"}
        response = requests.put(url, json=payload)
        self.print_results(f"Resume Program - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def stop_program(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        # stops the program running on the robot
        url = f"{self.BASE_URL}{self.PROGRAM_DOMAIN}"
        payload = {"action": "stop"}
        response = requests.put(url, json=payload)
        self.print_results(f"Stop Program - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def get_loaded_program(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        # gets the name of the program currently loaded on the robot
        url = f"{self.BASE_URL}{self.PROGRAM_LOADED_DOMAIN}"
        response = requests.get(url)
        self.print_results(f"Get Loaded Program - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def load_program(self, program_name, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        # loads the specified program onto the robot
        url = f"{self.BASE_URL}{self.PROGRAM_LOADED_DOMAIN}"
        payload = {"name": program_name}
        response = requests.put(url, json=payload)
        self.print_results(f"Load Program '{program_name}' - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    
    ############################################    
    # programs domain actions
    def get_loaded_program_names(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        # gets the names of all programs currently loaded on the robot
        url = f"{self.BASE_URL}{self.PROGRAMS_DOMAIN}"
        response = requests.get(url)
        self.print_results(f"Get Loaded Program Names - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def get_specific_urpx(self, program_name, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        # gets the specified urpx program from the robot
        # this gets the data of the urpx, and then needs to be written to a file to be useful
        url = f"{self.BASE_URL}{self.PROGRAMS_DOMAIN}{program_name}"
        response = requests.get(url)
        self.print_results(f"Get Specific URPX '{program_name}' - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response
    
    def upload_specific_urpx(self, urpx_file_name, urpx_file_path=None, function_print_info=None):
        # uploads the specified urpx program to the robot
        if function_print_info is None:
            function_print_info = self.object_print_info
        url = f"{self.BASE_URL}{self.PROGRAMS_DOMAIN}"
        # use filepath if provided, otherwise use current working directory
        if urpx_file_path is None:
            urpx_file_path = os.getcwd()
        full_file_path = os.path.join(urpx_file_path, f"{urpx_file_name}.urpx")
        myFile = open(full_file_path, 'rb')
        print(f"full_file_path: {full_file_path}")
        print(myFile)
        response = requests.post(url,files={'file': myFile})
        self.print_results(f"Upload Specific URPX '{urpx_file_name}' - status code: {response.status_code}, data retrieved: {response.json()}", function_print_info)
        return response


    ############################################    
    # user-defined functions
    def play_or_resume(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        data = self.get_program_state(function_print_info)
        if "PAUSED" in data.text:
            data = self.resume_program(function_print_info)
        elif "STOPPED" in data.text:
            data = self.play_program(function_print_info)
        return data
    
    def get_all_modes(self, function_print_info=None):
        if function_print_info is None:
            function_print_info = self.object_print_info
        modes = {}
        modes['operating_mode'] = self.get_operating_mode(function_print_info).json()['mode']
        modes['control_mode'] = self.get_control_mode(function_print_info).json()['mode']
        modes['safety_mode'] = self.get_safety_mode(function_print_info).json()['mode']
        modes['robot_mode'] = self.get_robot_mode(function_print_info).json()['mode']
        modes['program_state'] = self.get_program_state(function_print_info).json()['state']
        self.print_results(f"Get All Modes - data retrieved: {modes}", function_print_info)
        return modes
    
    def report_mode_changes(self, interval=1, print_state_changes=None):
        # TODO: add a return variable statement to the loop?
        if print_state_changes is None:
            print_state_changes = self.object_print_info
        # continuously monitors the robot modes and prints to console when a change occurs
        last_modes = self.get_all_modes(False)
        # self.print_results(f"Initial Modes: {last_modes}", self.object_print_info)
        while True:
            time.sleep(interval)
            current_modes = self.get_all_modes(False)
            for key in last_modes:
                if current_modes[key] != last_modes[key]:
                    self.print_results(f"Mode Change Detected - {key}: {last_modes[key]} -> {current_modes[key]}", print_state_changes)
            last_modes = current_modes

    # TODO: report all changes, including loaded program and list of programs?

    
    def power_on_full(self, function_print_info=None):
        # first, set print status to default to global object setting
        if function_print_info is None:
            function_print_info = self.object_print_info
          
        # start by checking arm modes
        modes = self.get_all_modes(function_print_info)

        # confirm in remote mode
        if modes['control_mode'] == 'REMOTE':
            ok_to_continue = True
        else:
            self.print_results("please set robot to remote mode and try again", function_print_info)
            ok_to_continue = False
        
        # next, make sure safety state is ok
        if ok_to_continue:
            if modes['safety_mode'] != 'NORMAL':
                self.print_results("address safety state before powering on arm", function_print_info)
                ok_to_continue = False
            
        # then, begin power on decision tree
        if ok_to_continue:
            # if on, dont need to do anything
            if modes['robot_mode'] == 'RUNNING':
                self.print_results("Robot is already powered on", function_print_info)
                ok_to_continue = False
            # cannot power on from these states
            if (modes['robot_mode'] == 'DISCONNECTED' or 
                modes['robot_mode'] == 'NO_CONTROLLER' or
                modes['robot_mode'] == 'BACKDRIVE' or
                modes['robot_mode']=='CONFIRM_SAFETY'):
                self.print_results(f"unable to power arm on, mode is {modes['robot_mode']}", function_print_info)
                ok_to_continue = False
            # if off, power on
            if modes['robot_mode'] == 'POWER_OFF':
                self.print_results("powering on robot...", function_print_info)
                self.power_on(function_print_info)
                time.sleep(0.5)  # brief pause to allow mode to update
                modes = self.get_all_modes(function_print_info)

            # modes where we need to wait for state to change on its own
            if (modes['robot_mode'] == 'BOOTING' or
                modes['robot_mode'] == 'POWER_ON' or
                modes['robot_mode'] == 'UPDATING'):
                keep_waiting = True
                while keep_waiting:
                    time.sleep(0.5)
                    self.print_results(f"waiting for robot to finish {modes['robot_mode']}...", function_print_info)
                    modes = self.get_all_modes(function_print_info)
                    if modes['robot_mode'] == 'IDLE':
                        keep_waiting = False
            
            # finally, unlock brakes
            if modes['robot_mode'] == 'IDLE':
                self.print_results("releasing brakes...", function_print_info)
                self.brake_release(function_print_info)
                time.sleep(0.5)  # brief pause to allow mode to update
                modes = self.get_all_modes(function_print_info)

        # confirm resulting state
        modes = self.get_all_modes(function_print_info)
        if modes['robot_mode'] == 'RUNNING':
            self.print_results("robot is now powered on and ready", function_print_info)
        else:
            print(f"Error: robot failed to power on, current mode is {modes['robot_mode']}")

                    

                
    # TODO: reset after estop test

    ############################################
    # ----- end of function definitions ------ #
    ############################################

    ### end of class robot_api ###

