import pytest
import json
from unittest.mock import patch
from auth import get_access_token

def test_get_access_token_mock(monkeypatch):
    with patch('auth.keycloak_openid.device') as mock_device, \
         patch('auth.requests.post') as mock_post:

        mock_device.return_value = {
            "device_code": "xxx",
            "user_code": "user-code",
            "verification_uri": "http://example.com",
            "interval": 0.01,
            "verification_uri_complete": "http://example.com/complete"
        }

        # Simula "authorization_pending" una vez y luego éxito
        mock_post.side_effect = [
            type("obj", (object,), {"status_code": 400, "json": lambda: {"error": "authorization_pending"}})(),
            type("obj", (object,), {"status_code": 200, "json": lambda: {"access_token": "token"}})()
        ]

        token = get_access_token()
        assert token["access_token"] == "token"
