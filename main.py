from fastapi import FastAPI
from api import TrueLayerClient
from auth import TrueLayerAuth
from repositories import AccountRepository, TransactionRepository, BalanceRepository

app = FastAPI()

@app.get("/accounts")
def get_accounts():
    accounts_repo = AccountRepository(client)
    accounts = accounts_repo.get_accounts()
    
    return accounts

@app.get("/balance/{account_id}")
def get_balance(account_id: str):
    balance_repo = BalanceRepository(client)
    balance = balance_repo.get_balance(account_id)

    return balance

@app.get("/transactions/{account_id}")
def get_transactions(account_id: str):
    transaction_repo = TransactionRepository(client)
    transactions = transaction_repo.get_transactions(account_id)
    
    return transactions

@app.get("/login")
def login():
    global client, auth

    auth = TrueLayerAuth()
    if not auth.login():
        return {
            "success": True,
            "user_login_required": True,
            "auth_link": auth.get_auth_link()
        }

    client = TrueLayerClient(auth)
    
    return {
        "success": True,
        "user_login_required": False
    }

@app.get("/code")
def claim_code(code: str):
    auth.exchange_code(code)
    return {
        "success": True
    }