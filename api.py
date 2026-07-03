import requests
from models import *

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

    def get_transactions(self, account_id: str) -> list[Transaction]:
        url = f"https://api.truelayer-sandbox.com/data/v1/accounts/{account_id}/transactions"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()["results"]
        
        transactions = []
        for t in data:
            rb = t.get("running_balance")
            if rb and rb.get("amount") and rb.get("currency"):
                running_balance = RunningBalance(
                        amount=rb["amount"],
                        currency=rb["currency"]
                    )
            else:
                running_balance = RunningBalance()
            
            transactions.append(Transaction(
                transaction_id = t["transaction_id"],
                timestamp = datetime.fromisoformat(t["timestamp"]),
                description=t["description"],
                amount=t["amount"],
                currency=t["currency"],
                transaction_type=t["transaction_type"],
                transaction_category=t["transaction_category"],
                transaction_classification=t["transaction_classification"],
                merchant_name=t.get("merchant_name"),
                running_balance=running_balance
                
            ))
        return transactions
    
    def get_pending_transactions(self, id):
        url = f"https://api.truelayer-sandbox.com/data/v1/accounts/{id}/transactions/pending"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_standing_orders(self, id):
        url = f"https://api.truelayer-sandbox.com/data/v1/accounts/{id}/standing_orders"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_direct_debits(self, id):
        url = f"https://api.truelayer-sandbox.com/data/v1/accounts/{id}/direct_debits"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_cards(self):
        url = f"https://api.truelayer-sandbox.com/data/v1/cards"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_card(self, id):
        url = f"https://api.truelayer-sandbox.com/data/v1/cards/{id}"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_card_balance(self, id):
        url = f"https://api.truelayer-sandbox.com/data/v1/cards/{id}/balance"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_card_transactions(self, id):
        url = f"https://api.truelayer-sandbox.com/data/v1/cards/{id}/transactions"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_card_pending_transactions(self, id):
        url = f"https://api.truelayer-sandbox.com/data/v1/cards/{id}/transactions/pending"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
