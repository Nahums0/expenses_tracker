export default async function fetchCategories(userToken) {
    console.log("Fetching categories...");
    let categories = null;
  
    try {
        const response = await fetch("/api/categories/get-user-categories", {
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
            categories = data.data;
        }
    } catch (error) {
        console.error("Error fetching categories:", error);
    }
  
    return categories;
}

