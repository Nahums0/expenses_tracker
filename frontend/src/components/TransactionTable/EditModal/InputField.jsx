import React from "react";

function InputField({ type, value, onChange, fieldData }) {
  if (type === "select") {
    return (
      <select
        value={value}
        className="w-full select-none rounded-none appearance-none bg-transparent border-none focus:outline-none"
        onChange={onChange}
      >
        {fieldData.map((item) => (
          <option key={item.id} value={item.categoryName}>
            {item.categoryName}
          </option>
        ))}
      </select>
    );
  }

  if (type === "date" && value) {
    value = value.split("T")[0];
  }

  return <input type={type} value={value ? value : ""} onChange={onChange} className="w-full" />;
}

export default InputField;
