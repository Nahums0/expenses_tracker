import React, { useEffect, useState } from "react";
import useStore from "@/store/store";
import CategoryCard from "@/components/CategoryCard/CategoryCard";

export default function TopCategories({isLoading, categories}) {
  if (isLoading || categories == null) {
    return (
      <>
        <CategoryCard isPlaceholder={true} />
        <CategoryCard isPlaceholder={true} />
        <CategoryCard isPlaceholder={true} className={"hidden lg:block"} />
      </>
    );
  }

  return (
    <>
      {categories
        .sort((a, b) => b.monthlySpending - a.monthlySpending)
        .slice(0, 3)
        .map((category, index) => (
          <CategoryCard
            key={category.categoryId}
            name={category.categoryName}
            amountSpent={category.monthlySpending}
            budget={category.monthlyBudget}
            className={index == 2 && "hidden lg:block"}
          />
        ))}
    </>
  );
}
