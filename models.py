from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from decimal import Decimal

class Currency(Enum):
    EUR = "EUR"
    GBP = "GBP"
    USD = "USD"
    AUD = "AUD"

class TransactionType(Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

class TransactionCategory(Enum):
    ATM = "ATM"
    BILL_PAYMENT = "BILL_PAYMENT"
    CASH = "CASH"
    CASHBACK = "CASHBACK"
    CHEQUE = "CHEQUE"
    CORRECTION = "CORRECTION"
    CREDIT = "CREDIT"
    DIRECT_DEBIT = "DIRECT_DEBIT"
    DIVIDEND = "DIVIDEND"
    FEE_CHARGE = "FEE_CHARGE"
    INTEREST = "INTEREST"
    OTHER = "OTHER"
    PURCHASE = "PURCHASE"
    STANDING_ORDER = "STANDING_ORDER"
    TRANSFER = "TRANSFER"
    DEBIT = "DEBIT"
    UNKNOWN = "UNKNOWN"

@dataclass
class RunningBalance:
    amount: Decimal | None = None
    currency: Currency | None = None

@dataclass
class Transaction:
    transaction_id: str
    account_id: str
    timestamp: datetime
    description: str
    amount: Decimal
    currency: Currency
    transaction_type: TransactionType
    transaction_category: TransactionCategory
    transaction_classification: list[str]
    running_balance: RunningBalance
    pending: bool
    merchant_name: str | None = None

class AccountType(Enum):
    TRANSACTION = "TRANSACTION"
    SAVINGS = "SAVINGS"
    BUISNESS_TRANSACTION = "BUSINESS_TRANSACTION"
    BUISNESS_SAVINGS = "BUSINESS_SAVINGS"
    
@dataclass
class Account:
    account_id: str
    account_type: AccountType
    display_name: str
    currency: Currency
    update_timestamp: datetime

@dataclass
class Balance:
    currency: Currency
    current: Decimal
    available: Decimal | None = None
    update_timestamp: datetime | None = None