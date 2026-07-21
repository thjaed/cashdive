from database import TransactionDb
from api import TrueLayerClient
from models import Transaction


class TransactionRepository:
    def __init__(self, client: TrueLayerClient):
        self.client = client
    
    def get_transactions(self, account_id: str) -> list[Transaction]:
        transactions = self.client.get_transactions(account_id)
        with TransactionDb() as db:
            db.insert_transactions(transactions)
        return transactions
        
        
def test():
    from prettytable import PrettyTable
    
    with TransactionDb() as db:
        transactions = db.get_transactions()

    table = PrettyTable(["Amount", "Currency", "Description", "Date", "Running Balance"])

    for t in transactions:
            table.add_row([
                t.amount,
                t.currency,
                t.description,
                t.timestamp.strftime("%A %d %B %Y"),
                t.running_balance.amount]
            )

    print(table)
