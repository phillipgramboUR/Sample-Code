# requires 'requests' package, do so with:
# pip install requests
# https://www.universal-robots.com/articles/ur/release-notes/release-note-software-version-1011x/

import requests
import time

ROBOT_IP_ADDR = "192.168.0.13" # Replace with your robot's IP address

# Define static aspects of the API
BASE_URL = f"http://{ROBOT_IP_ADDR}/universal-robots/robot-api"
STATE_DOMAIN = "/robotstate/v1/state"
PROGRAM_DOMAIN = "/program/v1/state"
PROGRAM_DOMAIN_LOAD = "/program/v1/load"

# ----- define functions for actions ----- #
def get_program_state():
    url = f"{BASE_URL}{PROGRAM_DOMAIN}"
    response = requests.get(url)
    print(f"Get Program - status code: {response.status_code}, data retrieved: {response.json()}")
    return response

def power_on():
    url = f"{BASE_URL}{STATE_DOMAIN}"
    payload = {"action": "POWER_ON"}
    response = requests.put(url, json=payload)
    print(f"Power On - status code: {response.status_code}, data retrieved: {response.json()}")
    return response

def power_off():
    url = f"{BASE_URL}{STATE_DOMAIN}"
    payload = {"action": "POWER_OFF"}
    response = requests.put(url, json=payload)
    print(f"Power Off - status code: {response.status_code}, data retrieved: {response.json()}")
    return response

def brake_release():
    url = f"{BASE_URL}{STATE_DOMAIN}"
    payload = {"action": "BRAKE_RELEASE"}
    response = requests.put(url, json=payload)
    print(f"Brake Release - status code: {response.status_code}, data retrieved: {response.json()}")
    return response

def play_program():
    url = f"{BASE_URL}{PROGRAM_DOMAIN}"
    payload = {"action": "play"}
    response = requests.put(url, json=payload)
    print(f"Play Program - status code: {response.status_code}, data retrieved: {response.json()}")
    return response

def pause_program():
    url = f"{BASE_URL}{PROGRAM_DOMAIN}"
    payload = {"action": "pause"}
    response = requests.put(url, json=payload)
    print(f"Pause Program - status code: {response.status_code}, data retrieved: {response.json()}")
    return response

def resume_program():
    url = f"{BASE_URL}{PROGRAM_DOMAIN}"
    payload = {"action": "resume"}
    response = requests.put(url, json=payload)
    print(f"Resume Program - status code: {response.status_code}, data retrieved: {response.json()}")
    return response

def stop_program():
    url = f"{BASE_URL}{PROGRAM_DOMAIN}"
    payload = {"action": "stop"}
    response = requests.put(url, json=payload)
    print(f"Stop Program - status code: {response.status_code}, data retrieved: {response.json()}")
    return response

def restart_safety():
    # ------ this powers the arm off ------- #
    url = f"{BASE_URL}{STATE_DOMAIN}"
    payload = {"action": "RESTART_SAFETY"}
    response = requests.put(url, json=payload)
    print(f"Restart Safety - status code: {response.status_code}, data retrieved: {response.json()}")
    return response

def unlock_protective_stop():
    url = f"{BASE_URL}{STATE_DOMAIN}"
    payload = {"action": "UNLOCK_PROTECTIVE_STOP"}
    response = requests.put(url, json=payload)
    print(f"Unlock Protective Stop - status code: {response.status_code}, data retrieved: {response.json()}")
    return response
    
def play_or_resume():
    data = get_program_state()
    if "PAUSED" in data.text:
        data = resume_program()
    elif "STOPPED" in data.text:
        data = play_program()
    return data
    
# ----- end of function definitions ----- #

# - example usage of the above functions - #   

abc = input("press enter to play program: ")
data = play_or_resume()
time.sleep(1)
abc = input("press enter to pause program: ")
data = pause_program()
time.sleep(1)
abc = input("press enter to play program: ")
data = play_or_resume()
time.sleep(1)

# functionality not yet available: get safety status, get loaded program name, get arm power state


