import Navbar from "@/components/NavigationBars/Navbar"
import Dashboard from "@/components/Dashboard/Dashboard"
import { useStore } from "@/store/store";

function DashboardPage() {
  const { sidebarOpen } = useStore();

  return (
    <>
      <div className="relative min-h-screen bg-bgColor">
        <Navbar />
        <div className={`${sidebarOpen? "sm:ml-52":"sm:ml-5"} mr-auto min-h-screen`}>
          <Dashboard/>
        </div>
      </div>
    </>
  );
}

export default DashboardPage;
