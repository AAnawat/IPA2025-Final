import requests
from pprint import pprint

def find_webex_room(auth_token, room_name):
    URL = "https://webexapis.com/v1/rooms"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "COntent-Type": "application/json"
    }

    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching rooms: {response.status_code}")
    
    return list(filter(lambda room: room["title"] == room_name, response.json()["items"]))[0]

if __name__ == "__main__":
    pprint(find_webex_room("ACCESS_KEY", "IPA-Final"))