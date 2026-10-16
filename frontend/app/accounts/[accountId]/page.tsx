import { Balance, Transaction, Account } from "@/app/types/models";
import Link from "next/link";

type AccountPageProps = {
  params: Promise<{
    accountId: string;
  }>;
};

export default async function AccountPage({ params }: AccountPageProps) {
  const { accountId } = await params;

  const balanceResponse = await fetch(
    `http://localhost:8000/balance/${accountId}`,
    {
      cache: "no-store",
    },
  );
  const balance = (await balanceResponse.json()) as Balance;

  const TransactionResponse = await fetch(
    `http://localhost:8000/transactions/${accountId}`,
    { cache: "no-store" },
  );
  const transactions = (await TransactionResponse.json()) as Transaction[];

  const accountResponse = await fetch("http://localhost:8000/accounts", {
    cache: "no-store",
  });
  const accounts = (await accountResponse.json()) as Account[];
  const account = accounts.find(
    (account: Account) => account.account_id == accountId,
  );

  return (
    <main className="min-h-screen bg-gray-900 px-4 py-12 text-slate-100">
      <div className="mx-auto max-w-3xl">
        <div className="flex flex-col gap-3 pb-3">
          <span className="flex hover:text-gray-400">
            <span className="material-symbols-outlined">chevron_backward</span>
            <Link
              href="/"
              className="underline-offset-2 hover:underline w-fit pb-3"
            >
              Back to Accounts
            </Link>
          </span>

          <h1 className="text-2xl font-bold">{account?.display_name}</h1>

          <div className="flex gap-3">
            <h1>Account Balance</h1>
            <h1>{balance.available} {balance.currency}</h1>
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
      </div>
    </main>
  );
}
