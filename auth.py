import os
import time
import json
import requests
from dotenv import load_dotenv
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError
from typing import Any, Dict, Optional

# Load environment variables
load_dotenv()

# Environment variables
KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
PROTECTED_API_URL = os.getenv("PROTECTED_API_URL") 

ACCESS_TOKEN: Optional[str] = None
TOKEN_CACHE_FILE = ".token_cache.json"


# Initialize KeycloakOpenID client
keycloak_openid = KeycloakOpenID(
    server_url=f"{KEYCLOAK_SERVER_URL}/",
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM
)

well_known = keycloak_openid.well_known()

TOKEN_ENDPOINT = well_known['token_endpoint']
JWKS_ENDPOINT = well_known['jwks_uri']

DEVICE_AUTH_ENDPOINT = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/device/auth"
TOKEN_ENDPOINT = f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"

def get_device_code():
    response = keycloak_openid.device()
    return response

def get_access_token():
    # First, try to load a valid token
    if os.path.exists(TOKEN_CACHE_FILE):
        with open(TOKEN_CACHE_FILE, "r") as f:
            token_data = json.load(f)
        expires_at = token_data.get("expires_at", 0)
        if time.time() < expires_at:
            return token_data

    device_info = get_device_code()
    print(f"Please go to the following URL and enter the code:\n{device_info['verification_uri']}")
    print(f"User Code: {device_info['user_code']}")
    print(f"Or visit directly:\n{device_info['verification_uri_complete']}")

    token_payload = {
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "device_code": device_info["device_code"],
        "client_id": KEYCLOAK_CLIENT_ID
    }

    interval = device_info.get("interval", 5)

    while True:
        time.sleep(interval)
        response = requests.post(TOKEN_ENDPOINT, data=token_payload)
        if response.status_code == 200:
            token_response = response.json()
            token_response["expires_at"] = time.time() + token_response.get("expires_in", 3600)
            with open(TOKEN_CACHE_FILE, "w") as f:
                json.dump(token_response, f)
            return token_response
        else:
            err = response.json()
            error = err.get("error")
            if error == "authorization_pending":
                print("Waiting for user authorization...")
                continue
            elif error in ("expired_token", "access_denied"):
                print("Authorization expired or denied.")
                return None
            else:
                print(f"Error inesperado: {error}")
                return None 

def refresh_token(refresh_token: str) -> Optional[Dict[str, Any]]:
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": KEYCLOAK_CLIENT_ID
    }
    try:
        response = requests.post(TOKEN_ENDPOINT, data=payload)
        response.raise_for_status()
        token_response = response.json()
        token_response["expires_at"] = time.time() + token_response.get("expires_in", 3600)
        with open(TOKEN_CACHE_FILE, "w") as f:
            json.dump(token_response, f)
        return token_response
    except requests.exceptions.RequestException as e:
        print("Error refreshing token:", e)
        return None

