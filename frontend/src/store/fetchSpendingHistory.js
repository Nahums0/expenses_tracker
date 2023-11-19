export default async function fetchSpendingHistory(userToken) {
    console.log("Fetching categories...");
    let spendingHistory = null;
  
    try {
        const response = await fetch("/api/transactions/get-monthly-spending-history", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${userToken}`
            },
        });
  
        if (!response.ok) {
            console.error("HTTP Error:", response.status, response.statusText);
        } else {
            const data = await response.json();
            console.log(data);
            spendingHistory = data.data;
        }
    } catch (error) {
        console.error("Error fetching categories:", error);
    }
  
    return spendingHistory;
}

