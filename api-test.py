from prettytable import PrettyTable
import pyfiglet
from datetime import datetime
from api import TrueLayerClient
from auth import TrueLayerAuth

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
    table = PrettyTable(["Name", "Type", "Currency", "ID"])

    accounts = client.get_accounts()

    for a in accounts:
        table.add_row([
            a.display_name,
            a.account_type,
            a.currency,
            a.account_id
        ])

    print(table)

def print_balance(id):
    print(f"Balance for {id}")
    table = PrettyTable(["Currency", "Available", "Current"])

    b = client.get_balance(id)

    table.add_row([
        b.currency,
        b.available,
        b.current
    ])

    print(table)

def print_transactions(id):
    print(f"Transactions for {id}")
    table = PrettyTable(["Amount", "Currency", "Description", "Date", "Running Balance"])

    transactions = client.get_transactions(id)

    for t in transactions:
        table.add_row([
            t.amount,
            t.currency,
            t.description,
            t.timestamp.strftime("%A %d %B %Y"),
            t.running_balance.amount]
        )

    print(table)

auth = TrueLayerAuth()

if not auth.login():
    print(auth.get_auth_link())

    code = input("Code: ")
    auth.exchange_code(code)

client = TrueLayerClient(auth.access_token)

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