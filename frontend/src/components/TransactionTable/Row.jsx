import React, { useState, useCallback } from "react";
import useStore from "@/store/store";

const formatDate = (date) => {
  if (!date) return "";
  return typeof date === "string" ? date.split("T")[0] : date.toISOString().split("T")[0];
};

const TransactionRow = ({ transaction, onEditClick }) => {
  const { user } = useStore();

  const dateString = formatDate(transaction.purchaseDate);
  const isRefund = transaction.transactionAmount < 0;
  const transactionAmount = Math.abs(transaction.transactionAmount);
  const transactionAmountString = transactionAmount.toFixed(2);
  const amountClass = `px-6 py-4 ${isRefund ? "text-green-500" : "text-red-500"} font-bold text-left truncate`;
  const categorized = transaction.categoryName != null && transaction.categoryId != -1;

  return (
    <>
      <tr className="bg-white border-b">
        <td className="px-6 py-4 text-gray-500 text-left truncate">{dateString}</td>
        <td className={amountClass}>
          {transactionAmountString}
          {user.currency}
        </td>
        <td className={`px-6 py-4 text-xl font-light text-left truncate ${!categorized && " text-gray-400"}`}>
          {categorized ? transaction.categoryName : "Pending"}
        </td>
        <td className="px-6 py-4 text-gray-700 text-left truncate">{transaction.merchantData.name}</td>
        <td className="px-6 py-4 text-left truncate">{`${transaction.originalAmount} ${transaction.originalCurrency}`}</td>
        <td
          className="px-6 py-4 text-left truncate font-medium text-blue-600 hover:cursor-pointer"
          onClick={() => onEditClick(transaction)}
        >
          EDIT
        </td>
      </tr>
    </>
  );
};

export default TransactionRow;
