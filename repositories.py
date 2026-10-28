from datetime import datetime, timezone, timedelta
from database import AccountDb, TransactionDb, BalanceDb, CacheExpiryDb, TransactionNoteDb
from api import TrueLayerClient
from models import Transaction, Account, Balance, TransactionNote, TransactionSummary

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
    
    def get_transactions(self, account_id: str, skip: int, limit: int) -> list[Transaction]:
        cache_key = f"transactions:{account_id}"
        
        with CacheExpiryDb() as db:
            expired = db.has_expired(cache_key)
        
        if not expired:
            with TransactionDb() as db:
                return db.get_transactions(account_id, skip, limit)
        
        complete_transactions = self.client.get_transactions(account_id)
        pending_transactions = self.client.get_pending_transactions(account_id)
        
        all_transactions = pending_transactions + complete_transactions
        
        with TransactionDb() as db:
            db.delete_pending_transactions(account_id)
            db.insert_transactions(all_transactions)
            transactions = db.get_transactions(account_id, skip, limit)
        
        with CacheExpiryDb() as db:
            db.update(cache_key, '3 minutes')
        
        return transactions

    def get_summary(self, account_id: str, skip: int, limit: int) -> list[TransactionSummary]:
            cache_key = f"transactions:{account_id}"
            
            with CacheExpiryDb() as db:
                expired = db.has_expired(cache_key)
            
            if not expired:
                with TransactionDb() as db:
                    return db.get_summary(account_id, skip, limit)
            
            complete_transactions = self.client.get_transactions(account_id)
            pending_transactions = self.client.get_pending_transactions(account_id)
            
            all_transactions = pending_transactions + complete_transactions
            
            with TransactionDb() as db:
                db.delete_pending_transactions(account_id)
                db.insert_transactions(all_transactions)
                transactions = db.get_summary(account_id, skip, limit)
            
            with CacheExpiryDb() as db:
                db.update(cache_key, '3 minutes')
            
            return transactions
        
    def get_transaction_count(self, account_id: str) -> int:
        with TransactionDb() as db:
            return db.get_transaction_count(account_id)
    
    def transaction_exists(self, transaction_id: str) -> bool:
        with TransactionDb() as db:
            return db.transaction_exists(transaction_id)

class TransactionNoteRepository:
    def get_note(self, transaction_id: str) -> TransactionNote | None:
        with TransactionNoteDb() as db:
            return db.get_note(transaction_id)
    
    def set_note(self, transaction_id: str, note: str) -> None:
        with TransactionNoteDb() as db:
            return db.insert_note(TransactionNote(transaction_id, note))
    
    def delete_note(self, transaction_id: str) -> None:
        with TransactionNoteDb() as db:
            return db.delete_note(transaction_id)
        