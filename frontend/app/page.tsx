import Link from "next/link";
import { AuthStatus, Account, AccountSummary, Balance } from "./types/models";
import { formatCurrency } from "@/extras/utils";

export default async function Home() {
  // bank connection status
  const response = await fetch("http://localhost:8000/auth/status", {
    cache: "no-store",
  });
  const authStatus = (await response.json()) as AuthStatus;
  const connected = authStatus.connected;

  let accounts: AccountSummary[] = [];
  if (connected) {
    const response = await fetch("http://localhost:8000/account_summary", {
      cache: "no-store",
    });
    accounts = (await response.json()) as AccountSummary[];
  }

  return (
    <main className="min-h-screen bg-gray-900 px-4 py-12 text-slate-100">
      {!connected ? (
        //not connected to bank
        <>
          <h1>Not connected to your bank.</h1>
          <Link href="http://localhost:8000/auth/start">Connect Here</Link>
        </>
      ) : (
        // connected to bank
        <>
          <div className="mx-auto w-full max-w-2xl">
            <h1 className="mb-6 text-2xl font-bold tracking-tight">Your Accounts</h1>

            <ul className="divide-y divide-black overflow-hidden border border-black bg-slate-800">
              {accounts.map((account: AccountSummary) => (
                <li key={account.account_id}>
                  <Link href={`/accounts/${account.account_id}`} className="flex items-center gap-4 px-5 py-4 hover:bg-gray-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-500">
                    <div>
                      <div className="font-semibold text-gray-100">{account.display_name}</div>
                      <div className="mt-1 text-sm text-gray-400">{account.account_type}</div>
                    </div>
                      <div className="ml-auto shrink-0 text-sm font-medium text-gray-300">
                        {account.balance.available ? formatCurrency(account.balance.currency, account.balance.available, "", "-") : ""}
                        </div>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </>
      )}
    </main>
  );
}
