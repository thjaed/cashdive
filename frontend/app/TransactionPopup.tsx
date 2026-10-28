"use client";

import Popup from "reactjs-popup";
import type { Transaction, TransactionSummary } from "./types/models";
import {
  formatCurrency,
  formatLongTransactionDate,
  formatTransactionDescription,
  formatTransactionCategory,
} from "./utils";
import { useEffect, useState } from "react";

interface TransactionPopupProps {
  transaction: TransactionSummary;
  open: boolean;
  onClose: (noteChanged: boolean) => void;
}

export default function TransactionPopup({
  transaction,
  open,
  onClose,
}: TransactionPopupProps) {
  const [noteInput, setNoteInput] = useState<string>("");

  useEffect(() => {
    // get note
    const controller = new AbortController();

    async function getNote() {
      setNoteInput("");

      try {
        const response = await fetch(
          `http://localhost:8000/transactions/${transaction.transaction_id}/note`,
          {
            cache: "no-store",
            signal: controller.signal,
          },
        );

        const data = await response.json();
        setNoteInput(data.note);

      } catch (error) {
        if (error instanceof DOMException && error.name === "AbortError") {
          return;
        }

        console.error(error);
      }
    }
    getNote();

    return () => {
      controller.abort();
    };
  }, []);

  async function submitNote() {
    if (noteInput.length <= 1000) {      
      try {
        const response = await fetch(
          `http://localhost:8000/transactions/${transaction.transaction_id}/note`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
            note: noteInput,
            }),
          },
        );

        if (!response.ok) {
            throw new Error(`Failed to update note (${response.status})`);
        }
        
        onClose(true)
      } catch (error) {
        console.error("Failed to submit note:", error);
      }
    }
  }

  return (
    <Popup open={open} onClose={() => onClose(false)} modal>
      <div className="flex flex-col gap-1 shadow-2xl w-80 h-140 text-slate-100 bg-slate-900 border-2 border-slate-700">
        <div className="flex justify-end">
          <button
            className="flex items-center px-2 py-2 hover:cursor-pointer hover:bg-slate-700"
            onClick={() => onClose(false)}
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
            <span className="flex items-center gap-1 pb-1"><span className="material-symbols-outlined text-sm font-normal">sticky_note_2</span>
            <span className="font-bold mb-1">Notes</span></span>           

            <textarea
              className="border border-gray-700 w-full flex-1 p-1 text-sm resize-none focus:outline-none focus:border-slate-500"
              placeholder="Add notes for this transaction here"
              value={noteInput}
              onChange={(e) => setNoteInput(e.target.value)}
            />
          </div>
          <button
            onClick={submitNote}
            className="bg-slate-700 px-14 py-2 font-bold hover:cursor-pointer hover:border-slate-500 border border-transparent transition-colors"
          >
            Save
          </button>
        </div>
      </div>
    </Popup>
  );
}
