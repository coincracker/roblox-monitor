"""
Roblox Presence Monitor

Author: Louis
Github: https://github.com/coincracker

Creds to: omega (@comprehensions on discord), did half of it. 
"""

import requests
import time
import json

# -- Gets webhook from JSON file
def get_webhook() -> str:
    try:
        with open("reqs/config.json", "r") as file:
            webhook = json.load(file)["webhook"]
            return webhook

    except FileNotFoundError:
        print("Error getting webhook...")

    return None

# -- Sends a message to discord webhook
def send_to_webhook(webhook: str , message: str) -> bool:
    try:
        response = requests.post(webhook, json={
            "content": message,
        })

        return response.status_code == 200

    except requests.RequestException:
        print("Error executing webhook request...")

# -- Gets the status of all users specified
def get_user_status(user_ids: list) -> dict:
    all_users = {}

    try:
        response = requests.post("https://presence.roblox.com/v1/presence/users", json={
            "userIds": user_ids
        })
        user_presences = response.json()["userPresences"]
        
        for item in user_presences:
            all_users[item["userId"]] = item["userPresenceType"]
    
    except requests.RequestException:
        print("Error executing presence request...")

    except KeyError:
        print("Error getting user presences...")

    return all_users

if __name__ == "__main__":
    webhook = get_webhook()

    if not webhook:
        exit(1)

    users = input("Enter all user IDs [1, 2, 3]: ").split(", ")
    users_status = {user : "offline" for user in users}

    while True:
        all_status = get_user_status(users)

        for user, presence_number in all_status.items():
            presence = "online" if presence_number == 2 else "offline"

            if presence == "online":
                if users_status[str(user)] == "offline":
                    print(f"Logged that {user} is in game.") if send_to_webhook(webhook, f"@everyone https://www.roblox.com/users/{user}/profile is in-game!") else print(f"Failed to log that {user} is in game...")
                    
                    users_status[str(user)] = "online"

                else:
                    continue

            else:
                if users_status[str(user)] == "online":
                    print(f"Logged that {user} went offline.") if send_to_webhook(webhook, f"https://www.roblox.com/users/{user}/profile went offline...") else print(f"Failed to log that {user} went offline...")
                    
                    users_status[str(user)] = "offline"
        
        time.sleep(1)
