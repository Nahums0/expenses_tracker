import React from "react";
import CategoryCard from "@/components/CategoryCard/CategoryCard";

export default function TopCategories({ isLoading, categories }) {
  const renderCategoryCards = () => {
    if (isLoading || !categories || categories.reduce((total, c)=> total + c.monthlySpending, 0) == 0) {
      return [0, 1, 2].map((i) => (
        <CategoryCard key={`placeholder-${i}`} isPlaceholder={true} className={i === 2 ? "hidden lg:block" : ""} />
      ));
    }
    const topCategories = categories.sort((a, b) => b.monthlySpending - a.monthlySpending).slice(0, 3);

    return topCategories
      .map((category, index) => (
        <CategoryCard
          key={index}
          name={category.categoryName}
          amountSpent={category.monthlySpending}
          budget={category.monthlyBudget}
          className={index === 2 ? "hidden lg:block" : ""}
        />
      ));
  };

  return <>{renderCategoryCards()}</>;
}
