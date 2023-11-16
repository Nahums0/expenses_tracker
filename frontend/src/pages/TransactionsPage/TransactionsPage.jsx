import Navbar from "@/components/NavigationBars/Navbar";
import TransactionsTable from "@/components/TransactionTable/Table";
import RecurringTransactionsTable from "@/components/RecurringTransactionsTable/Table"
import Tabs from '@/components/Tabs/Tabs';
import { useStore } from "@/store/store";
import React, { useState } from "react";


function TransactionsPage() {
  const { sidebarOpen } = useStore();
  const [tabIndex, setTabIndex] = useState(0);

  const tabs = [
    {
      name: "Transactions",
      childElements: <TransactionsTable />,
    },
    {
      name: "Recurring Transactions",
      childElements: <RecurringTransactionsTable />,
    }
  ];

  return (
    <>
      <div className="relative min-h-screen bg-bgColor">
        <Navbar />
        <div className={`${sidebarOpen? "sm:ml-60":"sm:ml-16"} min-h-screen`}>
        <Tabs tabs={tabs} tabIndex={tabIndex} setTabIndex={setTabIndex} />
        </div>
      </div>
    </>
  );
}

export default TransactionsPage;
