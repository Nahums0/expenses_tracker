import React, { useState, useCallback } from "react";
import Modal from "@/components/Modal/Modal";
import useStore from "@/store/store";
import ModalField from "./ModalField";
import ModalButtons from "./ModalButtons";
import { useFetchCategories, getEditableTransaction, prepareTransationsDataForPost } from "./helper";

function EditModal({ transaction, onClose, onSave }) {
  const { categories, fetchAndSetCategories } = useStore();
  const [editing, setEditing] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [editableTransaction, setEditableTransaction] = useState(getEditableTransaction(transaction, categories));

  useFetchCategories(fetchAndSetCategories, setErrorMessage);

  const handleChange = useCallback((key, value) => {
    setEditableTransaction((prev) => ({ ...prev, [key]: { ...prev[key], value } }));
  }, []);

  const toggleEditing = () => {
    if (editing) {
      onSave(
        prepareTransationsDataForPost(transaction.id, editableTransaction, categories),
        setEditing,
        setErrorMessage
      );
    } else {
      setEditing(!editing);
    }
  };

  return (
    <Modal
      onClose={onClose}
      header="Transaction Details"
      modalButtons={<ModalButtons editing={editing} onEditToggle={toggleEditing} onClose={onClose} />}
    >
      <div className="bg-white rounded-lg p-6 m-auto">
        <div className="grid grid-cols-1 gap-4 mb-4">
          {Object.entries(editableTransaction).map(([key, value]) => (
            <ModalField
              key={key}
              fieldKey={key}
              {...value}
              isEditable={editing && value.editable}
              onChange={handleChange}
            />
          ))}
        </div>
      </div>
      {errorMessage && <div className="error-message text-red-500">Internal server error: {errorMessage}</div>}
    </Modal>
  );
}

export default EditModal;
