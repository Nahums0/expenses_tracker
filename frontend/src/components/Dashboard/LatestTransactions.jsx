import Loading from "@/components/Loading/Loading";
import Card from "./Card";
import useStore from "@/store/store";
import react, { useEffect } from "react";

const LatestTransactions = () => {
  const { transactions, fetchAndSetTransactions } = useStore();

  const formatDate = (date) => {
    if (!date) return "";
    return typeof date === "string" ? date.split("T")[0] : date.toISOString().split("T")[0];
  };

  useEffect(() => {
    fetchAndSetTransactions();
  }, []);

  if (transactions.transactions == null || transactions.transactions[0] == null) {
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
    <div className="bg-gray-50 h-5/6 overflow-scroll">
      <Card className="p-4 flex flex-col overflow-y-scroll">
        <h1 className="text-2xl text-center font-thin mb-2">Latest Transactions</h1>
        <hr className="bg-gray-100 w-full mb-4" />
        <div className="grid gap-2">
          {transactions.transactions[0].slice(0, 14).map((t) => {
            const categorized = t.categoryName != null && t.categoryId != -1;

            return (
              <div key={t.id} className="grid grid-cols-3 items-center gap-2">
                <p className={`font-light col-span-1 truncate ${!categorized && "text-gray-400"}`}>
                  {categorized ? t.categoryName : "Pending"}
                </p>
                <p className="text-gray-400 font-thin col-span-1 truncate">{formatDate(t.purchaseDate)}</p>
                <p
                  className={`font-light text-base col-span-1 ${
                    t.transactionAmount < 0 ? "text-green-600 bg-green-200" : "text-red-400 bg-red-100"
                  } rounded-md px-2 py-1 text-center w-min ml-auto mr-auto font-thin`}
                >
                  {Math.abs(t.transactionAmount).toFixed(2)}₪
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
