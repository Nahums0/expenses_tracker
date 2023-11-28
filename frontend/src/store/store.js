import create from "zustand";
import { persist } from "zustand/middleware";
import {
  fetchAndSetTransactions,
  fetchAndSetCategories,
  fetchAndSetRecurringTransactions,
  fetchAndSetSpendingHistory,
  setSetupMonthlyBudget,
  setSetupCategories,
  setSetupErrorMessage,
  setSetupStepIndex,
  setSetupFullName,
  setSetupCurrency,
  setSetupCreditCardCredentials,
  initialState,
} from "./helpers";

export const useStore = create(
  persist(
    (set, get) => ({
      ...initialState,
      reset: () => set(initialState),
      toggleSidebar: (isOpen) => set({ sidebarOpen: isOpen }),
      setUser: (newUser) => set({ user: newUser }),

      // fetchAndSet functions
      fetchAndSetTransactions: (index, length, useCache = false) => {
        const { user, transactions } = get();
        fetchAndSetTransactions(set)(index, length, user.accessToken, transactions, useCache);
      },
      fetchAndSetCategories: (useCache = false) => {
        const { user, categories } = get();
        fetchAndSetCategories(set, user.accessToken, categories, useCache)();
      },
      fetchAndSetRecurringTransactions: (useCache = false) => {
        const { user, recurringTransactions } = get();
        fetchAndSetRecurringTransactions(set, user.accessToken, recurringTransactions, useCache)();
      },
      fetchAndSetSpendingHistory: (useCache = false) => {
        const { user, spendingHistory } = get();
        fetchAndSetSpendingHistory(set, user.accessToken, spendingHistory, useCache)();
      },

      // Set functions
      setSetupMonthlyBudget: setSetupMonthlyBudget(set),
      setSetupCategories: setSetupCategories(set),
      setSetupErrorMessage: setSetupErrorMessage(set),
      setSetupStepIndex: setSetupStepIndex(set),
      setSetupFullName: setSetupFullName(set),
      setSetupCurrency: setSetupCurrency(set),
      setSetupCreditCardCredentials: setSetupCreditCardCredentials(set),
    }),
    {
      name: "zustand-store",
      getStorage: () => sessionStorage,
    }
  )
);

export default useStore;
