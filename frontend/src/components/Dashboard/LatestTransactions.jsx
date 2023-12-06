import Loading from "@/components/Loading/Loading";
import Card from "./Card";
import useStore from "@/store/store";
import React, { useEffect } from "react";
import { getCurrencySymbol } from "@/utils/helpers";

const LatestTransactions = () => {
  const { transactions, user, fetchAndSetTransactions } = useStore();

  const formatDate = (date) => {
    if (!date) return "";
    return typeof date === "string" ? date.split("T")[0] : date.toISOString().split("T")[0];
  };

  const getAmountBadgeColor = (amount) => {
    return amount < 0 ? "text-green-600 bg-green-200" : "text-red-400 bg-red-100";
  };

  const getTransactionAmount = (transaction) => {
    let currency = user.currency
    let amount = Math.abs(transaction.transactionAmount).toFixed(2);
    if (transaction.isPending){
      currency = getCurrencySymbol(transaction.originalCurrency)
      amount = transaction.originalAmount
    }
    return `${amount}${currency}`;
  };
  
  useEffect(() => {
    fetchAndSetTransactions();
  }, []);

  if (transactions == null || transactions.transactions == null || transactions.transactions[0] == null) {
    return (
      <Card className="p-4 h-full flex flex-col justify-start">
        <h1 className="text-2xl text-center font-thin mb-5">Fetching Transactions</h1>
        <div className={"w-full flex items-center justify-center"}>
          <Loading />
        </div>
      </Card>
    );
  }

  return (
    <div className="bg-gray-50 h-full overflow-scroll">
      <Card className="p-4 flex flex-col overflow-y-scroll">
        <h1 className="text-2xl text-center font-thin mb-2">Latest Transactions</h1>
        <hr className="bg-gray-100 w-full mb-4" />
        <div className="grid gap-2">
          {transactions.transactions[0].slice(0, 14).map((t) => {
            if (t == null){
              return <></>
            }
            const categorized = t.categoryName != null && t.categoryId != -1;

            return (
              <div key={t.id} className="grid grid-cols-3 items-center gap-2">
                <p className={`font-light col-span-1 truncate ${!categorized && "text-gray-400"}`}>
                  {categorized ? t.categoryName : "Pending"}
                </p>
                <p className="text-gray-400 font-thin col-span-1 truncate">{formatDate(t.purchaseDate)}</p>
                <p
                  className={`text-base col-span-1 rounded-md px-2 py-1 text-center w-20 ml-auto mr-auto font-thin ${getAmountBadgeColor(
                    t.transactionAmount
                  )}`}
                >
                  {getTransactionAmount(t)}
                </p>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
};

export default LatestTransactions;
