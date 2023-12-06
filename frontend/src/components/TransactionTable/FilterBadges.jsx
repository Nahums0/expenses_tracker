import React from "react";
import { getChangedFiltersAndSorts } from "./helper";

const FilterBadge = ({ label, onReset }) => {
  return (
    <span className="bg-blue-100 text-blue-800 text-xs font-medium me-3 px-3  w-16 py-1 rounded relative">
      {label}
      <button
        onClick={onReset}
        className="absolute top-[-4px] right-[-4px] w-4 h-4 bg-blue-100 rounded-full text-xs text-gray-600 transition-transform  hover:scale-150"
      >
        &#x2715; {/* Close icon */}
      </button>
    </span>
  );
};

const FilterBadges = ({ initialState, currentState, resetFilter, sortConfig }) => {
  if (currentState == null) {
    return <></>;
  }

  const renderBadge = (key, subKey = null) => {
    const label = subKey ? `${key} ${subKey}` : key;
    return <FilterBadge key={label} label={label} onReset={() => resetFilter(key, subKey)} />;
  };

  const renderBadges = () => {
    const badges = [];
    const changedFilters = getChangedFiltersAndSorts(initialState, currentState, sortConfig);

    for (const i in changedFilters) {
      const element = changedFilters[i];

      if (element.length > 1) {
        badges.push(renderBadge(element[0], element[1]));
      } else {
        badges.push(renderBadge(element[0]));
      }
    }
    return badges;
  };

  return <div className="mb-3">{renderBadges()}</div>;
};

export default FilterBadges;
