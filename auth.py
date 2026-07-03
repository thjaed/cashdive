import os
import requests
import json

class TrueLayerAuth:
    def __init__(self):
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        
        if self.client_id == None and self.client_secret == None:
            raise Exception("CLIENT_ID and CLIENT_SECRET environment variables not set")
        elif self.client_id == None:
            raise Exception("CLIENT_ID environment variable not set")
        elif self.client_secret == None:
            raise Exception("CLIENT_SECRET environment variable not set")
        
        self.redirect_uri = "https://console.truelayer.com/redirect-page"
        self.access_token = None
        self.refresh_token = None

    def get_auth_link(self):
        # get a link to authenticate with bank provider
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
            "scope": "info accounts balance transactions offline_access",
            "state": "abcddd",
            "consent_id": "edfgfgh",
            "provider_id": "mock"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["result"]


    def exchange_code(self, code):
        # exchange code from auth link for access & refresh tokens
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
        self.refresh_token = data["refresh_token"]
        self.save_token()

        return self.access_token

    def refresh_access_token(self):
        # get a new access token from the refresh token
        url = 'https://auth.truelayer-sandbox.com/connect/token'

        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token
        }

        response = requests.post(url, data=data)
        response.raise_for_status()

        data = response.json()
        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]
        self.save_token()

        return self.access_token


    def save_token(self):
        token_data = {
                      "access_token": self.access_token,
                      "refresh_token": self.refresh_token
                      }
        with open("token.json", "w") as f:
            json.dump(token_data, f)

    def load_token(self):
        try:
            with open("token.json", "r") as f:
                data = json.load(f)
                self.access_token = data["access_token"]
                self.refresh_token = data["refresh_token"]
                return data
                
        except FileNotFoundError:
            return None

    def token_is_valid(self, token):
        try:
            url = "https://api.truelayer-sandbox.com/data/v1/accounts"

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
        # load tokens from file
        if not self.load_token():
            # if the token file doesn't exist
            return False
        
        if not self.token_is_valid(self.access_token):
            # refresh using refresh token if access token doesn't work
            self.refresh_access_token()

        if self.token_is_valid(self.access_token):
            return self.access_token
        else:
            return False