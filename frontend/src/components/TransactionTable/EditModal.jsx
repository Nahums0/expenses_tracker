import React, { useState } from "react";
import Modal from "@/components/Modal/Modal";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEdit, faCheck } from "@fortawesome/free-solid-svg-icons";

function getInputType(type, value, onChange) {
  const regularInputElement = (
    <input type={type} value={value} onChange={onChange} className="w-full" />
  );

  const selectElement = (
    <select className="w-full select-none rounded-none appearance-none bg-transparent border-none focus:outline-none">
      <option>b</option>
    </select>
  );

  switch (type) {
    case "text":
      return regularInputElement;
    case "date":
      return regularInputElement;
    case "select":
      return selectElement;
    case "number":
      return "number";
    default:
      return "text";
  }
}

const FieldValue = ({ value, color = "gray", isEditable, onChange, type }) => {
  const bgColorClass = `bg-${color}-200 pr-2 pl-2`;
  const textColorClass = `text-${color}-800`;
  const paddingValues = "p-1";

  return (
    <span className={`text-xs font-semibold px-2.5 py-0.5 col-span-2 h-7 `}>
      {isEditable ? (
        <div
          className={`${paddingValues} w-full bg-gray-50 border border-gray-300`}
        >
          {getInputType(type, value, onChange)}
        </div>
      ) : (
        <span
          className={`${textColorClass} ${bgColorClass} ${paddingValues} rounded-full`}
        >
          {value}
        </span>
      )}
    </span>
  );
};

const ModalField = ({ label, value, color, isEditable, onChange, type }) => {
  return (
    <div className="grid grid-cols-3 grid-col items-center justify-between space-x-4">
      <h1 className="text-gray-700 font-semibold col-span-1 truncate">
        {label}
      </h1>
      <FieldValue
        value={value}
        color={color}
        isEditable={isEditable}
        onChange={onChange}
        type={type}
      />
    </div>
  );
};

function EditModal({ transaction, onClose }) {
  const [editing, setEditing] = useState(false);
  const [editableTransaction, setEditableTransaction] = useState({
    ...transaction,
  });

  const toggleEditing = () => {
    if (editing) {
      // Save changes or call API to save changes
    }
    setEditing(!editing);
  };

  const handleChange = (key, value) => {
    setEditableTransaction((prev) => ({ ...prev, [key]: value }));
  };

  const transactionFields = [
    {
      label: "Amount",
      value: Math.abs( transaction.transactionAmount).toFixed(2),
      color: "green",
      editable: true,
      type: "text",
    },
    { label: "ARN", value: transaction.arn, editable: false, type: "text" },
    {
      label: "Category",
      value: transaction.categoryName,
      editable: true,
      type: "select",
    },
    {
      label: "Purchased At",
      value: transaction.purchaseDate,
      editable: true,
      type: "date",
    },
    {
      label: "Approved At",
      value: transaction.paymentDate,
      editable: true,
      type: "date",
    },
    {
      label: "Card",
      value: transaction.shortCardNumber,
      color: "red",
      editable: false,
      type: "text",
    },
    {
      label: "Merchant Name",
      value: transaction.merchantData.name,
      editable: false,
      type: "text",
    },
    {
      label: "Merchant Address",
      value: transaction.merchantData.address,
      editable: false,
      type: "text",
    },
    {
      label: "Original Amount",
      value: `${transaction.originalAmount} ${transaction.originalCurrency}`,

      editable: false,
      type: "text",
    },
  ];

  return (
    <Modal
      onClose={onClose}
      header={"Transaction Details"}
      modalButtons={
        <div className="w-20 flex justify-between align-middle">
          <FontAwesomeIcon
            icon={editing ? faCheck : faEdit}
            className="text-2xl m-auto pt-1 hover:opacity-60 cursor-pointer select-none"
            onClick={toggleEditing}
          />
          <button
            className="text-black text-4xl m-auto hover:opacity-60 cursor-pointer"
            onClick={onClose}
          >
            &times;
          </button>
        </div>
      }
    >
      <div className="bg-white">
        <div className="rounded-lg p-6  m-auto">
          <div className="grid grid-cols-1 gap-4 mb-4">
            {transactionFields.map((field, index) => (
              <ModalField
                key={index}
                label={field.label}
                value={field.value}
                color={field.color}
                isEditable={editing && field.editable}
                type={field.type}
                onChange={(e) => handleChange(field.key, e.target.value)}
              />
            ))}
          </div>
        </div>
      </div>
    </Modal>
  );
}

export default EditModal;
