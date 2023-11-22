import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import DashboardPage from "@/pages/DashboardPage/DashboardPage";
import TransactionsPage from "@/pages/TransactionsPage/TransactionsPage";
import useStore from "@/store/store";
import RequireAuth from "@/components/Auth/RequireAuth";
import SigninPage from "@/pages/SigninPage/SigninPage";
import SignupPage from "@/pages/SignupPage/SignupPage";
import SetupPage from "@/pages/SetupPage/SetupPage";
import PendingTransactions from "@/pages/PendingTransactions/PendingTransactions";

function App() {
  const reset = useStore((state) => state.reset);

  const AuthenticatedDashboardPage = RequireAuth(DashboardPage);
  const AuthenticatedTransactionsPage = RequireAuth(TransactionsPage);
  const AuthenticatedSetupPage = RequireAuth(SetupPage, false, false);
  const AuthenticatedPendingPage = RequireAuth(PendingTransactions, true, false);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<AuthenticatedDashboardPage />} />
        <Route path="/transactions" element={<AuthenticatedTransactionsPage />} />
        <Route
          path="/reset"
          element={
            <div>
              <button
                onClick={() => {
                  console.log("Reset");
                  reset();
                }}
              >
                Reset
              </button>
            </div>
          }
        />
        <Route path="/signin" element={<SigninPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/setup" element={<AuthenticatedSetupPage />} />
        <Route path="/pending-transactions" element={<AuthenticatedPendingPage />} />
      </Routes>
    </Router>
  );
}

export default App;
