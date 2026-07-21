import requests
from models import *

class TrueLayerClient:
    def __init__(self, auth):
        self.auth = auth
    
    def get_accounts(self) -> list[Account]:
        url = "https://api.truelayer-sandbox.com/data/v1/accounts"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.auth.token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()["results"]
        
        accounts = []
        for a in data:
            accounts.append(Account(
                account_id=a["account_id"],
                account_type=a["account_type"],
                display_name=a["display_name"],
                currency=a["currency"],
                update_timestamp=a["update_timestamp"]                
            ))
            
        return accounts

    def get_balance(self, account_id: str) -> Balance:
        url = f"https://api.truelayer-sandbox.com/data/v1/accounts/{account_id}/balance"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.auth.token}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        b = response.json()["results"][0]
        
        timestamp = b.get("update_timestamp")
        if timestamp:
            timestamp = datetime.fromisoformat(timestamp)
        
        balance = Balance(
            currency=b["currency"],
            current=b["current"],
            available=b.get("available"),
            update_timestamp=timestamp
        )
        
        return balance

    def get_transactions(self, account_id: str) -> list[Transaction]:
        url = f"https://api.truelayer-sandbox.com/data/v1/accounts/{account_id}/transactions"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.auth.token}"
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
                transaction_id=t["transaction_id"],
                timestamp=datetime.fromisoformat(t["timestamp"]),
                description=t["description"],
                amount=t["amount"],
                currency=t["currency"],
                transaction_type=t["transaction_type"],
                transaction_category=t["transaction_category"],
                transaction_classification=t["transaction_classification"],
                merchant_name=t.get("merchant_name"),
                running_balance=running_balance,
                pending=False
                
            ))
        return transactions
    
    def get_pending_transactions(self, account_id: str) -> list[Transaction]:
        url = f"https://api.truelayer-sandbox.com/data/v1/accounts/{account_id}/transactions/pending"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.auth.token}"
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
                transaction_id=t["transaction_id"],
                timestamp=datetime.fromisoformat(t["timestamp"]),
                description=t["description"],
                amount=t["amount"],
                currency=t["currency"],
                transaction_type=t["transaction_type"],
                transaction_category=t["transaction_category"],
                transaction_classification=t["transaction_classification"],
                merchant_name=t.get("merchant_name"),
                running_balance=running_balance,
                pending=True
                
            ))
        return transactions
    
    #def get_standing_orders(self, id):
    #    url = f"https://api.truelayer-sandbox.com/data/v1/accounts/{id}/standing_orders"
#
    #    headers = {
    #        "Accept": "application/json",
    #        "Authorization": f"Bearer {self.auth.token}"
    #    }
#
    #    response = requests.get(url, headers=headers)
    #    response.raise_for_status()
    #    return response.json()
#
    #def get_direct_debits(self, id):
    #    url = f"https://api.truelayer-sandbox.com/data/v1/accounts/{id}/direct_debits"
#
    #    headers = {
    #        "Accept": "application/json",
    #        "Authorization": f"Bearer {self.auth.token}"
    #    }
#
    #    response = requests.get(url, headers=headers)
    #    response.raise_for_status()
    #    return response.json()
    #
    #def get_cards(self):
    #    url = f"https://api.truelayer-sandbox.com/data/v1/cards"
#
    #    headers = {
    #        "Accept": "application/json",
    #        "Authorization": f"Bearer {self.auth.token}"
    #    }
#
    #    response = requests.get(url, headers=headers)
    #    response.raise_for_status()
    #    return response.json()
    #
    #def get_card(self, id):
    #    url = f"https://api.truelayer-sandbox.com/data/v1/cards/{id}"
#
    #    headers = {
    #        "Accept": "application/json",
    #        "Authorization": f"Bearer {self.auth.token}"
    #    }
#
    #    response = requests.get(url, headers=headers)
    #    response.raise_for_status()
    #    return response.json()
#
    #def get_card_balance(self, id):
    #    url = f"https://api.truelayer-sandbox.com/data/v1/cards/{id}/balance"
#
    #    headers = {
    #        "Accept": "application/json",
    #        "Authorization": f"Bearer {self.auth.token}"
    #    }
#
    #    response = requests.get(url, headers=headers)
    #    response.raise_for_status()
    #    return response.json()
#
    #def get_card_transactions(self, id):
    #    url = f"https://api.truelayer-sandbox.com/data/v1/cards/{id}/transactions"
#
    #    headers = {
    #        "Accept": "application/json",
    #        "Authorization": f"Bearer {self.auth.token}"
    #    }
#
    #    response = requests.get(url, headers=headers)
    #    response.raise_for_status()
    #    return response.json()
#
    #def get_card_pending_transactions(self, id):
    #    url = f"https://api.truelayer-sandbox.com/data/v1/cards/{id}/transactions/pending"
#
    #    headers = {
    #        "Accept": "application/json",
    #        "Authorization": f"Bearer {self.auth.token}"
    #    }
#
    #    response = requests.get(url, headers=headers)
    #    response.raise_for_status()
    #    return response.json()
#