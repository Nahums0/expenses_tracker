import React from "react";
import useStore from "./setupStore";

export default function MonthlyBudgetForm({ monthlyBudget, setMonthlyBudget }) {
  const handleInputChange = (event) => {
    const value = event.target.value;
    if (!isNaN(value) && Number(value) >= 0) {
      setMonthlyBudget(value);
    }
  };

  return (
    <div className="flex flex-col w-2/3 h-1/3 gap-4 justify-center m-auto">
      <label
        htmlFor="monthlyBudget"
        className="text-4xl font-thin text-main text-center"
      >
        Set Your Monthly Budget
      </label>
      <input
        type="number"
        id="monthlyBudget"
        name="monthlyBudget"
        className="border-2 text-4xl p-4 text-center ml-auto mr-auto rounded-md"
        min={0}
        value={monthlyBudget}
        onChange={handleInputChange}
        required
      />
    </div>
  );
}
