import React from "react";

function Headers({ headerMenuHandler }) {
  const columns = [
    { key: "purchaseDate", displayName: "Date", filterType: "date", sortable: true },
    { key: "transactionAmount", displayName: "Amount", filterType: "number", sortable: true },
    { key: "category", displayName: "Category", filterType: "select" },
    { key: "store", displayName: "Store", filterType: "text" },
    { key: "status", displayName: "Status", filterType: "boolean" },
    { key: "action", displayName: "Action" },
  ];

  return (
    <thead className="text-xs text-gray-700 uppercase bg-gray-50">
      <tr>
        {columns.map((column, idx) => (
          <th key={idx} scope="col" className={`px-6 py-3 text-left truncate`}>
            <span className="flex justify-between items-center">
              {column.displayName}
              {column.filterType && (
                <button
                  onClick={(event) => headerMenuHandler(event, column)}
                  className="cursor-pointer hover:opacity-80"
                >
                  <svg
                    className="w-2.5 h-2.5 ms-3"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 10 6"
                  >
                    <path
                      stroke="gray"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="m1 1 4 4 4-4"
                    />
                  </svg>
                </button>
              )}
            </span>
          </th>
        ))}
      </tr>
    </thead>
  );
}

export default Headers;
