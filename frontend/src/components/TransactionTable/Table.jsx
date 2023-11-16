import React, { useEffect, useState } from "react";
import Headers from "./Headers";
import TransactionRow from "./Row";
import PendingRow from "./PendingRow";
import { useStore } from "@/store/store";
import EditModal from "./EditModal";
import PagePicker from "@/components/Pagination/Pagination";

function TransactionsTable() {
  const { transactions, fetchAndSetTransactions } = useStore();
  const [showModal, setShowModal] = useState(false);
  const [currentTransaction, setCurrentTransaction] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(30);

  const totalPages = Math.ceil(transactions.totalTransactionsCount / pageSize);

  useEffect(() => {
    fetchAndSetTransactions(currentPage * pageSize - pageSize, pageSize * 2);
  }, [currentPage]);

  const getVisibleTransactions = () => {
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
    console.log(event.target.value);
    setPageSize(Number(event.target.value));
    setCurrentPage(1);
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
                {getVisibleTransactions().map((transaction) =>
                  transaction ? (
                    <TransactionRow key={transaction.id} transaction={transaction} onEditClick={handleRowClick} />
                  ) : (
                    <PendingRow />
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
            {/* <PageSizeSelector className="w-1/3" pageSize={pageSize} handlePageSizeChange={handlePageSizeChange} /> */}
          </div>
        </>
      )}
      {showModal && <EditModal onClose={handleCloseModal} transaction={currentTransaction} />}
    </div>
  );
}

export default TransactionsTable;
