import React from "react";
import Card from "./Card";

const MonthlyMetricsCard = ({title, body, className}) => {
  return (
    <Card className={`w-full lg:w-1/3 h-32 flex flex-col justify-around p-4 ${className}`}>
      <h2 className="text-2xl ">{title}</h2>
      <h2 className="text-xl font-thin text-center">{body}</h2>
    </Card>
  );
};

export default MonthlyMetricsCard;
