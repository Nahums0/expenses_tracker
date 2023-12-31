import React from "react";

function Headers() {
  const columns =  ["Name", "Amount", "Freqency", "Category", "Is Active", "Action"]

  return (
    <thead className="text-xs text-gray-700 uppercase bg-gray-50">
      <tr>
        {columns.map((column, idx) => (
          <th
            key={idx}
            scope="col"
            className={`px-6 py-3 text-left truncate`}
          >
            {column}
          </th>
        ))}
      </tr>
    </thead>
  );

}

export default Headers;
