"use client";

import { Balance, Transaction, Account } from "@/app/types/models";
import { formatCurrency, skeletonWidth } from "@/extras/utils";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

export default function AccountPage() {
  const params = useParams();
  const accountId = params.accountId as string;

  const [balance, setBalance] = useState<Balance | null>(null);
  const [transactions, setTransactions] = useState<Transaction[] | null>(null);
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

  function incrementPage(increment: number) {
    if (
      pageCount &&
      currentPage + increment <= pageCount &&
      currentPage + increment >= 1
    ) {
      setCurrentPage(currentPage + increment);
    }
  }

  useEffect(() => {
    const controller = new AbortController();

    async function getBalance() {
      setBalance(null);

      try {
        const response = await fetch(
          `http://localhost:8000/balance/${accountId}`,
          {
            cache: "no-store",
            signal: controller.signal,
          },
        );

        const data = await response.json();

        setBalance(data);
      } catch (error) {
        if (error instanceof DOMException && error.name === "AbortError") {
          return;
        }

        console.error(error);
      }
    }
    getBalance();

    return () => {
      controller.abort();
    };
  }, []);

  useEffect(() => {
    const controller = new AbortController();

    async function getTransactions() {
      setTransactions(null);

      try {
        const response = await fetch(
          `http://localhost:8000/transactions/${accountId}?page=${currentPage}&page_size=${pageSize}`,
          {
            cache: "no-store",
            signal: controller.signal,
          },
        );

        const data = await response.json();

        setTransactions(data.transactions);
        setPageCount(data.page_count);
      } catch (error) {
        if (error instanceof DOMException && error.name === "AbortError") {
          return;
        }

        console.error(error);
      }
    }

    getTransactions();

    setPageInput(String(currentPage));

    return () => {
      controller.abort();
    };
  }, [accountId, currentPage, pageSize]);

  useEffect(() => {
    const controller = new AbortController();

    async function getAccount() {
      setAccount(null);

      try {
        const response = await fetch("http://localhost:8000/accounts", {
          cache: "no-store",
          signal: controller.signal,
        });

        const data = await response.json();

        const account = data.find(
          (account: Account) => account.account_id == accountId,
        );
        if (account != null) {
          setAccount(account);
        }

      } catch (error) {
        if (error instanceof DOMException && error.name === "AbortError") {
          return;
        }

        console.error(error);
      }
    }

    getAccount();

    return () => {
      controller.abort();
    };
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

          <h1 className="text-2xl font-bold">
            {account?.display_name ? (
              account.display_name
            ) : (
              <div className="h-8 w-70 animate-pulse rounded bg-gray-700" />
            )}
          </h1>

          <div className="flex gap-3">
            {balance?.currency && balance.available ? (
              <p>
                Account Balance:{" "}
                {formatCurrency(balance.currency, balance.available, "", "-")}
              </p>
            ) : (
              <span className="inline-flex gap-2 items-center">
                <p>Account Balance: </p>
                <div className="ml-auto h-4 w-14 animate-pulse rounded bg-gray-700" />
              </span>
            )}
          </div>
        </div>

        <ul className="divide-y divide-gray-700 overflow-hidden border border-black bg-slate-800 max-w-3xl shadow-sm">
          {transactions !== null
            ? transactions.map((transaction: Transaction) => (
                <li key={transaction.transaction_id}>
                  <div className="flex items-center gap-4 px-5 py-3">
                    <div>{transaction.description}</div>
                    <div>{transaction.timestamp}</div>
                    <div className="ml-auto flex gap-3">
                      <div className="text-sm font-medium text-gray-300">
                        {formatCurrency(
                          transaction.currency,
                          transaction.amount,
                          "+",
                          "",
                        )}
                      </div>
                    </div>
                  </div>
                </li>
              ))
            : Array.from({ length: pageSize }).map((_, index) => (
                <li key={index}>
                  <div className="flex items-center gap-10 px-5 py-3">
                    <div
                      className="h-6 animate-pulse rounded bg-gray-700"
                      style={{ width: `${skeletonWidth(index, 150, 210)}px` }}
                    />
                    <div className="h-6 w-26 animate-pulse rounded bg-gray-700" />
                    <div className="ml-auto flex gap-3">
                      <div className="ml-auto h-3 w-10 animate-pulse rounded bg-gray-700" />
                    </div>
                  </div>
                </li>
              ))}
        </ul>
        <div className="flex items-center pt-5 justify-between">
          <div className="flex gap-3 items-center">
            <button
              onClick={() => incrementPage(-1)}
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
              onClick={() => incrementPage(1)}
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
