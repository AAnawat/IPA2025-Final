# -------------------------------------------------------------
# Import required libraries
# -------------------------------------------------------------

import os
import json
import requests
from dotenv import load_dotenv
requests.packages.urllib3.disable_warnings()

load_dotenv()

HOST = os.environ.get("ROUTER_HOST")

# Router IP Address is 10.0.15.181-184
api_url = f"https://{HOST}/restconf/data/ietf-interfaces:interfaces"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = {
    "Accept": "application/yang-data+json", 
    "Content-type":"application/yang-data+json"
}
basicauth = ("admin", "cisco")


# -------------------------------------------------------------
# Core functions
# -------------------------------------------------------------

# Create Loopback66070217 interface
def create():
    yangConfig = {
        "ietf-interfaces:interface": {
        "name": "Loopback66070217",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "172.2.17.1",
                    "netmask": "255.255.255.0"
                }
            ]
        }
    }
    }

    resp = requests.put(
        f"{api_url}/interface=Loopback66070217", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
    )
    
    # Handle case where interface already exists
    if (resp.status_code == 204):
        return "Cannot create: Interface loopback 66070217"

    # Check response status code
    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070217 is created successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot create: Interface loopback 66070217"

# Delete Loopback66070217 interface
def delete():
    resp = requests.delete(
        f"{api_url}/interface=Loopback66070217", 
        auth=basicauth, 
        headers={ "Accept": "application/yang-data+json" }, 
        verify=False
    )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070217 is deleted successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot delete: Interface loopback 66070217"

# Enable Loopback66070217 interface
def enable():
    # Check if interface Loopback66070217 exists
    checkExist = check_interface_exist()
    if not (checkExist):
        return "Cannot enable: Interface loopback 66070217"


    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070217",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
        }
    }

    resp = requests.put(
        f"{api_url}/interface=Loopback66070217", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
    )
    
    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070217 is enabled successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot enable: Interface loopback 66070217"

# Disable Loopback66070217 interface
def disable():
    # Check if interface Loopback66070217 exists
    checkExist = check_interface_exist()
    if not (checkExist):
        return "Cannot shutdown: Interface loopback 66070217"
    
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback66070217",
            "type": "iana-if-type:softwareLoopback",
            "enabled": False,
        }
    }

    resp = requests.put(
        f"{api_url}/interface=Loopback66070217", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
    )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070217 is shutdowned successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot shutdown: Interface loopback 66070217"

# Get status of Loopback66070217 interface
def status():
    api_url_status = f"https://{HOST}/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback66070217"

    resp = requests.get(
        api_url_status, 
        auth=basicauth, 
        headers=headers, 
        verify=False
    )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status = response_json["ietf-interfaces:interface"]["oper-status"]
        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback 66070217 is enabled"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback 66070217 is disabled"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "No Interface loopback 66070217"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


# -------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------

# Check if Loopback66070217 interface exists
# Returns True if exists, False otherwise
def check_interface_exist():
    queryInterface = requests.get(
        f"{api_url}/interface=Loopback66070217", 
        auth=basicauth,
        headers=headers,
        verify=False
    )
    
    return not (queryInterface.status_code == 404)