import React from 'react';
import FieldValue from './FieldValue';

const ModalField = ({ label, value, color, isEditable, onChange, type, fieldData, fieldKey }) => {
    return (
    <div className="grid grid-cols-3 items-center justify-between space-x-4">
      <h1 className="text-gray-700 font-semibold col-span-1 truncate">{label}</h1>
      <FieldValue
        value={value}
        color={color}
        isEditable={isEditable}
        onChange={onChange}
        type={type}
        fieldKey={fieldKey}
        fieldData={fieldData}
      />
    </div>
  );
};

export default ModalField;
