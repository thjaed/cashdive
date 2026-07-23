import os
import psycopg2
from models import Balance, RunningBalance, Transaction, Account


def get_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", 5432),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

class BalanceDb:
    def __enter__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self.create_table()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS balances (
            account_id TEXT PRIMARY KEY,
            currency TEXT NOT NULL,
            current NUMERIC(12,2) NOT NULL,
            available NUMERIC(12,2),
            update_timestamp TIMESTAMPTZ
        );
        """
        
        try:
            self.cursor.execute(query)
            self.conn.commit()
            
        except Exception:
            self.conn.rollback()
            raise
        
    def insert_balance(self, balance: Balance):
        query = """
        INSERT INTO balances (
            account_id,
            currency,
            current,
            available,
            update_timestamp
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (account_id) DO UPDATE SET
            currency = EXCLUDED.currency,
            current = EXCLUDED.current,
            available = EXCLUDED.available,
            update_timestamp = EXCLUDED.update_timestamp;
        """
        
        try:
            self.cursor.execute(query, (
                balance.account_id,
                balance.currency,
                balance.current,
                balance.available,
                balance.update_timestamp
                ))
            self.conn.commit()
            
        except Exception:
            self.conn.rollback()
            raise
        
    def get_balance(self, account_id: str) -> Balance:
        query = """
        SELECT * FROM balances WHERE account_id = %s;
        """

        try:
            self.cursor.execute(query, (account_id,))
            record = self.cursor.fetchone()
            
            if record is None:
                raise Exception("No balance found for account")

            balance = Balance(
                account_id=record[0],
                currency=record[1],
                current=record[2],
                available=record[3],
                update_timestamp=record[4]
            )
                
            print("Balance fetched")
            return balance
                
        except Exception:
            self.conn.rollback()
            raise
        
class AccountDb:
    def __enter__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self.create_table()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS accounts (
            account_id TEXT PRIMARY KEY,
            account_type TEXT NOT NULL,
            display_name TEXT NOT NULL,
            currency TEXT NOT NULL,
            update_timestamp TIMESTAMPTZ NOT NULL
        );
        """
        
        try:
            self.cursor.execute(query)
            self.conn.commit()
            
        except Exception:
            self.conn.rollback()
            raise
        
    def insert_accounts(self, accounts: list[Account]):
        query = """
        INSERT INTO accounts (
            account_id,
            account_type,
            display_name,
            currency,
            update_timestamp
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (account_id) DO UPDATE SET
            account_type = EXCLUDED.account_type,
            display_name = EXCLUDED.display_name,
            currency = EXCLUDED.currency,
            update_timestamp = EXCLUDED.update_timestamp;
        """
        
        try:
            for a in accounts:
                self.cursor.execute(query, (
                    a.account_id,
                    a.account_type,
                    a.display_name,
                    a.currency,
                    a.update_timestamp
                ))
            self.conn.commit()
            
        except Exception:
            self.conn.rollback()
            raise
        
    def get_accounts(self) -> list[Account]:
        query = """
        SELECT * FROM accounts;
        """

        try:
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            
            accounts: list[Account] = []
            
            for record in records:
                accounts.append(Account(
                    account_id=record[0],
                    account_type=record[1],
                    display_name=record[2],
                    currency=record[3],
                    update_timestamp=record[4]
                ))
                
            print("Accounts fetched")
            return accounts
                
        except Exception:
            self.conn.rollback()
            raise

class TransactionDb:
    def __enter__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self.create_table()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        
    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            account_id TEXT NOT NULL,
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
            
        except Exception:
            self.conn.rollback()
            raise
        
    def insert_transactions(self, transactions: list[Transaction]):
        query = """
        INSERT INTO transactions (
            transaction_id,
            account_id,
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
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (transaction_id) DO UPDATE SET
            account_id = EXCLUDED.account_id,
            transaction_timestamp = EXCLUDED.transaction_timestamp,
            description = EXCLUDED.description,
            amount = EXCLUDED.amount,
            currency = EXCLUDED.currency,
            transaction_type = EXCLUDED.transaction_type,
            transaction_category = EXCLUDED.transaction_category,
            transaction_classification = EXCLUDED.transaction_classification,
            running_balance_amount = EXCLUDED.running_balance_amount,
            running_balance_currency = EXCLUDED.running_balance_currency,
            pending = EXCLUDED.pending,
            merchant_name = EXCLUDED.merchant_name;
        """
        
        try:
            for t in transactions:
                self.cursor.execute(query, (
                    t.transaction_id,
                    t.account_id,
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
            self.conn.commit()
            
        except Exception:
            self.conn.rollback()
            raise
        
    def get_transactions(self, account_id: str) -> list[Transaction]:
        query = """
        SELECT * FROM transactions
        WHERE account_id = %s
        ORDER BY transaction_timestamp DESC;
        """

        try:
            self.cursor.execute(query, (account_id,))
            records = self.cursor.fetchall()
            
            transactions: list[Transaction] = []
            
            for record in records:
                transactions.append(Transaction(
                    transaction_id=record[0],
                    account_id=record[1],
                    timestamp=record[2],
                    description=record[3],
                    amount=record[4],
                    currency=record[5],
                    transaction_type=record[6],
                    transaction_category=record[7],
                    transaction_classification=record[8],
                    running_balance=RunningBalance(record[9], record[10]),
                    pending=record[11],
                    merchant_name=record[12]
                ))
                
            print("Transactions fetched")
            return transactions
                
        except Exception:
            self.conn.rollback()
            raise
    
    def delete_pending_transactions(self, account_id: str) -> None:
        query = """
        DELETE FROM transactions
        WHERE account_id = %s
            AND pending = TRUE;
        """
        
        try:
            self.cursor.execute(query, (account_id,))
            self.conn.commit()
            
        except Exception:
            self.conn.rollback()
            raise
