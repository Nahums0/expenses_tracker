import React, { useState, useRef, useEffect } from "react";
import Card from "@/components/Dashboard/Card";

const CategoryCard = ({
  category,
  index,
  budget,
  percentage,
  handleBudgetSliderChange,
  handleCategoryNameChange,
  handleCategoryDelete,
}) => {
  // State to keep track of editing mode, category name, and menu visibility
  const [isEditing, setIsEditing] = useState(false);
  const [editedCategoryName, setEditedCategoryName] = useState(
    category.categoryName
  );
  const [menuVisible, setMenuVisible] = useState(false);
  const menuRef = useRef(null);

  // Toggle the visibility of the menu
  const toggleMenu = () => {
    setMenuVisible(!menuVisible);
  };

  const handleEdit = () => {
    setMenuVisible(false);
    setIsEditing(true);
  };

  const handleDelete = () => {
    setMenuVisible(false);
    handleCategoryDelete(index);
  };

  // Toggle editing mode and handle category name update
  const toggleEdit = () => {
    if (isEditing) {
      handleCategoryNameChange(editedCategoryName, index);
    }
    setIsEditing(!isEditing);
    // Reset edited name to current category name when exiting edit mode
    if (!isEditing) setEditedCategoryName(category.categoryName);
  };

  // Update category name as user types
  const handleCategoryNameEdit = (e) => {
    setEditedCategoryName(e.target.value);
  };

  // Prevent form submission on Enter key press
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      toggleEdit();
    }
  };

  // Click outside handler to close menu if open
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setMenuVisible(false);
      }
    };

    // Bind the event listener
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      // Unbind the event listener on clean up
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [menuRef]);

  return (
    <Card
      className={`w-full p-5 relative ${budget == 0 && "opacity-30"}`}
      key={category.id}
    >
      <button
        onClick={toggleMenu}
        className="absolute top-0 right-0 m-3"
        aria-label="Options"
      >
        &#x22EE;
      </button>

      {menuVisible && (
        <div
          ref={menuRef}
          className="absolute top-0 right-0 mt-12 mr-3 bg-white shadow-lg rounded z-10 p-2"
        >
          {/* Implement menu items here */}
          <ul className="text-gray-700">
            <li
              className="hover:bg-gray-100 p-2 cursor-pointer"
              onClick={handleEdit}
            >
              Edit
            </li>
            <li
              className="hover:bg-gray-100 p-2 cursor-pointer"
              onClick={handleDelete}
            >
              Delete
            </li>
            {/* Add more menu items here as needed */}
          </ul>
        </div>
      )}
      <div className="w-full overflow-clip">
        {isEditing ? (
          <input
            type="text"
            value={editedCategoryName}
            onChange={handleCategoryNameEdit}
            onBlur={toggleEdit}
            onKeyPress={handleKeyPress}
            className="text-xl text-main font-medium tracking-widest w-full"
            autoFocus
          />
        ) : (
          <h1
            className="text-xl text-main font-medium tracking-widest truncate"
            onDoubleClick={toggleEdit}
          >
            {category.categoryName}
          </h1>
        )}
      </div>
      <h1 className="font-thin">
        <p className="inline-block mr-2">Budget:</p>
        {Math.round(budget)} / {Math.round(percentage)}%
      </h1>
      <div>
        <input
          id="default-range"
          type="range"
          min={0}
          max={100}
          value={percentage}
          onChange={(e) => handleBudgetSliderChange(index, e)}
          className="w-full h-2 bg-navBg rounded-lg appearance-none cursor-pointer"
        />
      </div>
    </Card>
  );
};

export default CategoryCard;
