import React from "react";
import MonthlyMetricsCard from "./MonthlyMetricsCard";
import LatestTransactions from "./LatestTransactions";
import useStore from "@/store/store";
import { numberWithCommas } from "@/utils/helpers";
import TopCategories from "./TopCategories";
import Chart from "./Chart";

export default function Dashboard() {
  const { user } = useStore();

  const spendingData = [
    1200, 900, 1400, 1300, 1000, 1180, 1290, 1250, 1300, 1400, 1500, 1100,
  ];
  const spendingLabels = [
    "2022-01-01",
    "2022-02-01",
    "2022-03-01",
    "2022-04-01",
    "2022-05-01",
    "2022-06-01",
    "2022-07-01",
    "2022-08-01",
    "2022-09-01",
    "2022-10-01",
    "2022-11-01",
    "2022-12-01",
  ];
  const currency = user.currency;
  const monthlyBudget = numberWithCommas(user.monthlyBudget);

  return (
    <div className="flex flex-col h-screen w-full">
      <h1 className="flex flex-col justify-center items-center h-28 w-72 shrink-0 text-[#0D4249] font-julius text-3xl normal-case font-normal leading-normal tracking-widest">
        Dashboard
      </h1>
      <div className="flex flex-row gap-4 m-9 mt-0 mb-0">
        <MonthlyMetricsCard
          title={"Monthly Spendings"}
          body={`1,000₪ / ${monthlyBudget}${currency}`}
        />
        <MonthlyMetricsCard title={"Daily Average"} body={"125₪"} />
        <MonthlyMetricsCard
          title={"Daily Surplus"}
          body={"560₪"}
          className={"hidden lg:block"}
        />
      </div>
      <div className="flex flex-row m-9 mb-4 mt-4 gap-4 h-full">
        <div className="w-2/3 flex flex-col gap-4">
          <div className="flex flex-row gap-4 justify-between">
            <TopCategories />
          </div>
          <div className="w-full h-full">
            <Chart data={spendingData} labels={spendingLabels} />
          </div>
        </div>
        <div className="w-1/3 ">
          <LatestTransactions />
        </div>
      </div>
    </div>
  );
}
