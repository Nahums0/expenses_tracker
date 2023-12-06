export const initialFilters = {
  purchaseDate: { start: null, end: null },
  transactionAmount: { min: null, max: null },
  category: [],
  store: "",
  status: null,
};

export const getChangedFiltersAndSorts = (initialFilters, currentState, sortConfig) => {
  const arraysEqual = (a, b) => {
    if (a === b) return true;
    if (a == null || b == null) return false;
    if (a.length !== b.length) return false;

    for (let i = 0; i < a.length; ++i) {
      if (a[i] !== b[i]) return false;
    }
    return true;
  };

  const changed = [];

  // Check for sort configuration changes
  if (sortConfig && sortConfig.field !== null) {
    changed.push(["Sort", `${sortConfig.field} - ${sortConfig.direction}`]);
  }

  // Check each filter key
  for (const key in initialFilters) {
    if (initialFilters.hasOwnProperty(key)) {
      const initialFilter = initialFilters[key];
      const currentFilter = currentState[key];

      if (typeof initialFilter === "object" && !Array.isArray(initialFilter)) {
        for (const subKey in initialFilter) {
          if (initialFilter[subKey] !== currentFilter[subKey]) {
            changed.push([key, subKey]);
          }
        }
      } else if (Array.isArray(initialFilter)) {
        if (!arraysEqual(initialFilter, currentFilter)) {
          changed.push([key]);
        }
      } else {
        if (initialFilter !== currentFilter) {
          changed.push([key]);
        }
      }
    }
  }

  return changed;
};

export async function sendApiRequest(url, method, body, accessToken, setError) {
  try {
    const response = await fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify(body),
    });
    const data = await response.json();

    if (!response.ok || response.status !== 200) {
      setError({ server: data.message });
      return null;
    } else {
      return data;
    }
  } catch (error) {
    setError({ server: "Network error or unexpected problem occurred." });
    return null;
  }
}

export const headerMenuHandler = (event, column, menuWidth, showHeaderMenu, setShowHeaderMenu) => {
  const screenWidth = window.innerWidth;

  let xPos = event.clientX;
  let yPos = event.clientY;

  if (xPos + menuWidth > screenWidth) {
    xPos = screenWidth - menuWidth - 20;
  }

  if (showHeaderMenu.show) {
    setShowHeaderMenu({
      show: false,
    });
  } else {
    setShowHeaderMenu({
      show: true,
      x: xPos,
      y: yPos,
      type: column.filterType,
      columnData: column,
    });
  }
};

export const getVisibleTransactions = (transactions, currentPage, pageSize) => {
  if (!transactions || !transactions.transactions) {
    return [];
  }

  function getChunkIndex(index, chunkSize) {
    return index == 0 ? 0 : Math.floor(index / chunkSize);
  }

  const startIndex = Math.floor(currentPage * pageSize - pageSize);
  const endIndex = startIndex + pageSize;
  const visibleTransactions = Array(pageSize).fill(null);
  const chunkSize = transactions.chunkSize;

  for (let i = startIndex; i < endIndex; i++) {
    let chunkIndex = getChunkIndex(startIndex, chunkSize);
    if (!transactions.transactions[chunkIndex]) {
      break;
    }
    visibleTransactions[i - startIndex] = transactions.transactions[chunkIndex][i % chunkSize];
  }

  return visibleTransactions;
};