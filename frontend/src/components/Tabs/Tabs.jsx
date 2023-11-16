import "./Tabs.css";
import React, { useState } from "react";

function TabButton({ label, onClick, isActive }) {
  const activeStyles = isActive ? "border-b-blue-400 text-blue-500 hover:opacity-100" : "hover:opacity-60";
  return (
    <li className="mr-2">
      <button
        onClick={onClick}
        className={`inline-block p-4 border-b-2 border-transparent rounded-t-lg ${activeStyles}`}
      >
        {label}
      </button>
    </li>
  );
}

export default function Tabs({ tabs, tabIndex, setTabIndex }) {
  return (
    <div className="h-screen w-full">
      <div className="h-16  text-sm font-medium text-center text-gray-500  border-gray-200 dark:text-gray-400 dark:border-gray-700 ">
        <ul className="flex flex-wrap -mb-px ">
          {tabs.map((tab, index) => (
            <TabButton key={index} label={tab.name} isActive={index === tabIndex} onClick={() => setTabIndex(index)} />
          ))}
        </ul>
      </div>
      <div style={{ height: 'calc(100vh - 4rem)' }}>{tabs[tabIndex].childElements}</div>
    </div>
  );
}
