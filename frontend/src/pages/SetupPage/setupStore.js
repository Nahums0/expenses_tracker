import create from "zustand";
import { persist } from "zustand/middleware";

const initialState = {
  user: null,
  initialSetupData: {
    stepIndex: 1,
    monthlyBudget: 0,
    categories: [],
    errorMessage: null,
  },
};

const useStore = create(
  persist(
    (set) => ({
      ...initialState,
      setMonthlyBudget: (budget) => set((state) => ({
        initialSetupData: {
          ...state.initialSetupData,
          monthlyBudget: budget,
        },
      })),
      setCategories: (categories) => set((state) => ({
        initialSetupData: {
          ...state.initialSetupData,
          categories: categories,
        },
      })),
      setErrorMessage: (message) => set((state) => ({
        initialSetupData: {
          ...state.initialSetupData,
          errorMessage: message,
        },
      })),
      setStepIndex: (index) => set((state) => ({
        initialSetupData: {
          ...state.initialSetupData,
          stepIndex: index,
        },
      })),
      reset: () => set(initialState),
    }),
    {
      name: "zustand-store",
      getStorage: () => sessionStorage,
    }
  )
);

export default useStore;
