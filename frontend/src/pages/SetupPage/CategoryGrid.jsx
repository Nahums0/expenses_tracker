import React, { useEffect } from "react";
import CategoryCard from "./CategoryCard";
import Card from "@/components/Dashboard/Card";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus } from "@fortawesome/free-solid-svg-icons";

export default function CategoryGrid({ monthlyBudget, categories, setCategories }) {
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
        console.log(data);
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

    let updatedCategories = [...categories];
    updatedCategories[changedIndex] = {
      ...updatedCategories[changedIndex],
      budget: newPercentage,
      locked: true,
    };

    const totalUnlockedPercentage = updatedCategories.reduce(
      (acc, curr, index) => acc + (index !== changedIndex && !curr.locked ? curr.budget : 0),
      0
    );

    const remainingPercentage =
      100 - updatedCategories.reduce((acc, curr) => acc + (curr.locked ? curr.budget : 0), 0);

    // Minimum allocation for unlocked categories
    const minAllocation = remainingPercentage > 0 ? 0.1 : 0;
    let totalAllocated = 0;

    updatedCategories = updatedCategories.map((category, index) => {
      if (index === changedIndex || category.locked) {
        return category;
      } else {
        let adjustedBudget;
        if (totalUnlockedPercentage === 0) {
          // Allocate a minimum budget to unlocked categories if total unlocked percentage is zero
          adjustedBudget = minAllocation;
        } else {
          adjustedBudget = (category.budget / totalUnlockedPercentage) * remainingPercentage;
        }
        if (adjustedBudget < 0) {
          adjustedBudget = 0;
        }
        totalAllocated += adjustedBudget;
        return {
          ...category,
          budget: adjustedBudget,
        };
      }
    });

    // Adjust for any rounding errors
    if (totalAllocated < remainingPercentage) {
      const difference = remainingPercentage - totalAllocated;
      updatedCategories.find((category) => !category.locked && category.budget > 0).budget += difference;
    }

    setCategories(updatedCategories);
  };

  return (
    <div className="grid w-11/12 mt-8 mb-5 gap-4 lg:grid-cols-4 m-auto md:grid-cols-3 sm:grid-cols-2 overflow-scroll">
      {categories == null ? (
        <h1 className="text-5xl w-full text-center font-thin">Loading Categories...</h1>
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
          {Math.floor(categories.reduce((total, category) => total + category.budget, 0)) > 100 && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 fixed z-50 bottom-20 ">
              <p className="text-center">Budget is higher than 100%</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
