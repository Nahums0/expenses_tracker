import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const SideNavbarItem = ({ icon, label, url, selected }) => {
  return (
    <li>
      <a
        href={url}
        className={`flex items-center p-2  text-gray-100 rounded-lg font-extralight text-xl group ${
          selected ? "bg-navBg" : "dark:hover:opacity-70"
        }
        `}
      >
        <FontAwesomeIcon className="justify-center m-auto" icon={icon} />
        <span className="flex-1 ml-3 whitespace-nowrap">{label}</span>
      </a>
    </li>
  );
};

export default SideNavbarItem;
