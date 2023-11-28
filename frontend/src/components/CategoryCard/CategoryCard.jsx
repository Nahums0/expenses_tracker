import React from "react";
import Card from "@/components/Dashboard/Card";

const CategoryCard = ({
  name,
  amountSpent,
  budget,
  className,
  isPlaceholder = false,
}) => {
  const percentage =  Math.round((amountSpent / budget) * 100);

  const backgroundStyle = {
    backgroundImage: `linear-gradient(to top, #86B1B4 ${percentage}%, transparent ${percentage}%, transparent 100%)`,
  };

  const hoverProperties =
    "hover:opacity-90 hover:scale-105 transition-transform cursor-pointer";

  return (
    <Card
      className={`h-56 w-full flex flex-col justify-around ${
        !isPlaceholder && hoverProperties
      } ${className}`}
    >
      <div style={backgroundStyle} className="h-full p-4">
        <div>
          <p className="text-center text-3xl font-thin text-gray-700">
            {isPlaceholder ? "Loading..." : name}
          </p>
          <p className="text-center font-thin">
              {!isPlaceholder && amountSpent + "/" + budget}
          </p>
        </div>
        <h2 className="text-3xl font-thin text-center">
          {!isPlaceholder && percentage + "%"}
        </h2>
      </div>
    </Card>
  );
};

export default CategoryCard;
