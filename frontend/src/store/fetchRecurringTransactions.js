export default async function fetchRecurringTransactions(userToken) {
  let transactions = null;

  try {
    const response = await fetch("/api/transactions/list-recurring-transactions", {
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
    console.error("Error fetching recurring transactions:", error);
  }

  return transactions;
}
