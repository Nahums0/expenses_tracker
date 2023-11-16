import "./Navbar.css";
import { sideBarItems } from "./sidebar-config";
import React, { useState } from "react";
import BottomNavbar from "./BottomNavbar/BottomNavbar";
import SideNavbar from "./SideNavbar/SideNavbar";
import { useStore } from "@/store/store";

const NavigationBar = () => {
  const { sidebarOpen, toggleSidebar } = useStore();
  const [isHovered, setIsHovered] = useState(false);

  return (
    <>
      <div className="sm:hidden">
        <BottomNavbar sideBarItems={sideBarItems} />
      </div>

      <div className="hidden sm:block">
        {sidebarOpen && (
          <SideNavbar sideBarItems={sideBarItems} className={`${isHovered && "opacity-90 transition-opacity"}`} />
        )}
      </div>

      <div
        onClick={() => toggleSidebar(!sidebarOpen)}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        className={`fixed text-xl ${
          sidebarOpen ? "left-56" : "left-7"
        } top-1/2 -translate-y-1/2 z-10 rounded h-6 w-1 bg-black cursor-pointer hidden sm:block`}
      ></div>
    </>
  );
};

export default NavigationBar;
