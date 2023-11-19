import { Navigate, useLocation } from "react-router-dom";
import useStore from "@/store/store";

function RequireAuth(Component, redirectSetup=true, redirectPendingTransactions=true) {
  return (props) => {
    const location = useLocation();
    var {user} = useStore()

    const isAuthenticated = user != null

    if (!isAuthenticated) {
      return <Navigate to="/signin" state={{ from: location }} replace />;
    }

    const initialSetupDone = user.initialSetupDone

    if (redirectSetup && initialSetupDone != true){
      return <Navigate to="/setup" state={{ from: location }} replace />;
    }

    const firstTransactionFetched = user.lastTransactionsScanDate
    if (redirectPendingTransactions && firstTransactionFetched == null){
      return <Navigate to="/pending-transactions" state={{ from: location }} replace />;
    }

    // If the user is authenticated, render the passed component
    return <Component {...props} />;
  };
}

export default RequireAuth;
