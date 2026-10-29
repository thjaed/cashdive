"use client";

import Link from "next/link";
import { AuthStatus, AccountSummary } from "./types/models";
import { formatCurrency, deCapitalise } from "@/app/utils";
import { useState, useEffect } from "react";

export default function Home() {
  const [accounts, setAccounts] = useState<AccountSummary[] | null>(null);
  const [connectionState, setConnectionState] = useState<boolean | null>(null);

  async function getConnectionStatus() {
    const response = await fetch("http://localhost:8000/auth/status", {
      cache: "no-store",
    });
    if (response.status == 200) {
      const authStatus = (await response.json()) as AuthStatus;
      setConnectionState(authStatus.connected);
    }
  }

  async function getAccounts() {
    if (connectionState) {
      const response = await fetch("http://localhost:8000/account_summary", {
        cache: "no-store",
      });
      if (response.status == 200) {
        const accountResponse = (await response.json()) as AccountSummary[];
        setAccounts(accountResponse);
      }
    }
  }

  useEffect(() => {
    document.title = "CashDive";
    getConnectionStatus();
  }, []);

  useEffect(() => {
    getAccounts();
  }, [connectionState]);

  return (
    <>
      {connectionState === null ? (
        // Connection state not determined
        <div className="flex justify-center items-center min-h-screen bg-ink-950">
          <div className="flex h-8 w-8 animate-spin rounded-full border-4 border-ink-600 border-t-terminal-400" />
        </div>
      ) : !connectionState ? (
        // Not connected
        <div className="flex flex-col gap-4 justify-center items-center min-h-screen bg-ink-950">
          <h1 className="text-bold text-2xl">
            CashDive is not connected to your bank.
          </h1>
          <Link
            className="group inline-flex items-center text-xl transition-colors text-slate-300 hover:text-terminal-300 underline-offset-2"
            href="http://localhost:8000/auth/start"
          >
            <span className="group-hover:underline underline-offset-4 decoration-terminal-300">
              Connect
            </span>

            <span
              aria-hidden="true"
              className="material-symbols-outlined transition-transform motion-safe:group-hover:-translate-y-0.5 motion-safe:group-hover:translate-x-0.5"
            >
              arrow_outward
            </span>
          </Link>
        </div>
      ) : (
        <main className="min-h-screen bg-ink-950 px-4 py-12 text-slate-100">
          <div className="mx-auto w-full max-w-2xl">
            <h1 className="mb-6 text-3xl font-bold uppercase font-mono text-terminal-300">
              Your Accounts
            </h1>
            {!accounts ? (
              // Skeleton account loader
              <ul className="divide-y divide-ink-600 overflow-hidden border border-ink-600 bg-ink-900">
                {Array.from({ length: 3 }).map((_, index) => (
                  <li key={index}>
                    <div className="flex items-center gap-4 px-5 py-4">
                      <div>
                        <div className="h-5 w-48 animate-pulse rounded bg-ink-700" />
                        <div className="h-3 w-20 mt-3 animate-pulse rounded bg-ink-700" />
                      </div>
                      <div className="ml-auto h-3 w-10 mt-3 animate-pulse rounded bg-ink-700" />
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <ul className="divide-y divide-ink-600 overflow-hidden border border-ink-600 bg-ink-900">
                {accounts.map((account: AccountSummary) => (
                  <li key={account.account_id}>
                    <Link
                      href={`/accounts/${account.account_id}`}
                      className="group flex items-center gap-6 px-5 py-4 border-transparent border-2 transition-colors hover:border-terminal-300 hover:bg-ink-700"
                    >
                      <div>
                        <p className="font-mono uppercase tracking-tight text-lg text-slate-100">
                          {deCapitalise(account.display_name)}
                        </p>
                        <p className="text-sm text-slate-400">
                          {deCapitalise(account.account_type)}
                        </p>
                      </div>
                      <p className="ml-auto shrink-0 font-mono text-xl font-medium text-terminal-300">
                        {account.balance.available
                          ? formatCurrency(
                              account.balance.currency,
                              account.balance.available,
                              "",
                              "-",
                            )
                          : ""}
                      </p>
                      <span className="material-symbols-outlined text-slate-300 transition-colors group-hover:translate-x-0.5 group-hover:text-terminal-300">
                        chevron_forward
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </main>
      )}
    </>
  );
}
