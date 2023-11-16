import React from "react";

const Card = ({ children, className, onClick=null }) => {
  return (
    <div onClick={onClick} className={`bg-white rounded-md shadow-md ${className}`}>
      {children}
    </div>
  );
};

export default Card;
