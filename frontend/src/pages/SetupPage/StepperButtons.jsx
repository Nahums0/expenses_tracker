import React from 'react';

const StepperButtons = ({ stepIndex, handlePreviousClick, handleNextClick, totalSteps }) => {
  const buttonBaseClass = "w-28 h-10 bg-navBg m-4 text-white rounded-md hover:shadow-2xl hover:scale-105 hover:opacity-90 transition-all";

  return (
    <div className="bg-white border-t-1 bottom-0 mb-0 absolute w-full">
      <div className="flex flex-row ml-1/24 w-11/12 gap-2 h-1/10 justify-end">
        {stepIndex > 1 && (
          <button
            onClick={handlePreviousClick}
            className={`${buttonBaseClass} ml-0 mr-0 `}
          >
            Previous
          </button>
        )}
        <button
          onClick={handleNextClick}
          className={`${buttonBaseClass} mr-0`}
        >
          {stepIndex >= totalSteps ? "Finish" : "Next"}
        </button>
      </div>
    </div>
  );
};

export default StepperButtons;
