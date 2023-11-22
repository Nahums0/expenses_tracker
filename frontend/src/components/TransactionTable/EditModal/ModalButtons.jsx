import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit, faCheck } from '@fortawesome/free-solid-svg-icons';

const ModalButtons = ({ editing, onEditToggle, onClose }) => {
  return (
    <div className="w-20 flex justify-between align-middle">
      <FontAwesomeIcon
        icon={editing ? faCheck : faEdit}
        className="text-2xl m-auto pt-1 hover:opacity-60 cursor-pointer select-none"
        onClick={onEditToggle}
      />
      <button className="text-black text-4xl m-auto hover:opacity-60 cursor-pointer" onClick={onClose}>
        &times;
      </button>
    </div>
  );
};

export default ModalButtons;
