import React, { useState, useEffect } from "react";
import CategoryCard from "./CategoryCard";
import Card from "@/components/Dashboard/Card";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus } from "@fortawesome/free-solid-svg-icons";

export default function CategoryGrid({
  monthlyBudget,
  categories,
  setCategories,
}) {
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await fetch("/api/categories/get-defaults", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        const data = await response.json();

        if (!response.ok) {
          setErrorMessage(response.statusText || "An error occurred");
        } else {
          var categoriesLength = data.data.length;
          setCategories(
            data.data.map((obj) => {
              return { ...obj, budget: 100 / categoriesLength };
            })
          );
        }
      } catch (error) {
        console.error(error);
        setErrorMessage("Network error or unexpected problem occurred.");
      }
    };
    fetchCategories();
  }, []);

  const handleCategoryNameChange = (newName, categoryIndex) => {
    categories[categoryIndex].categoryName = newName;
  };

  const handleCategoryDelete = (categoryIndex) => {
    console.log("categoryIndex", categoryIndex);
    setCategories(categories.filter((_, index) => index !== categoryIndex));
  };

  const handleCategoryAdd = () => {
    setCategories([
      ...categories,
      {
        id: categories[categories.length - 1].id + 1,
        categoryName: "New Category",
        budget: 0,
      },
    ]);
  };

  const handleBudgetSliderChange = (changedIndex, event) => {
    const newPercentage = parseFloat(event.target.value);
    // This is the total of percentages not including the one that has changed.
    const totalPercentage = categories.reduce(
      (acc, curr, index) => acc + (index !== changedIndex ? curr.budget : 0),
      0
    );

    var currentCategories = categories;
    if (totalPercentage === 0) {
      // If totalPercentage is 0, we distribute the remaining percentage equally.
      const remainingPercentage =
        (100 - newPercentage) / (currentCategories.length - 1);
      currentCategories = currentCategories.map((category, index) => {
        if (index === changedIndex) {
          return { ...category, budget: newPercentage };
        } else {
          return { ...category, budget: remainingPercentage };
        }
      });
    } else {
      // Calculate the factor to apply to other categories to adjust their budgets.
      const adjustFactor = (100 - newPercentage) / totalPercentage;
      currentCategories = currentCategories.map((category, index) => {
        if (index === changedIndex) {
          // The changed slider simply gets the new percentage.
          return { ...category, budget: newPercentage };
        } else {
          // Other sliders have their percentages adjusted.
          const adjustedBudget = category.budget * adjustFactor;
          return { ...category, budget: adjustedBudget };
        }
      });
    }
    setCategories(currentCategories);
  };

  return (
    <div className="grid w-11/12 mt-8 mb-5 gap-4 lg:grid-cols-4 m-auto md:grid-cols-3 sm:grid-cols-2 overflow-scroll">
      {categories == null ? (
        <h1 className="text-5xl w-full text-center font-thin">
          Loading Categories...
        </h1>
      ) : (
        <>
          {categories.map((category, index) => {
            const percentage = category.budget;
            const budget = (monthlyBudget / 100) * percentage;
            return (
              <CategoryCard
                key={category.id}
                category={category}
                index={index}
                handleCategoryNameChange={handleCategoryNameChange}
                budget={budget}
                percentage={percentage}
                handleBudgetSliderChange={handleBudgetSliderChange}
                handleCategoryDelete={handleCategoryDelete}
              />
            );
          })}
          <Card
            onClick={handleCategoryAdd}
            className={
              "flex flex-col justify-center hover:shadow-2xl hover:opacity-80 cursor-pointer transition-all hover:scale-105 h-28"
            }
          >
            <FontAwesomeIcon icon={faPlus} className="fa-4x" />
          </Card>
        </>
      )}
    </div>
  );
}
