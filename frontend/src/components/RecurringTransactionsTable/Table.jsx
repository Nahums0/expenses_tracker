import React, { useEffect, useState } from "react";
import Headers from "./Headers";
import TransactionRow from "./Row";
import { useStore } from "@/store/store";
import Modal from "@/components/Modal/Modal";
import NewTransactionModal from "./NewTransactionModal";
import EditTransactionModal from "./EditTransactionModal";

function RecurringTransactionsTable() {
  const { recurringTransactions, user, categories, fetchAndSetRecurringTransactions, fetchAndSetCategories } =
    useStore();
  const [isLoading, setIsLoading] = useState(true);
  const [modalState, setModalState] = useState({ isOpen: false, type: null, transaction: null });

  async function fetchTransactions() {
    setIsLoading(true);
    try {
      await Promise.all([fetchAndSetRecurringTransactions(), fetchAndSetCategories(useCache=true)]);
    } catch (error) {
      console.error("Failed to fetch transactions", error);
    }
    setIsLoading(false);
  }

  useEffect(() => {
    fetchTransactions();
  }, []);

  const openNewTransactionModal = () => {
    openModal("new");
  };

  const openModal = (type, transaction = null) => {
    setModalState({ isOpen: true, type, transaction });
  };

  const closeModal = () => {
    setModalState({ isOpen: false, type: null, transaction: null });
  };

  const transactionsApiRequestHandler = async (apiRoute, apiMethod, requestBody, setError) => {
    try {
      const response = await fetch(apiRoute, {
        method: apiMethod,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${user.accessToken}`,
        },
        body: JSON.stringify(requestBody),
      });
      console.log(requestBody);
      const data = await response.json();

      if (!response.ok || response.status != 200) {
        console.error("Error creating new recurring transaction:", data.message, data.data);
        setError({ server: data.data ? data.data : { errors: data.message } });
      } else {
        fetchTransactions();
        closeModal();
        console.log(data);
      }
    } catch (error) {
      console.error(error);
      setError({ server: "Network error or unexpected problem occurred." });
    }
  };

  const newTransactionHandler = async (transactionData, setError) => {
    transactionsApiRequestHandler("/api/transactions/create-recurring-transaction", "POST", transactionData, setError);
  };

  const editTransactionHandler = (transactionData, setError) => {
    transactionsApiRequestHandler("/api/transactions/update-recurring-transaction", "POST", transactionData, setError);
  };

  const onDelete = async (transactionData, setError) => {
    transactionsApiRequestHandler(
      "/api/transactions/delete-recurring-transaction",
      "DELETE",
      transactionData,
      setError
    );
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
                    onClick={openNewTransactionModal}
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
            <NewTransactionModal categories={categories} onSubmit={newTransactionHandler} />
          ) : (
            <EditTransactionModal
              categories={categories}
              transaction={modalState.transaction}
              onSubmit={editTransactionHandler}
              onDelete={onDelete}
            />
          )}
        </Modal>
      )}
    </div>
  );
}

export default RecurringTransactionsTable;
