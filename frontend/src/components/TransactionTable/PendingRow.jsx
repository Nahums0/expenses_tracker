import React from "react";

const PendingRow = () => {
  return (
    <tr className="bg-white border-b">
      <td colSpan="6" className="px-6 py-4 text-center text-gray-500">
        Loading transaction...
      </td>
    </tr>
  );
};

export default PendingRow;
