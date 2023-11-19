import React, { useEffect, useState } from "react";
import MonthlyMetricsCard from "./MonthlyMetricsCard";
import LatestTransactions from "./LatestTransactions";
import useStore from "@/store/store";
import { numberWithCommas } from "@/utils/helpers";
import TopCategories from "./TopCategories";
import Chart from "./Chart";

export default function Dashboard() {
  const { categories, user, spendingHistory, fetchAndSetCategories, fetchAndSetSpendingHistory } = useStore();
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function fetchData() {
      setIsLoading(true);
      try {
        // Start both fetch operations in parallel
        await Promise.all([fetchAndSetCategories(user.accessToken), fetchAndSetSpendingHistory()]);
      } catch (error) {
        console.error("Failed to fetch data", error);
      }
      setIsLoading(false);
    }

    fetchData();
  }, []);

  const currency = user.currency;
  const monthlyBudget = numberWithCommas(user.monthlyBudget);
  const monthlySpending = categories ? categories.reduce((sum, item) => sum + item.monthlySpending, 0) : 0;

  return (
    <div className="flex flex-col h-screen w-full">
      <h1 className="flex flex-col justify-center items-center h-28 w-72 shrink-0 text-[#0D4249] font-julius text-3xl normal-case font-normal leading-normal tracking-widest">
        Dashboard
      </h1>
      <div className="flex flex-row gap-4 m-9 mt-0 mb-0">
        <MonthlyMetricsCard title={"Monthly Spendings"} body={`${monthlySpending} / ${monthlyBudget}${currency}`} />
        <MonthlyMetricsCard title={"Daily Average"} body={"125₪"} />
        <MonthlyMetricsCard title={"Daily Surplus"} body={"560₪"} className={"hidden lg:block"} />
      </div>
      <div className="flex flex-row m-9 mb-4 mt-4 gap-4 h-full">
        <div className="w-2/3 flex flex-col gap-4">
          <div className="flex flex-row gap-4 justify-between">
            <TopCategories isLoading={isLoading} categories={categories} />
          </div>
          <div className="w-full h-full">
            <Chart data={spendingHistory} />
          </div>
        </div>
        <div className="w-1/3 ">
          <LatestTransactions />
        </div>
      </div>
    </div>
  );
}
