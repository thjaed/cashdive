export enum Currency {
    EUR = "EUR",
    GBP = "GBP",
    USD = "USD",
    AUD = "AUD"
}

export enum TransactionType {
    DEBIT = "DEBIT",
    CREDIT = "CREDIT"
}

export enum TransactionCategory {
    ATM = "ATM",
    BILL_PAYMENT = "BILL_PAYMENT",
    CASH = "CASH",
    CASHBACK = "CASHBACK",
    CHEQUE = "CHEQUE",
    CORRECTION = "CORRECTION",
    CREDIT = "CREDIT",
    DIRECT_DEBIT = "DIRECT_DEBIT",
    DIVIDEND = "DIVIDEND",
    FEE_CHARGE = "FEE_CHARGE",
    INTEREST = "INTEREST",
    OTHER = "OTHER",
    PURCHASE = "PURCHASE",
    STANDING_ORDER = "STANDING_ORDER",
    TRANSFER = "TRANSFER",
    DEBIT = "DEBIT",
    UNKNOWN = "UNKNOWN"
}

export enum AccountType {
    TRANSACTION = "TRANSACTION",
    SAVINGS = "SAVINGS",
    BUSINESS_TRANSACTION = "BUSINESS_TRANSACTION",
    BUSINESS_SAVINGS = "BUSINESS_TRANSACTION"
}

export interface RunningBalance {
    amount: string | null,
    currency: Currency | null
}

export interface Transaction {
    transaction_id: string,
    account_id: string,
    timestamp: string,
    description: string,
    amount: string,
    currency: Currency,
    transaction_type: TransactionType,
    transaction_category: TransactionCategory,
    transaction_classification: string[],
    running_balance: RunningBalance,
    pending: boolean,
    merchant_name: string | null
}

export interface Account {
  account_id: string;
  account_type: AccountType;
  display_name: string;
  currency: Currency;
  update_timestamp: string;
}

export interface Balance {
  account_id: string;
  currency: Currency;
  current: string;
  available: string | null;
  update_timestamp: string | null;
}

export interface AuthStatus {
  connected: boolean;
}

export interface AuthCallback {
  success: boolean;
}