import React from "react";
import useStore from "@/store/store";
import { getCurrencySymbol } from "@/utils/helpers";

const formatDate = (date) => {
  return date ? (typeof date === "string" ? date.split("T")[0] : date.toISOString().split("T")[0]) : "";
};

const formatAmount = (transaction, currency) => {
  let amount = transaction.transactionAmount;
  let isPending = transaction.isPending;
  let currencySymbol = getCurrencySymbol(transaction.originalCurrency);

  return isPending ? `${transaction.originalAmount}${currencySymbol}` : `${Math.abs(amount).toFixed(2)}${currency}`;
};

const formatStatus = (isPending) => {
  return (
    <p className={`text-gray-400 ${!isPending && "text-gray-700"}`}>{isPending ? "Pre-Authorized" : "Authorized"}</p>
  );
};

const calculateAmountClass = (transaction) => {
  let isRefund = transaction.transactionAmount < 0;
  let colorClass = isRefund ? "text-green-500" : "text-red-500";
  if (transaction.isPending) {
    colorClass = "text-black"
  }
  return `px-6 py-4 font-medium text-left truncate ${colorClass}`;
};

const isCategorized = (transaction) => {
  return transaction.categoryName != null && transaction.categoryId !== -1;
};

const TransactionRow = ({ transaction, onEditClick }) => {
  const { user } = useStore();

  const dateString = formatDate(transaction.purchaseDate);
  const transactionAmountString = formatAmount(transaction, user.currency);
  const amountClass = calculateAmountClass(transaction);
  const categorized = isCategorized(transaction);

  return (
    <tr className="bg-white border-b">
      <td className="px-6 py-4 text-gray-500 text-left truncate">{dateString}</td>
      <td className={amountClass}>{transactionAmountString}</td>
      <td className={`px-6 py-4 text-xl font-light text-left truncate ${!categorized && "text-gray-400"}`}>
        {categorized ? transaction.categoryName : "Pending"}
      </td>
      <td className="px-6 py-4 text-gray-700 text-left truncate">{transaction.merchantData.name}</td>
      <td className="px-6 py-4 text-left truncate">{formatStatus(transaction.isPending)}</td>
      <td
        className="px-6 py-4 text-left truncate font-medium text-blue-500 hover:cursor-pointer"
        onClick={() => onEditClick(transaction)}
      >
        View
      </td>
    </tr>
  );
};

export default TransactionRow;
