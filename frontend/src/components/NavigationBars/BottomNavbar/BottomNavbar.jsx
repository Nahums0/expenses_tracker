import "./BottomNavbar.css";
import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

function BottomNavbar({ sideBarItems }) {
  return (
    <div className="fixed bottom-0 left-0 z-50 w-full h-16 bg-white border-t border-gray-200 dark:bg-gray-700 dark:border-gray-600">
      <div className="grid h-full max-w-lg grid-cols-4 mx-auto font-medium text-white">
        {sideBarItems.map((item, index) => (
          <button
            key={index}
            type="button"
            className="inline-flex flex-col items-center justify-center px-5 hover:bg-gray-50 dark:hover:bg-gray-800 group"
          >
            <FontAwesomeIcon icon={item.icon} className="fill-white" />
            <span className="text-sm">{item.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}

export default BottomNavbar;
