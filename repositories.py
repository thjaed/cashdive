from database import AccountDb, TransactionDb, BalanceDb
from api import TrueLayerClient
from models import Transaction, Account, Balance

class BalanceRepository:
    def __init__(self, client: TrueLayerClient):
        self.client = client
    
    def get_balance(self, account_id: str) -> Balance:
        balance = self.client.get_balance(account_id)
        with BalanceDb() as db:
            db.insert_balance(balance)
        return balance
    
class AccountRepository:
    def __init__(self, client: TrueLayerClient):
        self.client = client
    
    def get_accounts(self) -> list[Account]:
        accounts = self.client.get_accounts()
        with AccountDb() as db:
            db.insert_accounts(accounts)
        return accounts
    
class TransactionRepository:
    def __init__(self, client: TrueLayerClient):
        self.client = client
    
    def get_transactions(self, account_id: str) -> list[Transaction]:
        transactions = self.client.get_transactions(account_id)
        with TransactionDb() as db:
            db.insert_transactions(transactions)
        return transactions
