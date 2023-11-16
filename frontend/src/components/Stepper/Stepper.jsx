import React, { useState } from 'react';

const Step = ({ number, title, description, isCompleted, isActive }) => {
  const textColor = isActive ? 'text-blue-600 dark:text-blue-500' : 'text-gray-500 dark:text-gray-400';
  const borderColor = isActive ? 'border-blue-600 dark:border-blue-500' : 'border-gray-500 dark:border-gray-400';

  return (
    <li className={`flex items-center ${textColor} space-x-2.5`}>
      <span className={`flex items-center justify-center w-8 h-8 border ${borderColor} rounded-full shrink-0`}>
        {number}
      </span>
      <span>
        <h3 className="font-medium leading-tight">{title}</h3>
        <p className="text-sm hidden sm:block">{description}</p>
      </span>
    </li>
  );
};

const Stepper = ({ steps, currentStep }) => {
  return (
    <ol className="w-full space-y-4 sm:flex sm:space-x-8 sm:space-y-0 flex items-center justify-center">
      {steps.map((step, index) => (
        <Step
          key={step.number}
          number={step.number}
          title={step.title}
          description={step.description}
          isCompleted={currentStep > index + 1}
          isActive={currentStep === index + 1}
        />
      ))}
    </ol>
  );
};

export default Stepper;
