import React, { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSort } from "@fortawesome/free-solid-svg-icons";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import useStore from "@/store/store";

const MenuButton = ({ icon, text, onClick, border, className }) => (
  <MenuItem border={border} className={`hover:bg-gray-100 items-center cursor-pointer ${className}`}>
    {icon && <FontAwesomeIcon icon={icon} />}
    <button className="flex-grow px-4 py-2" onClick={onClick}>
      {text}
    </button>
  </MenuItem>
);

const MenuItem = ({ children, border, className }) => (
  <li className={`flex flex-row pl-4 ${border ? "border-b-1 mb-3" : ""} ${className}`}>{children}</li>
);

const TextFilter = ({ inputValue, setInputValue, applyFilter }) => (
  <>
    <MenuItem className="pl-2 pr-4">
      <input
        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg outline-none block w-full p-2.5"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        placeholder="Text Search"
      />
    </MenuItem>
    <MenuButton onClick={applyFilter} text="Apply filter" className="mt-2 border-t-1" />
  </>
);

const NumberFilter = ({ numberRange, handleNumberChange, applyFilter }) => (
  <>
    <MenuItem>
      <input
        type="number"
        placeholder="Min"
        value={numberRange.min}
        onChange={(e) => handleNumberChange(e, "min")}
        className="border-1 border-b-0 p-2 rounded-sm outline-none"
      />
    </MenuItem>
    <MenuItem className="border-t-1">
      <input
        type="number"
        placeholder="Max"
        value={numberRange.max}
        onChange={(e) => handleNumberChange(e, "max")}
        className="border-1 border-t-0 p-2 rounded-sm outline-none"
      />
    </MenuItem>
    <MenuButton onClick={applyFilter} text="Apply filter" className="mt-2 border-t-1" />
  </>
);

const DateFilter = ({ dateRange, setDateRange, applyFilter }) => (
  <>
    <MenuItem>
      <DatePicker
        selected={dateRange.start ? new Date(dateRange.start) : null}
        onChange={(date) => setDateRange({ ...dateRange, start: date ? date.toISOString().split("T")[0] : null })}
        className="border-1 border-b-0 p-2 rounded-sm outline-none"
        placeholderText="Start Date"
      />
    </MenuItem>
    <MenuItem className="border-t-1">
      <DatePicker
        selected={dateRange.end ? new Date(dateRange.end) : null}
        onChange={(date) => setDateRange({ ...dateRange, end: date ? date.toISOString().split("T")[0] : null })}
        className="border-1 border-t-0 p-2 rounded-sm outline-none"
        placeholderText="End Date"
      />
    </MenuItem>
    <MenuButton onClick={applyFilter} text="Apply filter" className="mt-2 border-t-1" />
  </>
);

const SelectFilter = ({ options, selectedOptions, handleSelectionChange, applyFilter }) => (
  <>
    {options.map((option, index) => (
      <MenuItem key={index} className="items-center">
        <input
          type="checkbox"
          checked={selectedOptions.includes(option.id)}
          onChange={() => handleSelectionChange(option.id)}
          className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
        />
        <label className="ms-2 text-sm font-medium text-gray-900">{option.name}</label>
      </MenuItem>
    ))}
    <MenuButton onClick={applyFilter} text="Apply filter" className="mt-2 border-t-1" />
  </>
);

const BooleanFilter = ({ booleanValue, setBooleanValue, options, applyFilter }) => (
  <>
    {options.map((option, index) => (
      <MenuItem key={index} className="items-center gap-2">
        <input
          type="radio"
          name="booleanFilter"
          value={option.value}
          checked={booleanValue === option.value}
          onChange={() => setBooleanValue(option.value)}
          className="w-4 h-4 border-gray-300 outline-none"
        />
        {option.name}
      </MenuItem>
    ))}
    <MenuButton onClick={applyFilter} text="Apply filter" className="mt-2 border-t-1" />
  </>
);

