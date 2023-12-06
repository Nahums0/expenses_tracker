import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import queryString from "query-string";
import Headers from "./Headers";
import TransactionRow from "./Row";
import PendingRow from "./PendingRow";
import { useStore } from "@/store/store";
import EditModal from "./EditModal/EditModal";
import PagePicker from "@/components/Pagination/Pagination";
import HeaderMenu from "./HeaderMenu";
import { sendApiRequest, headerMenuHandler, getVisibleTransactions, initialFilters } from "./helper";
import FilterBadges from "./FilterBadges";

function TransactionsTable() {
  const { transactions, fetchAndSetTransactions } = useStore();
  const [showModal, setShowModal] = useState(false);
  const [currentTransaction, setCurrentTransaction] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [sortConfig, setSortConfig] = useState(null);
  const [filters, setFilters] = useState(null);

  const location = useLocation();
  const navigate = useNavigate();

  const [isInitialLoad, setIsInitialLoad] = useState(location.search == null || location.search == "");

  // Header drop down menu configuration
  const [showHeaderMenu, setShowHeaderMenu] = useState({ show: false, x: 0, y: 0 });
  const menuWidth = 240;

  const totalPages = Math.ceil((transactions?.totalTransactionsCount || 0) / pageSize);

  // Fetching Transactions Based on State
  useEffect(() => {
    if (filters && sortConfig) {
      setUrlParamsAndNavigate();
      fetchTransactions();
    }
  }, [filters, sortConfig, currentPage]);

  // Initial Load with URL Params
  useEffect(() => {
    if (isInitialLoad) {
      setFilters(initialFilters);
      setSortConfig({ field: null, direction: null });
      setUrlParamsAndNavigate();
      setIsInitialLoad(false);
    } else {
      parseUrlParams();
    }
  }, []);

  const parseUrlParams = () => {
    const params = queryString.parse(location.search);
    const urlFilters = params.filter ? JSON.parse(params.filter) : {};
    const urlSortConfig = params.sort ? JSON.parse(params.sort) : { field: null, direction: null };
  
    // Merging URL filters with initialFilters
    const mergedFilters = { ...initialFilters };
    for (const key in initialFilters) {
      if (urlFilters.hasOwnProperty(key)) {
        mergedFilters[key] = urlFilters[key];
      }
    }
  
    // Merging URL sort config with initial sort config
    const mergedSortConfig = { ...initialFilters.sortConfig, ...urlSortConfig };
  
    // Update the state with merged values
    setFilters(mergedFilters);
    setSortConfig(mergedSortConfig);
    
    // Set current page, defaulting to 1 if not specified
    setCurrentPage(params.page ? Number(params.page) : 1);
  };
  

  const setUrlParamsAndNavigate = () => {
    const params = {};
    params.filter = JSON.stringify(filters);
    params.sort = JSON.stringify(sortConfig);
    if (currentPage !== 1) {
      params.page = currentPage;
    }

    navigate({
      pathname: location.pathname,
      search: queryString.stringify(params),
    });
  };

  const fetchTransactions = () => {
    console.log("fetching transactions", filters, sortConfig);
    fetchAndSetTransactions(currentPage * pageSize - pageSize, pageSize * 2, filters, sortConfig);
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

  const editTransactionHandler = async (transaction, setEditing, setError, user) => {
    const data = await sendApiRequest(
      "/api/transactions/update-transaction",
      "PUT",
      transaction,
      user.accessToken,
      setError
    );

    if (data) {
      fetchTransactions();
      setEditing(false);
    }
  };

  const transactionDeleteHandler = async (transactionId, setError, user) => {
    const data = await sendApiRequest(
      "/api/transactions/delete-transaction",
      "DELETE",
      { transactionId },
      user.accessToken,
      setError
    );

    if (data) {
      fetchTransactions();
      handleCloseModal();
    }
  };

  const resetFilter = (key, subKey = null) => {
    if (key == "Sort") {
      setSortConfig({ field: null, direction: null });
    } else {
      setFilters((currentFilters) => {
        const newFilters = { ...currentFilters };
        if (subKey) {
          newFilters[key] = { ...newFilters[key], [subKey]: initialFilters[key][subKey] };
        } else {
          newFilters[key] = initialFilters[key];
        }
        return newFilters;
      });
    }
  };

  return (
    <div className="pr-6 h-full flex flex-col">
      <FilterBadges
        initialState={initialFilters}
        currentState={filters}
        resetFilter={resetFilter}
        sortConfig={sortConfig}
      />
      {transactions === null ? (
        <div className="w-full mt-48 align-middle text-center">
          <h1 className="align-middle text-4xl">Loading Transactions...</h1>
        </div>
      ) : (
        <>
          <div className="overflow-scroll h-9/10">
            <table className="w-full text-sm text-left">
              <Headers
                headerMenuHandler={(event, column) =>
                  headerMenuHandler(event, column, menuWidth, showHeaderMenu, setShowHeaderMenu)
                }
              />
              <tbody>
                {getVisibleTransactions(transactions, currentPage, pageSize).map((transaction, index) =>
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
              pageSize={pageSize}
              totalPages={totalPages}
              currentPage={currentPage}
              setCurrentPage={setCurrentPage}
              setPageSize={handlePageSizeChange}
            />
          </div>
        </>
      )}
      {showModal && (
        <EditModal
          onClose={handleCloseModal}
          transaction={currentTransaction}
          onUpdate={editTransactionHandler}
          onDelete={transactionDeleteHandler}
        />
      )}
      {showHeaderMenu.show && (
        <HeaderMenu
          xPos={showHeaderMenu.x}
          yPos={showHeaderMenu.y}
          menuWidth={menuWidth}
          closeMenu={() => setShowHeaderMenu({ show: false })}
          setFilters={setFilters}
          setSortConfig={setSortConfig}
          menuType={showHeaderMenu.type}
          columnData={showHeaderMenu.columnData}
          initialFilters={filters}
        />
      )}
    </div>
  );
}

export default TransactionsTable;
