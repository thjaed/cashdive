import os
import psycopg2
from models import Transaction, RunningBalance


def get_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", 5432),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

class TransactionDb:
    def __enter__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            transaction_timestamp TIMESTAMPTZ NOT NULL,
            description TEXT NOT NULL,
            amount NUMERIC(12,2) NOT NULL,
            currency TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            transaction_category TEXT NOT NULL,
            transaction_classification TEXT[] NOT NULL,
            running_balance_amount NUMERIC(12,2),
            running_balance_currency TEXT,
            pending BOOLEAN NOT NULL,
            merchant_name TEXT
        );
        """
        
        try:
            self.cursor.execute(query)
            self.conn.commit()
            print("Transaction table created")
        except Exception as e:
            print(f"An error occured creating the table: {e}")
        
    def insert_transactions(self, transactions: list[Transaction]):
        query = """
        INSERT INTO transactions (
            transaction_id,
            transaction_timestamp,
            description,
            amount,
            currency,
            transaction_type,
            transaction_category,
            transaction_classification,
            running_balance_amount,
            running_balance_currency,
            pending,
            merchant_name
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (transaction_id) DO NOTHING;
        """
        
        try:
            inserted = 0
            for t in transactions:
                self.cursor.execute(query, (
                    t.transaction_id,
                    t.timestamp,
                    t.description,
                    t.amount,
                    t.currency,
                    t.transaction_type,
                    t.transaction_category,
                    t.transaction_classification,
                    t.running_balance.amount,
                    t.running_balance.currency,
                    t.pending,
                    t.merchant_name
                ))
                inserted += self.cursor.rowcount
            self.conn.commit()
            print(f"{inserted} transactions inserted")
            
        except Exception as e:
            print(f"An error occured inserting transactions: {e}")
        
    def get_transactions(self) -> list[Transaction]:
        query = """
        SELECT * FROM transactions;
        """

        try:
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            
            transactions: list[Transaction] = []
            
            for record in records:
                transactions.append(Transaction(
                    transaction_id=record[0],
                    timestamp=record[1],
                    description=record[2],
                    amount=record[3],
                    currency=record[4],
                    transaction_type=record[5],
                    transaction_category=record[6],
                    transaction_classification=record[7],
                    running_balance=RunningBalance(record[8], record[9]),
                    pending=record[10],
                    merchant_name=record[11]
                ))
                
            print("Transactions fetched")
            return transactions
                
        except Exception as e:
            print(f"An error occured getting transactions: {e}")
            return []
