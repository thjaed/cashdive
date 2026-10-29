"use client";

import TransactionPopup from "@/app/TransactionPopup";
import {
  Balance,
  Transaction,
  Account,
  TransactionSummary,
} from "@/app/types/models";
import {
  formatCurrency,
  skeletonWidth,
  deCapitalise,
  formatTransactionDescription,
  formatTransactionDate,
} from "@/app/utils";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

export default function AccountPage() {
  const params = useParams();
  const accountId = params.accountId as string;

  const [balance, setBalance] = useState<Balance | null>(null);
  const [transactions, setTransactions] = useState<TransactionSummary[] | null>(
    null,
  );
  const [selectedTransaction, setSelectedTransaction] =
    useState<TransactionSummary | null>(null);
  const [refreshTransactions, setRefreshTransactions] = useState<number>(0); // refresh trigger state for after closing popup
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

  function triggerTransactionRefresh() {
    if (refreshTransactions === 0) {
      setRefreshTransactions(1);
    } else {
      setRefreshTransactions(0);
    }
  }

  function transactionPopupClosed(noteChanged: boolean) {
    if (noteChanged) {
      triggerTransactionRefresh();
    }
    setSelectedTransaction(null);
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
      try {
        const response = await fetch(
          `http://localhost:8000/transactions/${accountId}/summary?page=${currentPage}&page_size=${pageSize}`,
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
  }, [accountId, currentPage, pageSize, refreshTransactions]);

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

  useEffect(() => {
    if (account?.display_name) {
      document.title = `CashDive - ${deCapitalise(account.display_name)}`;
    } else {
      document.title = "CashDive";
    }
  }, [account]);

  return (
    <main className="min-h-screen bg-ink-950 px-4 py-12 text-slate-100">
      <div className="mx-auto max-w-3xl">
        <div className="flex flex-col pb-3">
          <Link href="/" className="flex w-fit pb-8 text-slate-400 group  ">
            <span className="text-slate-400 material-symbols-outlined group-hover:text-terminal-300">
              chevron_backward
            </span>{" "}
            <p className="group-hover:text-terminal-300 underline-offset-2 group-hover:underline">
              Back to Accounts
            </p>
          </Link>

          {account?.display_name ? (
            <h1 className="text-3xl font-bold pb-8 uppercase font-mono text-terminal-300">
              {deCapitalise(account.display_name)}
            </h1>
          ) : (
            // skeleton title
            <div className="h-9 w-80 mb-4 animate-pulse rounded bg-ink-700" />
          )}

          <div className="flex gap-3">
            {balance?.currency && balance.available ? (
              <div className="w-full border-2 border-ink-600 bg-ink-900 px-6 py-5">
                <h2 className="font-mono text-sm uppercase tracking-wider text-slate-400">
                  Account Balance
                </h2>
                <h3 className="font-mono text-4xl font-bold text-terminal-300">
                  {formatCurrency(balance.currency, balance.available, "", "-")}
                </h3>
              </div>
            ) : (
              // skeleton
              <div className="w-full border-2 border-ink-600 bg-ink-900 px-6 py-5">
                <h2 className="font-mono text-sm uppercase tracking-wider text-slate-400">
                  Account Balance
                </h2>
                <div className="h-10 w-50 animate-pulse rounded bg-ink-700" />
              </div>
            )}
          </div>
        </div>

        <ul className="divide-y divide-ink-600 overflow-hidden border-2 border-ink-600 bg-ink-900 max-w-3xl shadow-sm">
          <li className="hidden sm:block bg-ink-800 text-sm tracking-wider text-slate-400 font-mono uppercase">
            <div className="grid grid-cols-2 sm:grid-cols-[minmax(0,1.3fr)_170px_minmax(0,0.5fr)] px-5 py-1 w-full">
              <p className="order-1 mr-5">Description</p>
              <p className="order-3 sm:order-2">Date</p>
              <div className="order-2 sm:order-3 ml-auto flex gap-3">
                <p className="text-ml">Amount</p>
              </div>
            </div>
          </li>
          {transactions !== null
            ? transactions.map((transaction: TransactionSummary) => (
                <li
                  key={transaction.transaction_id}
                  onClick={() => setSelectedTransaction(transaction)}
                >
                  <div className="grid grid-cols-[minmax(0,1fr)_auto] gap-x-4 gap-y-1 px-5 py-3 sm:grid-cols-[minmax(0,1.3fr)_170px_minmax(0,0.5fr)] sm:gap-0 hover:cursor-pointer border-transparent border-2 transition-colors hover:border-terminal-300 hover:bg-ink-700">
                    <div className="order-1 flex flex-col sm:flex-row min-w-0 sm:items-center justify-between sm:justify-start sm:gap-3">
                      <span className="font-bold truncate flex items-center gap-1">
                        {formatTransactionDescription(transaction.description)}
                        {transaction.has_note && (
                          <span className="material-symbols-outlined text-sm font-normal">
                            sticky_note_2
                          </span>
                        )}
                      </span>
                      {transaction.pending && (
                        <div className="hidden sm:block rounded-sm border border-terminal-300 text-terminal-300 px-2 text-sm">
                          Pending
                        </div>
                      )}

                      <p className="sm:hidden text-slate-300">
                        {formatTransactionDate(transaction.timestamp)}
                      </p>
                    </div>

                    <p className="hidden sm:block text-slate-300 sm:order-2">
                      {formatTransactionDate(transaction.timestamp)}
                    </p>

                    <div className="order-2 ml-auto flex flex-col items-end gap-2 sm:order-3 sm:flex-row">
                      <div
                        className={`rounded-sm w-fit px-1 ${Number(transaction.amount) > 0 ? "bg-positive/30" : ""}`}
                      >
                        <p className="text-ml font-mono font-bold">
                          {formatCurrency(
                            transaction.currency,
                            transaction.amount,
                            "+",
                            "",
                          )}
                        </p>
                      </div>
                      {transaction.pending ? (
                        <div className="sm:hidden rounded-sm border border-terminal-300 text-terminal-300 px-2 text-sm">
                          Pending
                        </div>
                      ) : (
                        ""
                      )}
                    </div>
                  </div>
                </li>
              ))
            : Array.from({ length: pageSize }).map((_, index) => (
                // skeleton loader
                <li key={index}>
                  <div className="grid grid-cols-2 sm:grid-cols-[minmax(0,1fr)_150px_180px] md:grid-cols-[minmax(0,1fr)_170px_200px] px-5 py-3 w-full">
                    <div
                      className="order-1 mb-2 sm:mb-0 mr-5 h-5 sm:h-6 animate-pulse rounded bg-ink-700"
                      style={{ width: `${skeletonWidth(index, 150, 210)}px` }}
                    />
                    <div className="order-3 sm:order-2 h-5 sm:h-6 w-36 animate-pulse rounded bg-ink-700" />
                    <div className="order-2 sm:order-3 ml-auto flex gap-3">
                      <div className="h-6 w-16 animate-pulse rounded bg-ink-700" />
                    </div>
                  </div>
                </li>
              ))}
        </ul>
        {selectedTransaction && (
          <>
            <TransactionPopup
              transaction={selectedTransaction}
              open={true}
              onClose={(x) => transactionPopupClosed(x)}
            />
            <div className="fixed inset-0 z-40 bg-black/60"></div>
          </>
        )}
        <div className="flex items-center pt-5 justify-between">
          <div className="flex gap-3 items-center">
            <button
              onClick={() => incrementPage(-1)}
              className="flex items-center border-2 border-ink-600 bg-ink-800 shadow-sm transition-colors hover:cursor-pointer hover:border-terminal-300 hover:bg-ink-700"
            >
              <span className="material-symbols-outlined">
                chevron_backward
              </span>
            </button>

            <p>Page</p>

            <input
              className="field-sizing-content border-2 border-ink-600 bg-ink-800 px-3 py-1 text-center shadow-sm focus:border-terminal-300 focus:outline-none"
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
              className="flex items-center border-2 border-ink-600 bg-ink-800 shadow-sm transition-colors hover:cursor-pointer hover:border-terminal-300 hover:bg-ink-700"
            >
              <span className="material-symbols-outlined">chevron_forward</span>
            </button>
          </div>
          <label className="flex items-center gap-3">
            Transactions Per Page
            <select
              name="selectedPageSize"
              className="border-2 border-ink-600 bg-ink-800 px-3 py-2 shadow-sm hover:cursor-pointer focus:border-terminal-300 focus:outline-none"
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
