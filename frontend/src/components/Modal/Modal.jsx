import React from "react";
import useStore from "@/store/store";

function Modal({ onClose, header, children, bgClassName, modalClassName, modalButtons }) {
  const { sidebarOpen } = useStore();
  const handleModalContentClick = (e) => {
    e.stopPropagation();
  };

  return (
    <div
      onClick={onClose}
      className={`fixed ${
        sidebarOpen && "sm:ml-52"
      }  inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50 ${bgClassName}`}
    >
      <div
        className={`bg-white rounded-lg md:w-3/4 lg:w-3/4 w-full hover:cursor-default ${modalClassName}`}
        onClick={handleModalContentClick}
      >
        <div className="flex justify-between items-center p-6 border-b border-gray-200">
          <p className="text-2xl font-bold">{header}</p>
          {modalButtons ? (
            modalButtons
          ) : (
            <button className="text-black" onClick={onClose}>
              &times;
            </button>
          )}
        </div>
        <div className="p-6">{children}</div>
      </div>
    </div>
  );
}

export default Modal;
