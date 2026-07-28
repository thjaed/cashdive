from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from api import TrueLayerClient
from auth import TrueLayerAuth
from repositories import AccountRepository, TransactionRepository, BalanceRepository
from models import Account, Balance, Transaction, AuthStatus, AuthCallback
from requests.exceptions import HTTPError

app = FastAPI()

@app.get(
    "/accounts",
    response_model=list[Account]
)
def get_accounts() -> list[Account]:
    auth = TrueLayerAuth()
    client = TrueLayerClient(auth)
    accounts_repo = AccountRepository(client)
    
    try:
        accounts = accounts_repo.get_accounts()
        return accounts
    except HTTPError as error:
            if error.response is not None:
                match error.response.status_code:
                    
                    case 404:
                        raise HTTPException(404, detail="Accounts not found")
                    
                raise HTTPException(error.response.status_code)
            
            raise HTTPException(502)

@app.get(
    "/balance/{account_id}",
    response_model=Balance
)
def get_balance(account_id: str) -> Balance:
    if len(account_id) > 128:
        raise HTTPException(400, detail="ID exceeds maximum length")
    
    auth = TrueLayerAuth()
    client = TrueLayerClient(auth)
    balance_repo = BalanceRepository(client)
    
    try:
        balance = balance_repo.get_balance(account_id)
        return balance
    
    except HTTPError as error:
        if error.response is not None:
            match error.response.status_code:
                
                case 404:
                    raise HTTPException(404, detail="Account not found")
                
            raise HTTPException(error.response.status_code)
        
        raise HTTPException(502)
        
    

@app.get(
    "/transactions/{account_id}",
    response_model=list[Transaction]
)
def get_transactions(account_id: str) -> list[Transaction]:
    if len(account_id) > 128:
        raise HTTPException(400, detail="ID exceeds maximum length")

    auth = TrueLayerAuth()
    client = TrueLayerClient(auth)
    transaction_repo = TransactionRepository(client)
    
    try:
        transactions = transaction_repo.get_transactions(account_id)
        return transactions
    
    except HTTPError as error:
        if error.response is not None:
            match error.response.status_code:
                
                case 404:
                    raise HTTPException(404, detail="Account not found")
                
            raise HTTPException(error.response.status_code)
        
        raise HTTPException(502)
                

@app.get(
    "/auth/status",
    response_model=AuthStatus
)
def auth_status() -> AuthStatus:
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
def start_auth() -> RedirectResponse:
    # Redirect to TrueLayer bank login
    auth = TrueLayerAuth()
    auth_url = auth.get_auth_link()
    
    return RedirectResponse(auth_url)
    
@app.get(
    "/auth/callback",
    response_model=AuthCallback
)
def auth_callback(code: str, scope: str | None = None) -> AuthCallback:
    # Exchange code given by TrueLayer
    auth = TrueLayerAuth()
    
    if not code:
        print("no code")
    
    try:
        auth.exchange_code(code)
    except HTTPError as error:
        if error.response is not None:
            match error.response.status_code:
                
                case 400:
                    raise HTTPException(400, detail="Invalid code")
                
            raise HTTPException(error.response.status_code)
        
        raise HTTPException(502)
    
    return AuthCallback(success=True)
