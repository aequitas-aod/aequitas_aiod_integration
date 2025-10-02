import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PROTECTED_API_URL = os.getenv("PROTECTED_API_URL") 

def add_asset(entity_type, entity_data, token):
    # Dynamic endpoint selection
    if entity_type == "dataset":
        endpoint="v2/datasets"
    elif entity_type == "experiment":
        endpoint="v2/experiments"
    elif entity_type == "educational_resource":
        endpoint="v2/educational_resources"
    else:
        print(f"Entity '{entity_type}' not supported.")
        return
    
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

def edit_asset(entity_type, entity_data, token, identifier):
    
    if not identifier:
        print("Error: Identifier (ID) is required to edit an asset.")
        return
    # Dynamic endpoint selection
    if entity_type == "dataset":
        endpoint="v2/datasets"
    elif entity_type == "experiment":
        endpoint="v2/experiments"
    elif entity_type == "educational_resource":
        endpoint="v2/educational_resources"
    else:
        print(f"Entity '{entity_type}' not supported.")
        return
    
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