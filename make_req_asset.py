import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PROTECTED_API_URL = os.getenv("PROTECTED_API_URL") 

def add_asset(entity_data, token):
    endpoint="v2/experiments"  #or v2/experiments or v2/datasets or v2/educational_resources
    url = f"{PROTECTED_API_URL}/{endpoint}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=entity_data, headers=headers)
    if response.ok:
        print("Asset created successfully", response.text)
    else:
        print("Error creating asset:", response.text)

def edit_asset(entity_data, token):
    identifier="<id>"
    endpoint="v2/experiments"  #or v2/experiments or v2/datasets or v2/educational_resources
    url = f"{PROTECTED_API_URL}/{endpoint}/{identifier}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    response = requests.put(url, json=entity_data, headers=headers)
    if response.ok:
        print("Asset edited successfully.")
    else:
        print("Error when editing asset:", response.text)