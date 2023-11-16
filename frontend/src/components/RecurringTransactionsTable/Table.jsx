import React, { useEffect, useState } from "react";
import Headers from "./Headers";
import TransactionRow from "./Row";
import { useStore } from "@/store/store";
import Modal from "@/components/Modal/Modal";
import NewTransactionModal from "./NewTransactionModal";
import EditTransactionModal from "./EditTransactionModal";

function RecurringTransactionsTable() {
  const { recurringTransactions, user, fetchAndSetRecurringTransactions } = useStore();
  const [isLoading, setIsLoading] = useState(true);
  const [modalState, setModalState] = useState({ isOpen: false, type: null, transaction: null });

  useEffect(() => {
    async function fetchCategories() {
      setIsLoading(true);
      try {
        await fetchAndSetRecurringTransactions(user.accessToken);
      } catch (error) {
        console.error("Failed to fetch categories", error);
      }
      setIsLoading(false);
    }

    fetchCategories();
  }, []);

  const newRecurringTransactionHandler = () => {
    openModal("new");
  };

  const openModal = (type, transaction = null) => {
    setModalState({ isOpen: true, type, transaction });
  };

  const closeModal = () => {
    setModalState({ isOpen: false, type: null, transaction: null });
  };

  return (
    <div className={`relative overflow-x-auto pr-6 ${!isLoading && recurringTransactions != null && "shadow-md"}`}>
      {recurringTransactions == null && !isLoading ? (
        <h1 className="text-red-500 text-xl text-center">
          Failed to fetch recurring transactions, please try again later
        </h1>
      ) : isLoading ? (
        <div className="w-full mt-48 align-middle text-center">
          <h1 className="align-middle text-4xl">Loading Recurring Transactions...</h1>
        </div>
      ) : (
        <>
          <table className="w-full text-sm text-left">
            <Headers />
            <tbody>
              {recurringTransactions.map((transaction) => (
                <TransactionRow
                  key={transaction.id}
                  transaction={transaction}
                  onEdit={() => openModal("edit", transaction)}
                />
              ))}
              <tr className="bg-white border-b">
                <td colSpan={6} className={"px-6 py-4 text-left truncate "}>
                  <div
                    className="text-center cursor-pointer hover:opacity-80 text-blue-500"
                    onClick={newRecurringTransactionHandler}
                  >
                    Add New Recurring Transaction
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </>
      )}
      {modalState.isOpen && (
        <Modal
          header={modalState.type === "new" ? "New Recurring Transaction" : "Edit Recurring Transaction"}
          onClose={closeModal}
        >
          {modalState.type === "new" ? (
            <NewTransactionModal categories={["Bills", "General", "Groceries"]} />
          ) : (
            <EditTransactionModal categories={["Bills", "General", "Groceries"]} transaction={modalState.transaction} />
          )}
        </Modal>
      )}
    </div>
  );
}

export default RecurringTransactionsTable;
