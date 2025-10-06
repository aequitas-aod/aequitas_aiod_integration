
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
    PROTECTED_API_URL=http://your-protected-api/
    TESTING=1 # 0 disable testing, 1 enable testing
    ```

    Replace the values with your Keycloak server URL, realm name, client ID, and the URL of the protected API you want to access.


    
2.  **Run the script:**
   
   To add a new asset:

    ```bash
    python  aiod_cli.py --entity <fill with entity> add --data '"$(cat <entity>_metadata.json)"'
    ```

    To edit an asset:
    
      ```bash
    python  aiod_cli.py --entity <fill with entity> edit --id <fill with the id> --data '"$(cat <entity>_metadata.json)"'
    ```

        the entity field might be:  
        - dataset
        - educational_resource
        - experiment
    
        the id parameter must be an existing asset ID

  
        the metadata.json must be filled acording to the type of entity (see the examples)

3.  **Authorize the device:**

    The script will output a verification URL and a user code.

    ```
    Please go to the following URL and enter the code:
    <verification-uri>
    User Code: <user-code>
    ```

    Open the `verification_uri` in a browser on another device (like a smartphone or computer) and enter the `user_code` to authorize the device.

4. **Run the tests**
    Update the `.env` file and set 
    ```bash
    TESTING=1
    ```
    After that, execute:

    ```bash
    pytest tests
    ```


## Environment Variables Definition

-   `KEYCLOAK_SERVER_URL`: The URL of your Keycloak server (e.g., `http://localhost:8080`).
-   `KEYCLOAK_REALM`: The name of the Keycloak realm you are using.
-   `KEYCLOAK_CLIENT_ID`: The ID of the client configured in Keycloak for this application.
-   `PROTECTED_API_URL`: The URL of the protected API endpoint that the script will call with the access token.
-   `TESTING`: The variable that uses the mock for testing (1) or not (0).

## Dependencies

The project's dependencies are listed in the `requirements.txt` file:

-   `python-dotenv`: For managing environment variables.
-   `python-keycloak`: A Python client for Keycloak.
-   `PyJWT`: For decoding JSON Web Tokens (JWTs).
-   `requests`: For making HTTP requests.
-   `pytest`: For testing.
-   `requests-mock`: For making HTTP requests in testing.
-   `pytest-dotenv`: For managing environment variables in testing.


