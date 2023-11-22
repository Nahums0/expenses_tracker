import { useEffect } from "react";

export const useFetchCategories = (fetchAndSetCategories, setErrorMessage) => {
  useEffect(() => {
    async function fetchData() {
      try {
        await fetchAndSetCategories();
      } catch (error) {
        console.error("Failed to fetch data", error);
        setErrorMessage("Failed to fetch categories.");
      }
    }

    fetchData();
  }, [fetchAndSetCategories, setErrorMessage]);
};

export const prepareTransationsDataForPost = (transactionId, transaction, categories) => {
  console.log(transaction.categoryName);
  let transformed = {
    transactionId,
    categoryId: categories.find((c) => c.categoryName == transaction.categoryName.value).id,
    transactionAmount: parseFloat(transaction.transactionAmount.value),
    paymentDate: transaction.paymentDate.value,
    purchaseDate: transaction.purchaseDate.value,
    merchantData: {
      name: transaction["merchantData.name"].value,
      address: transaction["merchantData.address"].value,
    },
  };

  // Handling for possible null or undefined values
  if (!transformed.merchantData.name) {
    delete transformed.merchantData.name;
  }
  if (!transformed.merchantData.address) {
    delete transformed.merchantData.address;
  }

  return transformed;
};

export const getEditableTransaction = (transaction, categories) => {
  return {
    transactionAmount: {
      label: "Amount",
      value: Math.abs(transaction.transactionAmount).toFixed(2),
      color: "green",
      editable: true,
      type: "text",
    },
    arn: {
      label: "ARN",
      value: transaction.arn,
      editable: false,
      type: "text",
    },
    categoryName: {
      label: "Category",
      value: transaction.categoryName,
      editable: true,
      type: "select",
      fieldData: categories,
    },
    purchaseDate: {
      label: "Purchased At",
      value: transaction.purchaseDate,
      editable: true,
      type: "date",
    },
    paymentDate: {
      label: "Approved At",
      value: transaction.paymentDate,
      editable: true,
      type: "date",
    },
    shortCardNumber: {
      label: "Card",
      value: transaction.shortCardNumber,
      color: "red",
      editable: false,
      type: "text",
    },
    "merchantData.name": {
      label: "Merchant Name",
      value: transaction.merchantData.name,
      editable: true,
      type: "text",
    },
    "merchantData.address": {
      label: "Merchant Address",
      value: transaction.merchantData.address,
      editable: true,
      type: "text",
    },
    originalAmount: {
      label: "Original Amount",
      value: `${transaction.originalAmount} ${transaction.originalCurrency}`,
      editable: false,
      type: "text",
    },
  };
};
