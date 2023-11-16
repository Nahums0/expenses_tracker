import React, { useState } from "react";

const TooltipLabel = ({ label, htmlFor, tooltipText }) => {
  const [showTooltip, setShowTooltip] = useState(false);

  return (
    <div className="relative">
      <label
        htmlFor={htmlFor}
        className="block text-sm font-medium text-gray-700"
      >
        {label} <span
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
        
        >(?)</span>
      </label>
      {showTooltip && (
        <div className="absolute z-10 inline-block px-3 py-2 text-sm font-medium text-white bg-gray-900 rounded-lg shadow-sm">
          {tooltipText}
        </div>
      )}
    </div>
  );
};

export default TooltipLabel;
