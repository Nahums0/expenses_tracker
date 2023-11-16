export default async function fetchTransactions(userToken, index, length) {
  console.log("Fetching transactions...");
  let transactions = {
    transactions: null,
    totalTransactionsCount: 0,
    chunkSize: 0,
  };

  try {
    const response = await fetch(`/api/transactions/list?index=${index}&length=${length}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${userToken}`,
      },
    });

    if (!response.ok) {
      console.error("HTTP Error:", response.status, response.statusText);
    } else {
      const data = await response.json();
      transactions = data.data;
    }
  } catch (error) {
    console.error("Error fetching transactions:", error);
  }

  return transactions;
}
