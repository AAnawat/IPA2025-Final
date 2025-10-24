#######################################################################################
# Yourname: Anawat Wongprachanukul
# Your student ID: 66070217
# Your GitHub Repo: https://github.com/AAnawat/IPA2025-Final

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.
import os
import time
import json
import requests
from dotenv import load_dotenv
from requests_toolbelt.multipart.encoder import MultipartEncoder

from webex_utils.findRoom import find_webex_room
from netmiko_final import gigabit_status
from ansible_final import showrun, config_motd
from restconf_final import \
    create as rest_create, \
    delete as rest_delete, \
    enable as rest_enable, \
    disable as rest_disable, \
    status as rest_status
from netconf_final import \
    create as net_create, \
    delete as net_delete, \
    enable as net_enable, \
    disable as net_disable, \
    status as net_status 

#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

load_dotenv()

ACCESS_TOKEN = os.environ.get("AUTH_TOKEN")

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = (
    find_webex_room(ACCESS_TOKEN, "IPA2025")["id"]
)

# Defind variable used to control the use of restconf or netconf
method = None

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)

    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message.startswith("/66070217"):
        # extract the command
        message_parts = message.split()

# 5. Complete the logic for each command
        responseMessage = None;
        text = None;
        
        if (len(message_parts) == 2):
            command = message.split()[-1]
            
            if (command in ["restconf", "netconf"]):
                method = command
                text = f"Ok: {method.capitalize()}"
            elif (command in ["create", "delete", "enable", "disable", "status", "gigabit_status", "showrun"]):
                text = "Error: No IP specified"
            elif (all(part.isdigit() and 0 <= int(part) <= 255 for part in command.split('.'))):
                text = "Error: No command found."
        
        if (method == None):
            text = "Error: method not specified."
        
        if (len(message_parts) == 3):
            os.environ["ROUTER_HOST"] = message_parts[1]
            command = message_parts[2]
            
            if (method != None) and (command in ["create", "delete", "enable", "disable", "status"]):
                if (method == "restconf"):
                    if command == "create":
                        text = rest_create()
                    elif command == "delete":
                        text = rest_delete()
                    elif command == "enable":
                        text = rest_enable()
                    elif command == "disable":
                        text = rest_disable()
                    elif command == "status":
                        text = rest_status()
                elif (method == "netconf"):
                    if command == "create":
                        text = net_create()
                    elif command == "delete":
                        text = net_delete()
                    elif command == "enable":
                        text = net_enable()
                    elif command == "disable":
                        text = net_disable()
                    elif command == "status":
                        text = net_status()
                else:
                    text = "Error: method not supported."
            
            if (command in ["gigabit_status", "showrun", "motd"]):
                if (command == "gigabit_status"):
                    text = gigabit_status()
                elif (command == "showrun"):
                    responseMessage, filename = showrun()
                elif (command == "motd"):
                    text = "test in motd command"
            
        if (len(message_parts) > 3):
            command = message_parts[2]
            os.environ["ROUTER_HOST"] = message_parts[1]
            
            motd_message = ' '.join(message_parts[3:])
            text = config_motd(motd_message)
            
            
# 6. Complete the code to post the message to the Webex Teams room.

        # The Webex Teams POST JSON data for command showrun
        # - "roomId" is ID of the selected room
        # - "text": is always "show running config"
        # - "files": is a tuple of filename, fileobject, and filetype.

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
        # Prepare postData and HTTPHeaders for command showrun
        # Need to attach file if responseMessage is 'ok'; 
        # Read Send a Message with Attachments Local File Attachments
        # https://developer.webex.com/docs/basics for more detail

        if command == "showrun" and responseMessage == 'ok':
            fileobject = open(f"./files/{filename}", "rb")
            filetype = "text/plain"
            postData = {
                "roomId": roomIdToGetMessages,
                "text": "show running config",
                "files": (filename, fileobject, filetype),
            }
            postData = MultipartEncoder(postData)
            HTTPHeaders = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": postData.content_type
            }
        # other commands only send text, or no attached file.
        else:
            postData = {"roomId": roomIdToGetMessages, "text": text}
            postData = json.dumps(postData)

            # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
            HTTPHeaders = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}   

        # Post the call to the Webex Teams message API.
        r = requests.post(
            "https://webexapis.com/v1/messages",
            data=postData,
            headers=HTTPHeaders,
        )
        if not r.status_code == 200:
            print(r.json())
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )
