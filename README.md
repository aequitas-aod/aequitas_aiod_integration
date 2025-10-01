
# Keycloak Device Authorization Grant Flow Example

This project demonstrates the OAuth 2.0 Device Authorization Grant Flow using Python and Keycloak. 

The script initiates the device authorization flow, polls the token endpoint until the user authorizes the device, and then uses the obtained access token to call a protected API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6+
- pip (Python package installer)
- A running Keycloak instance
- A protected API endpoint to test the access token


### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage



1.  **Configure the environment variables:**

    Create a `.env` file in the root of the project and add the following variables:

    ```
    KEYCLOAK_SERVER_URL=http://localhost:8080
    KEYCLOAK_REALM=your-realm
    KEYCLOAK_CLIENT_ID=your-client-id
    PROTECTED_API_URL=http://your-protected-api/endpoint
    REF_TOKEN=<It will be automatically generated>
    ACCESS=TOKEN=<It will be automatically generated>
    ```

    Replace the values with your Keycloak server URL, realm name, client ID, and the URL of the protected API you want to access.


    
2.  **Run the script:**
    ```bash
    python create_token.py
    ```

3.  **Authorize the device:**

    The script will output a verification URL and a user code.

    ```
    Please go to the following URL and enter the code:
    <verification-uri>
    User Code: <user-code>
    ```

    Open the `verification_uri` in a browser on another device (like a smartphone or computer) and enter the `user_code` to authorize the device.

4.  **Token retrieval and API call:**

    Once authorized, the script will obtain an access token from Keycloak, decode it, and use it to make a request to the `PROTECTED_API_URL`. The response from the protected API will be printed to the console.

5. **Token Creation and refreshing**
    Once created, the initial token only will be automatically refreshed if the process is not termined

6. **Make the request to load a new asset or edit an existing**
    Run the desired script and uncomment the type of asset at the endpoint variable


## Environment Variables Definition

-   `KEYCLOAK_SERVER_URL`: The URL of your Keycloak server (e.g., `http://localhost:8080`).
-   `KEYCLOAK_REALM`: The name of the Keycloak realm you are using.
-   `KEYCLOAK_CLIENT_ID`: The ID of the client configured in Keycloak for this application.
-   `PROTECTED_API_URL`: The URL of the protected API endpoint that the script will call with the access token.
-   `ACCESS_TOKEN`:It need to be created first
-   `REF_TOKEN`:It need to be created first

## Dependencies

The project's dependencies are listed in the `requirements.txt` file:

-   `python-dotenv`: For managing environment variables.
-   `python-keycloak`: A Python client for Keycloak.
-   `PyJWT`: For decoding JSON Web Tokens (JWTs).
-   `requests`: For making HTTP requests.
