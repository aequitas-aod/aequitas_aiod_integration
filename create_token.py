import os
import time
import json
import jwt
import requests
from dotenv import load_dotenv, set_key
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



def call_protected_api(access_token):
    """Make a request to a protected API endpoint using the access token."""
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(PROTECTED_API_URL, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to access protected API. Status code: {response.status_code}"}
    
 

def refresh_access_token(refresh_token: str) -> Optional[Dict[str, Any]]:
    token_data = {
        "grant_type": "refresh_token",
        "client_id": KEYCLOAK_CLIENT_ID,
        "refresh_token": refresh_token,
    }
    try:
        response = requests.post(TOKEN_ENDPOINT, data=token_data, timeout=30)
    except requests.RequestException as exc:
        print(f"Failed to refresh token: {exc}")
        return None

    if response.status_code == 200:
        return response.json()

    print("Failed to refresh token:", response.json())
    return None

# Initialize KeycloakOpenID client
keycloak_openid = KeycloakOpenID(
    server_url=f"{KEYCLOAK_SERVER_URL}/",
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM
)

well_known = keycloak_openid.well_known()
#print("Well-known configuration:")
#print(well_known)

TOKEN_ENDPOINT = well_known['token_endpoint']
JWKS_ENDPOINT = well_known['jwks_uri']

response = keycloak_openid.device()
device_code = response['device_code']
user_code = response['user_code']
verification_uri = response['verification_uri']
verification_uri_complete = response['verification_uri_complete']
interval = response['interval']

print(f"Please go to the following URL and enter the code:\n{verification_uri}")
print(f"User Code: {user_code}")
print(f"Or visit directly:\n{verification_uri_complete}")



if __name__ == "__main__":
 while True:

    time.sleep(interval)
    token_data = {
    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    "client_id": KEYCLOAK_CLIENT_ID,
    "device_code": device_code,
    }

    token_response = requests.post(TOKEN_ENDPOINT, data=token_data)
    token_response_data = token_response.json()

    if token_response.status_code == 200:
        access_token = token_response_data['access_token']
        id_token = token_response_data.get('id_token')
        refresh_token = token_response_data.get('refresh_token')
        #print(f"Access Token: {access_token}")
        #print(f"ID Token: {id_token}")
        #print()
        #print(f"Refresh Token: {refresh_token}")
        #print()
        # Save initial tokens in .env
        set_key(".env","REF_TOKEN",refresh_token)
        set_key(".env","ACCESS_TOKEN",access_token)
        print("Tokens saved in .env")
        print()
 
        decoded_token = jwt.decode(access_token, options={"verify_signature": False})
        aud = decoded_token['aud']

        # Fetch JWKS and select the correct signing key
        jwks = requests.get(JWKS_ENDPOINT).json()
        header = jwt.get_unverified_header(access_token)
        signing_key = None
        for key in jwks['keys']:
            if (
                key.get('kid') == header.get('kid')
                and key.get('use') == 'sig'
                and key.get('alg') == 'RS256'
            ):
                signing_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
                break
        if not signing_key:
            raise Exception("No suitable signing key found in JWKS")

        decoded_token = jwt.decode(access_token, signing_key, algorithms=["RS256"], audience=aud)   
       # print(f"Decoded original Access Token:", decoded_token)
        #print()
 
    
        api_response = call_protected_api(access_token)
        print("Protected API response:", api_response)
        # Start refresh loop every 5 minutes
        try:
            print("Starting refresh loop every 5 minutes (Ctrl+C to exit)...")
            while True:
                time.sleep(300)
                refreshed = refresh_access_token(refresh_token)
                #print("Refreshed token response:", refreshed)
                if not refreshed:
                    print("Failed to refresh, retrying in 60s...")
                    time.sleep(60)
                    continue
                access_token = refreshed.get('access_token')
                refresh_token = refreshed.get('refresh_token', refresh_token)
                if access_token:
                    set_key(".env","ACCESS_TOKEN",access_token)
                    set_key(".env","REF_TOKEN",refresh_token)
                    print("ACCESS_TOKEN actualizado en .env")
                else:
                    print("Refresh response without valid access_token")
        except KeyboardInterrupt:
            print("\n Loop stopped by user")
        break

   

    elif token_response.status_code == 400:
        error = token_response_data.get("error")
        if error == "authorization_pending":
            print("Waiting for user authorization...")
            continue
        elif error == "slow_down":
            interval += 5
        else:
            print(f"Error: {error}")
            break
    else:
        print("Unexpected error occurred.")
        break


