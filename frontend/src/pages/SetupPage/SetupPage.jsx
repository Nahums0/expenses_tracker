import React, { useEffect } from "react";
import Stepper from "@/components/Stepper/Stepper";
import MonthlyBudgetForm from "./MonthlyBudgetForm";
import CategoryGrid from "./CategoryGrid";
import useStore from "@/store/store";
import StepperButtons from "./StepperButtons";
import { Navigate, useNavigate } from "react-router-dom";
import ProfileSetup from "@/components/ProfileSetup/ProfileSetup";
import "./SetupPage.css";

export default function SetupPage() {
  const {
    user,
    initialSetupData,
    setUser,
    setSetupMonthlyBudget,
    setSetupStepIndex,
    setSetupCategories,
    setSetupFullName,
    setSetupCurrency,
    setSetupCreditCardCredentials,
    setSetupErrorMessage,
  } = useStore();
  const { monthlyBudget, errorMessage, stepIndex, categories, fullName, currency, creditCardCredentials } =
    initialSetupData;

  const navigate = useNavigate();

  const submitHandler = async () => {
    var parsedBudget = parseInt(monthlyBudget);
    var filteredCategories = categories
      .filter((c) => c.budget > 0)
      .map((c) => {
        c.budget *= parsedBudget / 100;
        return c;
      });
    var formatttedFullname = fullName
      .split(" ")
      .map((s) => s[0].toUpperCase() + s.substr(1))
      .join(" ");

    const requestBody = {
      budget: parsedBudget,
      categories: filteredCategories,
      fullName: formatttedFullname,
      currency: currency,
      creditCardCredentials: creditCardCredentials,
    };

    try {
      const accessToken = user.accessToken;
      const response = await fetch("/api/users/setup-user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();

      if (!response.ok) {
        setSetupErrorMessage(data.message || "An error occurred");
      } else {
        setSetupErrorMessage("");
        setUser(data.data.user);
        navigate("/");
      }
    } catch (error) {
      console.log(error);
      setSetupErrorMessage("Network error or unexpected problem occurred.");
    }
  };

  const handleNextClick = () => {
    if (stepIndex == 2 && Math.floor(categories.reduce((total, category) => total + category.budget, 0)) > 100) {
      alert("Budget can't be over 100%");
      return;
    }
    if (stepIndex < stepperConfig.length) {
      setSetupStepIndex(stepIndex + 1);
    } else {
      submitHandler();
    }
  };

  const handlePreviousClick = () => {
    setSetupStepIndex(stepIndex - 1);
  };

  const stepperConfig = [
    {
      number: 1,
      title: "Set Monthly Budget",
      description: "Define your average monthly budget.",
    },
    {
      number: 2,
      title: "Category Allocation",
      description: "Spread your budget across categories.",
    },
    {
      number: 3,
      title: "Profile Setup",
      description: "Finish setting up your profile.",
    },
  ];

  useEffect(() => {
    if (user == null || user.initialSetupDone == true) {
      navigate("/");
    }
  });

  return (
    <div className="bg-bgColor w-full h-screen overflow-scroll">
      <div className="h-9/10 overflow-scroll">
        <h1 className="text-4xl text-main font-thin text-center pt-8 pb-8">Welcome to Expenses Tracker</h1>
        <div className="w-full">
          <Stepper steps={stepperConfig} currentStep={stepIndex} />
        </div>

        {stepIndex === 1 && (
          <MonthlyBudgetForm monthlyBudget={initialSetupData.monthlyBudget} setMonthlyBudget={setSetupMonthlyBudget} />
        )}

        {stepIndex === 2 && (
          <CategoryGrid monthlyBudget={monthlyBudget} categories={categories} setCategories={setSetupCategories} />
        )}

        {stepIndex === 3 && (
          <ProfileSetup
            user={user}
            fullName={fullName}
            setFullName={setSetupFullName}
            currency={currency}
            setCurrency={setSetupCurrency}
            creditCardCredentials={creditCardCredentials}
            setSetupCreditCardCredentials={setSetupCreditCardCredentials}
            errorMessage={errorMessage}
          />
        )}
      </div>
      <StepperButtons
        stepIndex={stepIndex}
        handlePreviousClick={handlePreviousClick}
        handleNextClick={handleNextClick}
        totalSteps={stepperConfig.length}
      />
    </div>
  );
}
