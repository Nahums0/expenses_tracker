import create from "zustand";
import { persist } from "zustand/middleware";
import fetchTransactions from "./fetchTransactions";
import fetchCategories from "./fetchCategories";
import fetchRecurringTransactions from "./fetchRecurringTransactions";
import fetchSpendingHistory from "./fetchSpendingHistory";

const initialState = {
  user: null,
  transactions: null,
  recurringTransactions: null,
  spendingHistory: {0:0},
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

// TODO: Add mecanism for a time based fetch
export const useStore = create(
  persist(
    (set) => ({
      ...initialState,
      reset: () => set(initialState),
      toggleSidebar: (isOpen) => set({ sidebarOpen: isOpen }),
      setUser: (newUser) => set({ user: newUser }),
      fetchAndSetTransactions: async (index = 0, length = 75) => {
        const { user } = useStore.getState();
        const { chunkSize, totalTransactionsCount, transactions, fetchTimestamp } = await fetchTransactions(
          user.accessToken,
          index,
          length
        );

        set((prevState) => {
          const currentTimestamp = new Date().getTime() / 1000;

          try {
            // Check if newly recived transactions should override previous state transactions
            // Based on null presence and time difference from the last fetch time
            const lastFetchTimestamp = prevState?.transactions?.fetchTimestamp || 0;
            const shouldOverride = currentTimestamp - lastFetchTimestamp > 60 * 60 * 24;

            if (shouldOverride) {
              return {
                transactions: { chunkSize, totalTransactionsCount, transactions, fetchTimestamp: currentTimestamp },
              };
            }

            const updatedTransactions = [];

            for (let i = 0; i < transactions.length; i++) {
              // Process transactions: fill nulls with previous state or null based on index
              if (transactions[i] === null) {
                updatedTransactions.push(
                  prevState.transactions.transactions.length <= i ? null : prevState.transactions.transactions[i]
                );
                continue;
              }

              updatedTransactions[i] = [];

              for (let j = 0; j < transactions[i].length; j++) {
                // Insert data into transactions array, choosing between previous and new data based on null presence
                updatedTransactions[i].push(
                  prevState.transactions.transactions[i] &&
                    prevState.transactions.transactions[i][j] !== null &&
                    transactions[i][j] === null
                    ? prevState.transactions.transactions[i][j]
                    : transactions[i][j]
                );
              }
            }

            return {
              transactions: {
                chunkSize,
                totalTransactionsCount,
                transactions: updatedTransactions,
                fetchTimestamp: lastFetchTimestamp,
              },
            };
          } catch (error) {
            console.error("Error merging transactions:", error);
            return {
              transactions: { chunkSize, totalTransactionsCount, transactions, fetchTimestamp: currentTimestamp },
            };
          }
        });
      },
      fetchAndSetCategories: async (accessToken) => {
        const categories = await fetchCategories(accessToken);
        set({ categories });
      },
      fetchAndSetRecurringTransactions: async (accessToken) => {
        const recurringTransactions = await fetchRecurringTransactions(accessToken);
        set({ recurringTransactions });
      },
      fetchAndSetSpendingHistory: async () => {
        const { user } = useStore.getState();
        const spendingHistory = await fetchSpendingHistory(user.accessToken);
        set({ spendingHistory });
      },
      setSetupMonthlyBudget: (budget) =>
        set((state) => ({
          initialSetupData: {
            ...state.initialSetupData,
            monthlyBudget: budget,
          },
        })),
      setSetupCategories: (categories) =>
        set((state) => ({
          initialSetupData: {
            ...state.initialSetupData,
            categories: categories,
          },
        })),
      setSetupErrorMessage: (message) =>
        set((state) => ({
          initialSetupData: {
            ...state.initialSetupData,
            errorMessage: message,
          },
        })),
      setSetupStepIndex: (index) =>
        set((state) => ({
          initialSetupData: {
            ...state.initialSetupData,
            stepIndex: index,
          },
        })),
      setSetupFullName: (fullName) =>
        set((state) => ({
          initialSetupData: {
            ...state.initialSetupData,
            fullName: fullName,
          },
        })),
      setSetupCurrency: (currency) =>
        set((state) => ({
          initialSetupData: {
            ...state.initialSetupData,
            currency: currency,
          },
        })),
      setSetupCreditCardCredentials: (creditCardCredentials) =>
        set((state) => ({
          initialSetupData: {
            ...state.initialSetupData,
            creditCardCredentials: creditCardCredentials,
          },
        })),
    }),
    {
      name: "zustand-store",
      getStorage: () => sessionStorage,
    }
  )
);

export default useStore;
