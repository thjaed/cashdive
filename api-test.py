import requests
import os

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

link = get_auth_link()

if link.get("success") == True:
    print(f"Login Here: {link['result']}")

    code = input("Paste Code: ")
    response = exchange_code(code)

    if response.get("access_token"):
        token = response["access_token"]
        print("Login Succeded!")
        print("\n")
        print(get_accounts(token))
    else:
        print("Error gettting token")
        print(response)

else:
    print(f"Error getting auth link: {link}")