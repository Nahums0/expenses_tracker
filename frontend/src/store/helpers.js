import fetchTransactions from "./fetchTransactions";
import fetchCategories from "./fetchCategories";
import fetchRecurringTransactions from "./fetchRecurringTransactions";
import fetchSpendingHistory from "./fetchSpendingHistory";

// Constants
const refetchThreshold = 5; // In seconds

export const initialState = {
  user: null,
  transactions: null,
  recurringTransactions: null,
  spendingHistory: { 0: 0 },
  categories: null,
  sidebarOpen: true,
  initialSetupData: {
    stepIndex: 1,
    monthlyBudget: 0,
    categories: [],
    errorMessage: null,
    fullName: "",
    currency: "₪",
    creditCardCredentials: null,
  },
};

// Common functions
const fetchAndSetData =
  (fetchFunction, set, dataKey, accessToken, currentData, useCache = true) =>
  async (...args) => {
    // If current state exists and was fetched more less than refetchThreshold seconds ago, don't refetch
    if (useCache && currentData && !_shouldRefetch(currentData.fetchTimestamp, refetchThreshold)) {
      return;
    }
    const newData = await fetchFunction(accessToken, currentData, ...args);
    set({ [dataKey]: newData });
  };

const _shouldRefetch = (lastFetch, thresholdSeconds) => {
  lastFetch = lastFetch || 0;
  const currentTime = new Date().getTime();
  return currentTime - lastFetch > thresholdSeconds * 1000;
};

// Fetch functions
export const fetchAndSetTransactions = (set) => (index, length, accessToken, currentTransactions) =>
  fetchAndSetData(fetchTransactions, set, "transactions", accessToken, currentTransactions, false)(index, length);

export const fetchAndSetCategories = (set, accessToken, currentCategories) =>
  fetchAndSetData(fetchCategories, set, "categories", accessToken, currentCategories, true);

export const fetchAndSetRecurringTransactions = (set, accessToken, recurringTransactions) =>
  fetchAndSetData(fetchRecurringTransactions, set, "recurringTransactions", accessToken, recurringTransactions);

export const fetchAndSetSpendingHistory = (set, accessToken, currentSpendingHistory) =>
  fetchAndSetData(fetchSpendingHistory, set, "spendingHistory", accessToken, currentSpendingHistory, true);

// Set functions
export const setSetupMonthlyBudget = (set) => (budget) => {
  set((state) => ({
    initialSetupData: {
      ...state.initialSetupData,
      monthlyBudget: budget,
    },
  }));
};

export const setSetupCategories = (set) => (categories) => {
  set((state) => ({
    initialSetupData: {
      ...state.initialSetupData,
      categories: categories,
    },
  }));
};

export const setSetupErrorMessage = (set) => (message) => {
  set((state) => ({
    initialSetupData: {
      ...state.initialSetupData,
      errorMessage: message,
    },
  }));
};

export const setSetupStepIndex = (set) => (index) => {
  set((state) => ({
    initialSetupData: {
      ...state.initialSetupData,
      stepIndex: index,
    },
  }));
};

export const setSetupFullName = (set) => (fullName) => {
  set((state) => ({
    initialSetupData: {
      ...state.initialSetupData,
      fullName: fullName,
    },
  }));
};

export const setSetupCurrency = (set) => (currency) => {
  set((state) => ({
    initialSetupData: {
      ...state.initialSetupData,
      currency: currency,
    },
  }));
};

export const setSetupCreditCardCredentials = (set) => (creditCardCredentials) => {
  set((state) => ({
    initialSetupData: {
      ...state.initialSetupData,
      creditCardCredentials: creditCardCredentials,
    },
  }));
};
