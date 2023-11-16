import React, { useState } from "react";
import "./SideNavbar.css";
import SideNavbarItem from "./SideNavbarItem";
import { useLocation } from "react-router-dom";
import useStore from "@/store/store";
import InitialsAvatar from "@/components/InitialsAvatar/InitialsAvatar";

const SideNavbar = ({ sideBarItems, className }) => {
  const currentUrl = useLocation().pathname;
  const { user, sidebarOpen } = useStore();

  return (
    <>
      <aside
        id="default-sidebar"
        className={`fixed top-0 left-0 z-56 h-screen transition-transform ${sidebarOpen ? "w-52" : "w-16"} ${className}`}
        aria-label="Sidebar"
      >
        <div className="relative flex flex-col justify-between h-full px-3 py-4 overflow-y-auto bg-gray-50 dark:bg-main overflow-visible z-9">
          <ul className="space-y-2 font-medium">
            <div className="h-32 w-full  grid place-items-center mt-5 mb-10">
              <InitialsAvatar username={user.fullName} className="w-32 h-32 text-6xl" />
            </div>

            {sideBarItems.map(
              (item, idx) =>
                item.isPinned != true && (
                  <SideNavbarItem selected={currentUrl == item.url} key={idx} sidebarOpen={sidebarOpen} {...item} />
                )
            )}
          </ul>

          <ul className="space-y-2 font-medium mt-4 border-t border-gray-500 pt-4">
            {sideBarItems.map(
              (item, idx) =>
                item.isPinned == true && (
                  <SideNavbarItem
                    key={`pinned-${idx}`}
                    {...item}
                    selected={currentUrl == item.url}
                  />
                )
            )}
          </ul>
        </div>
      </aside>
    </>
  );
};

export default SideNavbar;
