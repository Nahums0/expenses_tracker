import React, { useEffect, useState } from "react";
import useStore from "@/store/store";
import CategoryCard from "@/components/CategoryCard/CategoryCard";

export default function TopCategories() {
  const { categories, user, fetchAndSetCategories } = useStore();
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function fetchCategories() {
      setIsLoading(true);
      try {
        await fetchAndSetCategories(user.accessToken);
      } catch (error) {
        console.error("Failed to fetch categories", error);
      }
      setIsLoading(false);
    }

    fetchCategories();
  }, []);

  if (isLoading || categories == null) {
    return (
      <>
        <CategoryCard isPlaceholder={true} />
        <CategoryCard isPlaceholder={true} />
        <CategoryCard isPlaceholder={true} />
      </>
    );
  }
  console.log(categories);
  return (
    <>
      {categories
        .sort((a, b) => (b.monthlySpending / b.monthlyBudget) * 100 - (a.monthlySpending / a.monthlyBudget) * 100)
        .slice(0, 3)
        .map((category, index) => (
          <CategoryCard
            key={category.categoryId}
            name={category.categoryName}
            amountSpent={category.monthlySpending}
            budget={category.monthlyBudget}
            className={index == categories.length - 1 && "hidden lg:block"}
          />
        ))}
    </>
  );
}