const HeaderMenu = ({
  xPos,
  yPos,
  menuWidth,
  closeMenu,
  menuType,
  columnData,
  setFilters,
  setSortConfig,
  initialFilters,
}) => {
  const { categories } = useStore();
  const [inputValue, setInputValue] = useState("");
  const [numberRange, setNumberRange] = useState({ min: "", max: "" });
  const [dateRange, setDateRange] = useState({ start: null, end: null });
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [booleanValue, setBooleanValue] = useState("");
  const [menuData, setMenuData] = useState([]);

  useEffect(() => {
    switch (columnData.key) {
      case "purchaseDate":
        setDateRange(initialFilters.purchaseDate || { start: null, end: null });
        break;
      case "transactionAmount":
        setNumberRange({
          min: initialFilters.transactionAmount?.min || "",
          max: initialFilters.transactionAmount?.max || "",
        });
        break;
      case "category":
        setSelectedOptions(initialFilters.category || []);
        setMenuData(categories.map((c) => ({ name: c.categoryName, id: c.id })));
        break;
      case "store":
        setInputValue(initialFilters.store || "");
        break;
      case "status":
        setBooleanValue(initialFilters.status ?? "");
        setMenuData([
          { value: true, name: "Pre-Authorized" },
          { value: false, name: "Authorized" },
        ]);
        break;
      default:
        // Reset state for unrecognized column keys
        setInputValue("");
        setNumberRange({ min: "", max: "" });
        setDateRange({ start: null, end: null });
        setSelectedOptions([]);
        setBooleanValue("");
        setMenuData([]);
    }
  }, []);

  const handleSort = (direction) => {
    const field = columnData.key;
    setSortConfig({
      field,
      direction: direction,
    });
  };

  const handleFilters = () => {
    let newFilters = { ...initialFilters };
    switch (menuType) {
      case "text":
        newFilters[columnData.key] = inputValue;
        break;
      case "number":
        newFilters[columnData.key] = { min: numberRange?.min || null, max: numberRange?.max || null };
        break;
      case "date":
        newFilters[columnData.key] = dateRange;
        break;
      case "select":
        newFilters[columnData.key] = selectedOptions;
        break;
      case "boolean":
        newFilters[columnData.key] = booleanValue;
        break;
      default:
        break;
    }
    setFilters(newFilters);
  };

  const handleSelectionChange = (selectedId) => {
    if (selectedOptions.includes(selectedId)) {
      setSelectedOptions(selectedOptions.filter((id) => id !== selectedId));
    } else {
      setSelectedOptions([...selectedOptions, selectedId]);
    }
  };

  const handleNumberChange = (e, type) => {
    setNumberRange({ ...numberRange, [type]: e.target.value });
  };

  const renderFilter = () => {
    switch (menuType) {
      case "text":
        return <TextFilter inputValue={inputValue} setInputValue={setInputValue} applyFilter={handleFilters} />;
      case "number":
        return (
          <NumberFilter
            numberRange={numberRange}
            handleNumberChange={handleNumberChange}
            applyFilter={handleFilters}
          />
        );
      case "date":
        return <DateFilter dateRange={dateRange} setDateRange={setDateRange} applyFilter={handleFilters} />;
      case "select":
        return (
          <SelectFilter
            options={menuData}
            selectedOptions={selectedOptions}
            handleSelectionChange={handleSelectionChange}
            applyFilter={handleFilters}
          />
        );
      case "boolean":
        return (
          <BooleanFilter
            booleanValue={booleanValue}
            setBooleanValue={setBooleanValue}
            options={menuData}
            applyFilter={handleFilters}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50 bg-opacity-30" onClick={closeMenu}>
      <ul
        onClick={(e) => e.stopPropagation()}
        className="bg-white rounded-md shadow-md fixed flex flex-col pt-2"
        style={{ left: `${xPos}px`, top: `${yPos}px`, width: menuWidth }}
      >
        {columnData.sortable && (
          <>
            <MenuButton onClick={() => handleSort("asc")} icon={faSort} text="Sort column ascending" />
            <MenuButton onClick={() => handleSort("desc")} icon={faSort} text="Sort column descending" border />
          </>
        )}

        {renderFilter()}
      </ul>
    </div>
  );
};

export default HeaderMenu;
