import React, { useState, useEffect } from "react";
import TooltipLabel from "@/components/TooltipLabel/TooltipLabel";

const EditTransactionModal = ({ categories, onSubmit, transaction }) => {
  const [formData, setFormData] = useState({
    name: transaction.transactionName,
    amount: transaction.transaction.transactionAmount,
    frequencyUnit: transaction.frequencyUnit,
    frequencyValue: transaction.frequencyValue,
    category: transaction.transaction.categoryName,
    startDate: transaction.startDate.split("T")[0],
  });
  const [errorMessages, setErrorMessages] = useState({
    name: "",
    amount: "",
    frequencyValue: "",
    startDate: "",
  });

  const validateInput = () => {
    let errors = {};
    let isValid = true;

    // Validate name
    if (!formData.name) {
      errors.name = "Name is required";
      isValid = false;
    }

    // Validate amount
    if (!formData.amount || formData.amount <= 0) {
      errors.amount = "Amount must be a positive number";
      isValid = false;
    }

    // Validate frequencyValue
    if (![1, 2, 3, 4].includes(formData.frequencyValue)) {
      errors.frequencyValue = "Invalid frequency value";
      isValid = false;
    }

    // Validate startDate
    const today = new Date();
    const startDate = new Date(formData.startDate);
    if (startDate < today) {
      errors.startDate = "Start date cannot be in the past";
      isValid = false;
    }

    setErrorMessages(errors);
    return isValid;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateInput()) {
      onSubmit(formData);
    }
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const renderInputField = (label, name, type, tooltipText) => (
    <>
      <TooltipLabel label={label} htmlFor={name} tooltipText={tooltipText} />
      <input
        type={type}
        name={name}
        id={name}
        required
        className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        value={formData[name]}
        onChange={handleInputChange}
      />
      {errorMessages[name] && <div className="error-message text-red-500">{errorMessages[name]}</div>}
    </>
  );

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      {renderInputField("Name", "name", "text", "Label this transaction...")}
      {renderInputField("Amount", "amount", "number", "Set the amount...")}
      <div>
        <TooltipLabel
          label="Frequency"
          htmlFor="frequency"
          tooltipText="Set the interval at which this transaction will repeat"
        />
        <div className="flex space-x-2">
          <select
            name="frequencyValue"
            id="frequencyValue"
            required
            className="mt-1 block w-1/2 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            value={formData.frequencyValue}
            onChange={handleInputChange}
          >
            {[1, 2, 3, 4].map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
          <select
            name="frequencyUnit"
            id="frequencyUnit"
            required
            className="mt-1 block w-1/2 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            value={formData.frequencyUnit}
            onChange={handleInputChange}
          >
            {["days", "weeks", "months"].map((unit) => (
              <option key={unit} value={unit}>
                {unit}
              </option>
            ))}
          </select>
        </div>
        {errorMessages.frequencyValue && (
          <div className="error-message text-red-500">{errorMessages.frequencyValue}</div>
        )}
      </div>
      <div>
        <TooltipLabel
          label="Category"
          htmlFor="category"
          tooltipText="Classify this transaction into a relevant category"
        />
        <select
          name="category"
          id="category"
          required
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          value={formData.category}
          onChange={handleInputChange}
        >
          {categories.map((category) => (
            <option key={category} value={category}>
              {category}
            </option>
          ))}
        </select>
      </div>

      {renderInputField(
        "Start Date",
        "startDate",
        "date",
        "Set the initial date for the recurring transaction's first occurrence"
      )}

      <button
        type="submit"
        className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
      >
        Update
      </button>
    </form>
  );
};

export default EditTransactionModal;