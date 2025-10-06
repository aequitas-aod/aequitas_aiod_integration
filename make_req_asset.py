import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PROTECTED_API_URL = os.getenv("PROTECTED_API_URL", "http://localhost:8080") 

def add_asset(entity_type, entity_data, token):
    # Dynamic endpoint selection
    endpoints = {
        "dataset": "v2/datasets",
        "experiment": "v2/experiments",
        "educational_resource": "v2/educational_resources"
    }
    endpoint = endpoints.get(entity_type)
    if not endpoint:
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
        # responseAsJSON = response.json()
        # identifier = responseAsJSON['identifier']
        # print("Requesting the asset just created with identifier: ", identifier)
        # retrieveUrl = f"{PROTECTED_API_URL}/{endpoint}/{identifier}"
        # res = requests.get(retrieveUrl,headers=headers)
        # if res.ok:
        #     print("res", res.text)
        # else:
        #     print("Error retrieving asset:", res.text)
    else:
        print("Error creating asset:", response.text)

def edit_asset(entity_type, entity_data, token, identifier):    
    if not identifier:
        print("Error: Identifier (ID) is required to edit an asset.")
        return
    # Dynamic endpoint selection
    endpoints = {
        "dataset": "v2/datasets",
        "experiment": "v2/experiments",
        "educational_resource": "v2/educational_resources"
    }
    endpoint = endpoints.get(entity_type)
    if not endpoint:
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