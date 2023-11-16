import { faTachometerAlt, faExchangeAlt, faTags, faUserCog } from '@fortawesome/free-solid-svg-icons';
export const sideBarItems = [
  {
    icon: faTachometerAlt,
    label: "Dashboard",
    url: "/"
  },
  {
    icon: faExchangeAlt,
    label: "Transactions",
    url: "/transactions"
  },
  {
    icon: faTags,
    label: "Categories",
    url: "/categories"
  },
  {
    icon: faUserCog,
    label: "User Settings",
    badge: "Pro",
    isPinned: true,
    url: "/user-settings"
  },
];
