import React, { useState } from "react";

const RecurringTransactionRow = React.memo(({ transaction, onEdit }) => {
  const formatFrequency = (freqValue, freqUnit) => {
    if (freqValue == 1) {
      freqValue = "";
      freqUnit = freqUnit.substring(0, freqUnit.length - 1);
    }
    return `Once every ${freqValue} ${freqUnit}`;
  };

  const calculateIsActive = (startDateStr, scannedAtStr) => {
    const now = new Date();
    const startDate = startDateStr ? new Date(startDateStr) : null;
    const scannedAt = scannedAtStr ? new Date(scannedAtStr) : null;

    // If the start date is in the future
    if (startDate > now) {
      const timeUntilActive = Math.round(
        (startDate - now) / (1000 * 60 * 60 * 24) // converting milliseconds to days
      );

      // Check if the start date is more than one day away
      if (timeUntilActive > 1) {
        return `Will be active in ${Math.floor(timeUntilActive)} days`;
      } else {
        return `Will be active later today`;
      }
    } else {
      // If the start date is in the past or present
      if (scannedAt && scannedAt >= startDate) {
        return "Yes"; // Active if scanned at or after the start date
      } else {
        return "Waiting for scan"; // Not active if not scanned yet
      }
    }
  };

  return (
    <tr className="bg-white border-b ">
      <td className={"px-6 py-4 text-left truncate "}>{transaction.transactionName}</td>
      <td className={"px-6 py-4 text-left truncate "}>{transaction.transaction.transactionAmount.toFixed(2)}</td>
      <td className={"px-6 py-4 text-left truncate "}>
        {formatFrequency(transaction.frequencyValue, transaction.frequencyUnit)}
      </td>
      <td className={"px-6 py-4 text-left truncate "}>{transaction.transaction.categoryName}</td>
      <td className={"px-6 py-4 text-left truncate "}>
        {calculateIsActive(transaction.startDate, transaction.scannedAt)}
      </td>
      <td
        className={"px-6 py-4 text-left truncate font-medium text-blue-600 hover:cursor-pointer"}
        onClick={() => onEdit(transaction)}
      >
        EDIT
      </td>
    </tr>
  );
});

export default RecurringTransactionRow;
