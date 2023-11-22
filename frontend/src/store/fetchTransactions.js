export default async function fetchTransactions(userToken, prevState, index=0, length=75) {
  let transactions = {
    transactions: null,
    totalTransactionsCount: 0,
    chunkSize: 0,
  };

  try {
    const response = await fetch(`/api/transactions/list-transactions?index=${index}&length=${length}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${userToken}`,
      },
    });

    if (!response.ok) {
      console.error("HTTP Error:", response.status, response.statusText);
    } else {
      console.log("Fetching new transactions...");

      const data = await response.json();
      transactions = mergeTransactions(prevState, data.data);
    }
  } catch (error) {
    console.error("Error fetching transactions:", error);
  }
  return transactions;
}

function mergeTransactions(prevState, fetchedData) {
  const { chunkSize, totalTransactionsCount, transactions: fetchedTransactions } = fetchedData;
  try {
    const currentTimestamp = new Date().getTime();

    // Check if newly recived transactions should override previous state transactions
    // This logic will clear all data that is older than 1 day
    const lastFetchTimestamp = prevState?.transactions?.fetchTimestamp || 0;
    const shouldOverride = currentTimestamp - lastFetchTimestamp > 60 * 60 * 24;

    if (shouldOverride) {
      return {
          chunkSize,
          totalTransactionsCount,
          transactions: fetchedTransactions,
          fetchTimestamp: currentTimestamp,
      };
    }

    // Merge new transactions with existing ones, filling gaps with previous data if necessary
    const updatedTransactions = fetchedTransactions.map(
      (transactionGroup, i) =>
        transactionGroup?.map((transaction, j) =>
          transaction === null && prevState.transactions.transactions[i]?.[j] !== null
            ? prevState.transactions.transactions[i][j]
            : transaction
        ) ?? prevState.transactions.transactions[i]
    );

    return {
        chunkSize,
        totalTransactionsCount,
        transactions: updatedTransactions,
        fetchTimestamp: lastFetchTimestamp,
    };
  } catch (error) {
    console.error("Error merging transactions:", error);
    // On error, reset transactions with fetched data
    return {
        chunkSize,
        totalTransactionsCount,
        transactions: transactions,
        fetchTimestamp: currentTimestamp,
    };
  }
}
