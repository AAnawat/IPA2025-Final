import os

from dotenv import load_dotenv
from netmiko import ConnectHandler
from pprint import pprint

load_dotenv()


# Device connection parameters from environment variables
device_ip = os.environ.get("ROUTER_HOST")
username = os.environ.get("ROUTER_USER")
password = os.environ.get("ROUTER_PASS")

# Define device parameters for Netmiko
device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


# Get gigabit interface status
def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        result = ssh.send_command("show ip interface brief", use_textfsm=True, read_timeout=60)
        
        int_status_list = []
        for status in result:
            if status:
                int_status_list.append(f"{status['interface']} {status['status']}")
                if status["status"] == "up":
                    up += 1
                elif status["status"] == "down":
                    down += 1
                elif status["status"] == "administratively down":
                    admin_down += 1
        ans = f"{', '.join(int_status_list)} -> {up} up, {down} down, {admin_down}, administratively down"

        pprint(ans)
        return ans
