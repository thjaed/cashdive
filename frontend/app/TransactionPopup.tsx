import Popup from "reactjs-popup";
import type { Transaction } from "./types/models";
import {
  formatCurrency,
  formatLongTransactionDate,
  formatTransactionDescription,
  formatTransactionCategory,
} from "./utils";

interface TransactionPopupProps {
  transaction: Transaction;
  open: boolean;
  onClose: () => void;
}

export default function TransactionPopup({
  transaction,
  open,
  onClose,
}: TransactionPopupProps) {
  return (
    <Popup open={open} onClose={onClose} modal>
      <div className="flex flex-col gap-1 shadow-2xl w-80 h-120 text-slate-100 bg-slate-900 border-2 border-slate-700">
        <div className="flex justify-end">
          <button
            className="flex items-center px-2 py-2 hover:cursor-pointer hover:bg-slate-700"
            onClick={onClose}
          >
            <span className="material-symbols-outlined text-slate-300">
              close
            </span>
          </button>
        </div>
        <div className="flex flex-col flex-1 items-center px-6 pb-5 text-slate-100 min-h-0">
          <h2 className="text-4xl font-bold font-mono mb-3">
            {formatCurrency(transaction.currency, transaction.amount, "+", "-")}
          </h2>
          <div className="flex flex-col items-center text-slate-300 mb-5">
            <p>{formatTransactionDescription(transaction.description)}</p>
            <p>{formatLongTransactionDate(transaction.timestamp)}</p>
          </div>
          <ul className="divide-y divide-gray-700 overflow-hidden border border-gray-700 bg-slate-800 w-full mb-5">
            <li className="bg-slate-900 flex justify-between px-3 py-1 items-center">
              <p className="font-bold">Status</p>
              <p className="font-mono uppercase text-sm">
                {transaction.pending ? "Pending" : "Cleared"}
              </p>
            </li>
            <li className="bg-slate-900 flex justify-between px-3 py-1 items-center">
              <p className="font-bold">Type</p>
              <p className="font-mono uppercase text-sm">
                {formatTransactionCategory(transaction.transaction_category)}
              </p>
            </li>
          </ul>
          <div className="w-full flex-1 flex flex-col min-h-0 pb-5">
            <p className="font-bold mb-1">Notes</p>
            <textarea
              className="border border-gray-700 w-full flex-1 p-1 text-sm resize-none focus:outline-none focus:border-slate-500"
              placeholder="Add notes for this transaction here"
            />
          </div>
          <button
            onClick={onClose}
            className="bg-slate-700 px-14 py-2 font-bold hover:cursor-pointer hover:border-slate-500 border border-transparent transition-colors"
          >
            Save
          </button>
        </div>
      </div>
    </Popup>
  );
}
