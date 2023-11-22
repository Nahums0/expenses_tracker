import React, { useEffect, useState } from "react";
import Headers from "./Headers";
import TransactionRow from "./Row";
import PendingRow from "./PendingRow";
import { useStore } from "@/store/store";
import EditModal from "./EditModal/EditModal";
import PagePicker from "@/components/Pagination/Pagination";

function TransactionsTable() {
  const { user, transactions, fetchAndSetTransactions } = useStore();
  const [showModal, setShowModal] = useState(false);
  const [currentTransaction, setCurrentTransaction] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(30);

  const totalPages = Math.ceil((transactions?.totalTransactionsCount || 0) / pageSize);

  useEffect(() => {
    fetchTransactions();
  }, [currentPage]);

  const fetchTransactions = () => {
    fetchAndSetTransactions(currentPage * pageSize - pageSize, pageSize * 2);
  };

  const getVisibleTransactions = () => {
    if (!transactions || !transactions.transactions) {
      return [];
    }

    function getChunkIndex(index, chunkSize) {
      return index == 0 ? 0 : Math.floor(index / chunkSize);
    }

    const startIndex = Math.floor(currentPage * pageSize - pageSize);
    const endIndex = startIndex + pageSize;
    const visibleTransactions = Array(pageSize).fill(null);
    const chunkSize = transactions.chunkSize;

    for (let i = startIndex; i < endIndex; i++) {
      let chunkIndex = getChunkIndex(startIndex, chunkSize);
      if (!transactions.transactions[chunkIndex]) {
        break;
      }
      visibleTransactions[i - startIndex] = transactions.transactions[chunkIndex][i % chunkSize];
    }

    return visibleTransactions;
  };

  const handleRowClick = (transaction) => {
    setCurrentTransaction(transaction);
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setCurrentTransaction(null);
  };

  const handlePageSizeChange = (event) => {
    setPageSize(Number(event.target.value));
    setCurrentPage(1);
  };

  const editTransactionHandler = async (transaction, setEditing, setError) => {
    try {
      const response = await fetch("/api/transactions/update-transaction", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${user.accessToken}`,
        },
        body: JSON.stringify(transaction),
      });
      console.log(transaction);
      const data = await response.json();

      if (!response.ok || response.status != 200) {
        console.error("Error creating new recurring transaction:", data.message, data.data);
        setError({ server: data.data ? data.data : { errors: data.message } });
      } else {
        fetchTransactions();
        handleCloseModal();
        console.log(data);
      }
    } catch (error) {
      console.error(error);
      setError({ server: "Network error or unexpected problem occurred." });
    }
  };

  return (
    <div className="shadow-md pr-6 h-full ">
      {transactions === null ? (
        <div className="w-full mt-48 align-middle text-center">
          <h1 className="align-middle text-4xl">Loading Transactions...</h1>
        </div>
      ) : (
        <>
          <div className="overflow-scroll h-9/10">
            <table className="w-full text-sm text-left">
              <Headers />
              <tbody>
                {getVisibleTransactions().map((transaction, index) =>
                  transaction ? (
                    <TransactionRow key={transaction.id} transaction={transaction} onEditClick={handleRowClick} />
                  ) : (
                    <PendingRow key={index} />
                  )
                )}
              </tbody>
            </table>
          </div>
          <div className="h-1/10 w-full bg-white border-t-2 flex flex-row ">
            <PagePicker
              className=""
              totalPages={totalPages}
              currentPage={currentPage}
              setCurrentPage={setCurrentPage}
              setPageSize={handlePageSizeChange}
            />
          </div>
        </>
      )}
      {showModal && (
        <EditModal onClose={handleCloseModal} transaction={currentTransaction} onSave={editTransactionHandler} />
      )}
    </div>
  );
}

export default TransactionsTable;
