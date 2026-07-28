from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api import TrueLayerClient
from auth import TrueLayerAuth
from repositories import AccountRepository, TransactionRepository, BalanceRepository
from models import Account, Balance, Transaction, AuthStatus, AuthCallback

app = FastAPI()

@app.get(
    "/accounts",
    response_model=list[Account]
)
def get_accounts():
    auth = TrueLayerAuth()
    client = TrueLayerClient(auth)
        
    accounts_repo = AccountRepository(client)
    accounts = accounts_repo.get_accounts()
    
    return accounts

@app.get(
    "/balance/{account_id}",
    response_model=Balance
)
def get_balance(account_id: str):
    auth = TrueLayerAuth()
    client = TrueLayerClient(auth)
        
    balance_repo = BalanceRepository(client)
    balance = balance_repo.get_balance(account_id)

    return balance

@app.get(
    "/transactions/{account_id}",
    response_model=list[Transaction]
)
def get_transactions(account_id: str):
    auth = TrueLayerAuth()
    client = TrueLayerClient(auth)
    
    transaction_repo = TransactionRepository(client)
    transactions = transaction_repo.get_transactions(account_id)
    
    return transactions

@app.get(
    "/auth/status",
    response_model=AuthStatus
)
def auth_status():
    auth = TrueLayerAuth()
    
    if auth.load_token() is None:
        return AuthStatus(connected=False)
    
    try:
        auth.token
        return AuthStatus(connected=True)
    except:
        return AuthStatus(connected=False)
    
@app.get(
    "/auth/start"
)
def start_auth():
    # Redirect to TrueLayer bank login
    auth = TrueLayerAuth()
    auth_url = auth.get_auth_link()
    
    return RedirectResponse(auth_url)
    
@app.get(
    "/auth/callback",
    response_model=AuthCallback
)
def auth_callback(code: str, scope: str):
    # Exchange code given by TrueLayer
    auth = TrueLayerAuth()
    auth.exchange_code(code)
    
    return AuthCallback(success=True)
