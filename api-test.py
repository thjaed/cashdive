import requests
import os
from prettytable import PrettyTable
import pyfiglet
import json
from datetime import datetime

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "https://console.truelayer.com/redirect-page"

def get_auth_link():
    url = "https://auth.truelayer-sandbox.com/v1/authuri"

    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    payload = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "https://console.truelayer.com/redirect-page",
        "scope": "info accounts balance transactions",
        "state": "abcddd",
        "consent_id": "edfgfgh",
        "provider_id": "mock"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def exchange_code(code):
    url = 'https://auth.truelayer-sandbox.com/connect/token'

    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "https://console.truelayer.com/redirect-page",
        "code": code
    }

    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()

def get_accounts(token):
    url = "https://api.truelayer-sandbox.com/data/v1/accounts"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_balance(token, id):
    url = f"https://api.truelayer-sandbox.com/data/v1/accounts/{id}/balance"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_transactions(token, id):
    url = f"https://api.truelayer-sandbox.com/data/v1/accounts/{id}/transactions"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def save_token(token_data):
    with open("token.json", "w") as f:
        json.dump(token_data, f)

def load_token():
    try:
        with open("token.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def token_is_valid(token):
    try:
        get_accounts(token)
        return True
    except:
        return False

def login():
    link = get_auth_link()

    if link.get("success") == True:
        print(f"Login Here: {link['result']}")

        code = input("Paste Code: ")
        response = exchange_code(code)

        if response.get("access_token"):
            token = response["access_token"]
            print("Login Succeded!")
            print("\n")
            return token
        else:
            print("Error gettting token")
            print(response)

    else:
        print(f"Error getting auth link: {link}")

text = "CASHDIVE"
ascii_art = pyfiglet.figlet_format(text, font="slant")
print(ascii_art)

def print_options():
    print("1: Accounts")
    print("2: Balance")
    print("3: Transactions")
    #print("4: Pending Transactions")
    #print("5: Standing Orders")
    #print("6: Direct Debits")

def print_accounts():
    print("Accounts")
    table = PrettyTable(["Name", "Type", "Currency", "Number", "Sort Code", "ID"])

    accounts = get_accounts(token)

    for a in accounts["results"]:
        table.add_row([a["display_name"],
                                a["account_type"],
                                a["currency"],
                                a["account_number"]["number"],
                                a["account_number"]["sort_code"],
                                a["account_id"]]
                                )

    print(table)

def print_balance(id):
    print(f"Balance for {id}")
    table = PrettyTable(["Currency", "Available", "Current", "Overdraft"])

    b = get_balance(token, id)["results"][0]

    table.add_row([b["currency"],
                   b["available"],
                   b["current"],
                   b["overdraft"]]
                )

    print(table)

def print_transactions(id):
    print(f"Transactions for {id}")
    table = PrettyTable(["Amount", "Currency", "Description", "Date", "Running Balance"])

    transactions = get_transactions(token, id)["results"]

    for t in transactions:

        timestamp = t["timestamp"]
        dt = datetime.fromisoformat(timestamp)
        formatted = dt.strftime("%A %d %B %Y %H:%M")

        table.add_row([t["amount"],
                       t["currency"],
                       t["description"],
                       formatted,
                       t["running_balance"]["amount"]]
                    )

    print(table)


token_data = load_token()
token = None

if token_data:
    print("Testing stored token")
    token = token_data["access_token"]

    if not token_is_valid(token):
        print("Token expired, logging in again")
        token = None

if not token:
    token = login()
    save_token({"access_token": token})

print_accounts()

while True:
    print_options()
    option = input("Option: ")
    match option:
        case "1":
            print_accounts()
        case "2":
            print_balance(input("Account ID: "))
        case "3":
            print_transactions(input("Account ID: "))
