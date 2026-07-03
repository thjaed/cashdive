import requests
import json

class TrueLayerClient:
    def __init__(self, access_token):
        self.access_token = access_token
    
    def get_accounts(self):
        url = "https://api.truelayer-sandbox.com/data/v1/accounts"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_balance(self, id):
        url = f"https://api.truelayer-sandbox.com/data/v1/accounts/{id}/balance"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_transactions(self, id):
        url = f"https://api.truelayer-sandbox.com/data/v1/accounts/{id}/transactions"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()