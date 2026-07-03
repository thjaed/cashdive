import os
import requests
import json

class TrueLayerAuth:
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.redirect_uri = "https://console.truelayer.com/redirect-page"
        self.access_token = None

    def get_auth_link(self):
        url = "https://auth.truelayer-sandbox.com/v1/authuri"

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        payload = {
            "response_type": "code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "scope": "info accounts balance transactions",
            "state": "abcddd",
            "consent_id": "edfgfgh",
            "provider_id": "mock"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["result"]


    def exchange_code(self, code):
        url = 'https://auth.truelayer-sandbox.com/connect/token'

        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": code
        }

        response = requests.post(url, data=data)
        response.raise_for_status()

        data = response.json()
        self.access_token = data["access_token"]
        self.save_token()

        return self.access_token

    def save_token(self):
        token_data = {"access_token": self.access_token}
        with open("token.json", "w") as f:
            json.dump(token_data, f)

    def load_token(self):
        try:
            with open("token.json", "r") as f:
                data = json.load(f)
                return data["access_token"]
        except FileNotFoundError:
            return None

    def token_is_valid(self, token):
        try:
            url = "https://api.truelayer-sandbox.com/data/v1/me"

            headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {token}"
            }

            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False
    
    def login(self):
        self.access_token = self.load_token()
        if self.token_is_valid(self.access_token):
            return self.access_token
        else:
            return False