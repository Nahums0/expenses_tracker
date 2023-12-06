import React from "react";
import Card from "@/components/Dashboard/Card";
import { useNavigate } from "react-router-dom";

const CategoryCard = ({ name, amountSpent, budget, className, isPlaceholder = false, categoryId }) => {
  const percentage = Math.round((amountSpent / budget) * 100);
  const navigate = useNavigate();

  const backgroundStyle = {
    backgroundImage: `linear-gradient(to top, #86B1B4 ${percentage}%, transparent ${percentage}%, transparent 100%)`,
  };

  const hoverProperties = "hover:opacity-90 hover:scale-105 transition-transform cursor-pointer";
  
  const handleCardClick = () => {
    const filter = {
      category: [categoryId], // Add the categoryId to the category array
    };

    const filterString = encodeURIComponent(JSON.stringify(filter));
    navigate(`/transactions?filter=${filterString}`);
  };

  return (
    <Card
      onClick={handleCardClick}
      className={`h-56 w-full flex flex-col justify-around ${!isPlaceholder && hoverProperties} ${className}`}
    >
      <div style={backgroundStyle} className="h-full p-4">
        <div>
          <p className="text-center text-3xl font-thin text-gray-700">{isPlaceholder ? "Loading..." : name}</p>
          <p className="text-center font-thin">{!isPlaceholder && amountSpent + "/" + budget}</p>
        </div>
        <h2 className="text-3xl font-thin text-center">{!isPlaceholder && percentage + "%"}</h2>
      </div>
    </Card>
  );
};

export default CategoryCard;
