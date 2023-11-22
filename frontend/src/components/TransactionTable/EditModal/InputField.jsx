import React from "react";

function InputField({ type, value, onChange, fieldData }) {
  if (type === "select") {
    return (
      <select className="w-full select-none rounded-none appearance-none bg-transparent border-none focus:outline-none">
        {fieldData.map((item) => (
          <option key={item.id} value={item.id}>
            {item.categoryName}
          </option>
        ))}
      </select>
    );
  }

  if (type === "date") {
    value = value.split("T")[0];
  }

  return <input type={type} value={value ? value : ""} onChange={onChange} className="w-full" />;
}

export default InputField;
