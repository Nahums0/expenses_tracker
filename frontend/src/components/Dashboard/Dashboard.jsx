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
        await Promise.all([fetchAndSetCategories(true), fetchAndSetSpendingHistory()]);
      } catch (error) {
        console.error("Failed to fetch data", error);
      }
      setIsLoading(false);
    }

    fetchData();
  }, []);

  const _getTotalDaysInMonth = (date) => {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
  };

  const _calculateDailySurplus = () => {
    const currentDate = new Date();
    const monthDay = currentDate.getDate();
    const totalDaysInMonth = _getTotalDaysInMonth(currentDate);
    const dailyBudget = monthlyBudget / totalDaysInMonth;

    return Math.round(monthDay * dailyBudget - monthlySpending);
  };

  const _calculateDailyAverage = () => {
    const currentDate = new Date();
    const monthDay = currentDate.getDate();
    return Math.round(monthlySpending / monthDay);
  };

  const _calculateTargetDailyAverage = () =>{
    const totalDaysInMonth = _getTotalDaysInMonth(new Date());
    const targetDailyBudget = monthlyBudget / totalDaysInMonth;

    return Math.round(targetDailyBudget);
  }

  const currency = user.currency;
  const monthlyBudget = user.monthlyBudget;
  const monthlySpending = categories ? categories.reduce((sum, item) => sum + item.monthlySpending, 0) : 0;

  return (
    <div className="flex flex-col h-screen w-full">
      <div className="h-28">
        <h1 className="flex flex-col justify-center items-center h-28 w-72 shrink-0 text-[#0D4249] font-julius text-3xl normal-case font-normal leading-normal tracking-widest">
          Dashboard
        </h1>
      </div>
      <div className="flex flex-row gap-3 ml-9 mr-9 h-32">
        <MonthlyMetricsCard
          title={"Monthly Spendings"}
          body={`${monthlySpending} / ${numberWithCommas(monthlyBudget)}${currency}`}
        />
        <MonthlyMetricsCard
          title={"Monthly Surplus"}
          body={`${_calculateDailySurplus(monthlyBudget, monthlySpending)}₪`}
        />
        <MonthlyMetricsCard
          title={"Daily Average"}
          body={`${_calculateDailyAverage()}₪ / ${_calculateTargetDailyAverage()}₪`}
          className={"hidden lg:flex"}
        />
      </div>
      <div className="flex flex-row m-9 gap-4" style={{ height: " calc(100vh - 14rem - 4rem)" }}>
        <div className="w-2/3 flex flex-col">
          <div className="flex flex-row gap-4 justify-between h-[15rem] mb-4">
            <TopCategories isLoading={isLoading} categories={categories} />
          </div>
          <div className="w-full h-full">
            <Chart data={spendingHistory} />
          </div>
        </div>
        <div className="w-1/3 h-full">
          <LatestTransactions />
        </div>
      </div>
    </div>
  );
}
