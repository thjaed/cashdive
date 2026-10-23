"use client";

import { Balance, Transaction, Account } from "@/app/types/models";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

export default function AccountPage() {
  const params = useParams();
  const accountId = params.accountId as string;

  const [balance, setBalance] = useState<Balance | null>(null);
  const [transactions, setTransactions] = useState<Transaction[] | []>([]);
  const [account, setAccount] = useState<Account | null>(null);

  const [pageCount, setPageCount] = useState<number | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [pageInput, setPageInput] = useState(String(1));

  function submitPage() {
    if (isNaN(Number(pageInput))) {
      setPageInput(String(currentPage));
      return;
    }

    let page = Number(pageInput);

    if (page < 1) {
      setPageInput("1");
      page = 1;
    } else if (pageCount && page > pageCount) {
      setPageInput(String(pageCount));
      page = pageCount;
    }

    if (pageCount && page >= 1 && page <= pageCount) {
      setCurrentPage(page);
    }
  }

  async function getBalance() {
    const balanceResponse = await fetch(
      `http://localhost:8000/balance/${accountId}`,
      {
        cache: "no-store",
      },
    );
    const balance = (await balanceResponse.json()) as Balance;
    setBalance(balance);
  }

  async function getTransactions() {
    const TransactionResponse = await fetch(
      `http://localhost:8000/transactions/${accountId}?page=${currentPage}&page_size=${pageSize}`,
      { cache: "no-store" },
    );
    const PagintatedTransactions = await TransactionResponse.json();
    const transactions = PagintatedTransactions.transactions;
    const page_count = PagintatedTransactions.page_count;

    setTransactions(transactions);
    setPageCount(page_count);
  }

  async function getAccount() {
    const accountResponse = await fetch("http://localhost:8000/accounts", {
      cache: "no-store",
    });
    const accounts = (await accountResponse.json()) as Account[];
    const account = accounts.find(
      (account: Account) => account.account_id == accountId,
    );
    if (account != null) {
      setAccount(account);
    }
  }

  useEffect(() => {
    getBalance();
  }, []);

  useEffect(() => {
    getTransactions();
    setPageInput(String(currentPage));
  }, [currentPage, pageSize]);

  useEffect(() => {
    getAccount();
  }, []);

  return (
    <main className="min-h-screen bg-gray-900 px-4 py-12 text-slate-100">
      <div className="mx-auto max-w-3xl">
        <div className="flex flex-col gap-3 pb-3">
          <span className="flex w-fit">
            <span className="material-symbols-outlined">chevron_backward</span>
            <Link
              href="/"
              className="hover:text-gray-400 underline-offset-2 hover:underline pb-3"
            >
              Back to Accounts
            </Link>
          </span>

          <h1 className="text-2xl font-bold">{account?.display_name}</h1>

          <div className="flex gap-3">
            <h1>Account Balance</h1>
            <h1>
              {balance?.available} {balance?.currency}
            </h1>
          </div>
        </div>

        <ul className="divide-y divide-gray-700 overflow-hidden border border-black bg-slate-800 max-w-3xl shadow-sm">
          {transactions.map((transaction: Transaction) => (
            <li key={transaction.transaction_id}>
              <div className="flex items-center gap-4 px-5 py-3">
                <div>{transaction.description}</div>
                <div>{transaction.timestamp}</div>
                <div className="ml-auto flex gap-3">
                  <div className="text-sm font-medium text-gray-300">
                    {transaction.amount}
                  </div>
                  <div className="text-sm font-medium text-gray-300">
                    {transaction.currency}
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
        <div className="flex items-center pt-5 justify-between">
          <div className="flex gap-3 items-center">
            <button
              onClick={() => setCurrentPage(currentPage - 1)}
              disabled={pageCount === null || currentPage <= 1}
              className="flex items-center hover:cursor-pointer hover:bg-gray-700 bg-slate-800 border-gray-700 shadow-sm border-2"
            >
              <span className="material-symbols-outlined">
                chevron_backward
              </span>
            </button>

            <p>Page</p>

            <input
              className="field-sizing-content bg-slate-800 border-gray-700 shadow-sm border-2 text-center px-3 py-1"
              value={pageInput}
              onFocus={() => setPageInput("")}
              onChange={(e) => setPageInput(e.target.value)}
              onBlur={submitPage}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  submitPage();
                }
              }}
            />

            <p>of {pageCount}</p>

            <button
              onClick={() => setCurrentPage(currentPage + 1)}
              disabled={pageCount === null || currentPage >= pageCount}
              className="flex items-center hover:cursor-pointer hover:bg-gray-700 bg-slate-800 border-gray-700 shadow-sm border-2"
            >
              <span className="material-symbols-outlined">chevron_forward</span>
            </button>
          </div>
          <label className="flex items-center gap-3">
            Transactions Per Page
            <select
              name="selectedPageSize"
              className="bg-slate-800 border-gray-700 shadow-sm border-2 px-3 py-2 hover:cursor-pointer"
              onChange={(e) => {
                setCurrentPage(1);
                setPageSize(Number(e.target.value));
              }}
              value={pageSize}
            >
              <option value="20">20</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
          </label>
        </div>
      </div>
    </main>
  );
}
