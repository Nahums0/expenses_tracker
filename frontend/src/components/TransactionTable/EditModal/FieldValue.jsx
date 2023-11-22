import React from 'react';
import InputField from './InputField';

const FieldValue = ({ value, color = 'gray', isEditable, onChange, type, fieldData, fieldKey }) => {
  const bgColorClass = `bg-${color}-200 pr-2 pl-2`;
  const textColorClass = `text-${color}-800`;

  return (
    <span className={`text-xs font-semibold px-2.5 py-0.5 col-span-2 h-7`}>
      {isEditable ? (
        <div className="p-1 w-full bg-gray-50 border border-gray-300">
          <InputField
            type={type}
            value={value}
            onChange={e => onChange(fieldKey, e.target.value)}
            fieldData={fieldData}
          />
        </div>
      ) : (
        <span className={`${textColorClass} ${bgColorClass} p-1 rounded-full`}>{value}</span>
      )}
    </span>
  );
};

export default FieldValue;
