import Link from "next/link";
import { AuthStatus, Account } from "./types/models";

export default async function Home() {
  // bank connection status
  const response = await fetch("http://localhost:8000/auth/status", {
    cache: "no-store",
  });
  const authStatus = (await response.json()) as AuthStatus;
  const connected = authStatus.connected;

  let accounts: Account[] = [];
  if (connected) {
    const response = await fetch("http://localhost:8000/accounts", {
      cache: "no-store",
    });
    accounts = (await response.json()) as Account[];
  }

  return (
    <main>
      <h1>CashDive</h1>

      {connected ? (
        <h1>Your Accounts</h1>
      ) : (
        <>
          <h1>Not connected to your bank.</h1>
          <Link href="http://localhost:8000/auth/start">Connect Here</Link>
        </>
      )}

      {connected && (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Currency</th>
            </tr>
          </thead>

          <tbody>
            {accounts.map((account: Account) => (
              <tr key={account.account_id}>
                <td>{account.display_name}</td>
                <td>{account.account_type}</td>
                <td>{account.currency}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}
