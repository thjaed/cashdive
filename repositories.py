from datetime import datetime, timezone, timedelta
from database import AccountDb, TransactionDb, BalanceDb, CacheExpiryDb
from api import TrueLayerClient
from models import Transaction, Account, Balance

class BalanceRepository:
    def __init__(self, client: TrueLayerClient):
        self.client = client
    
    def get_balance(self, account_id: str) -> Balance:
        cache_key = f"balance:{account_id}"
        
        with CacheExpiryDb() as db:
            expired = db.has_expired(cache_key)
        
        if not expired:
            with BalanceDb() as db:
                return db.get_balance(account_id)
        
        balance = self.client.get_balance(account_id)
        
        with BalanceDb() as db:
            db.insert_balance(balance)
        
        with CacheExpiryDb() as db:
            db.update(cache_key, '3 minutes')
        
        return balance
    
class AccountRepository:
    def __init__(self, client: TrueLayerClient):
        self.client = client
    
    def get_accounts(self) -> list[Account]:
        cache_key = "accounts"
        
        with CacheExpiryDb() as db:
            expired = db.has_expired(cache_key)
        
        if not expired:
            with AccountDb() as db:
                return db.get_accounts()
            
        accounts = self.client.get_accounts()
        
        with AccountDb() as db:
            db.update(accounts)
        
        with CacheExpiryDb() as db:
            db.update(cache_key, '3 minutes')
            
        return accounts
    
class TransactionRepository:
    def __init__(self, client: TrueLayerClient):
        self.client = client
    
    def get_transactions(self, account_id: str) -> list[Transaction]:
        cache_key = f"transactions:{account_id}"
        
        with CacheExpiryDb() as db:
            expired = db.has_expired(cache_key)
        
        if not expired:
            with TransactionDb() as db:
                return db.get_transactions(account_id)
        
        complete_transactions = self.client.get_transactions(account_id)
        pending_transactions = self.client.get_pending_transactions(account_id)
        
        all_transactions = pending_transactions + complete_transactions
        
        with TransactionDb() as db:
            db.delete_pending_transactions(account_id)
            db.insert_transactions(all_transactions)
            transactions = db.get_transactions(account_id)
        
        with CacheExpiryDb() as db:
            db.update(cache_key, '3 minutes')
        
        return transactions
        