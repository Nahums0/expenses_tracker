import React, {useState} from "react";
import { useNavigate } from 'react-router-dom';
import useStore from "@/store/store";

const SignupPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [inviteKey, setInviteKey] = useState("");
  const [error, setError] = useState("");
  const { user, setUser } = useStore();

  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent default form submission behavior

    try {
      const response = await fetch("/api/users/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
          inviteKey,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.message || "An error occurred");
      } else {
        setError("");
        setUser(data.data.user);
        navigate("/");
      }
    } catch (error) {
      console.error(error)
      setError("Network error or unexpected problem occurred.");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-bgColor">
      <div className="mb-4 text-5xl text-main font-thin">Expenses Tracker</div>
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold">Register a new account</h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <input
              id="email-address"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-main focus:border-main focus:z-10 sm:text-sm"
              placeholder="Email address"
            />
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="new-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-main focus:border-main focus:z-10 sm:text-sm"
              placeholder="Password"
            />
            <input
              id="inviteKey"
              name="inviteKey"
              required
              value={inviteKey}
              onChange={(e) => setInviteKey(e.target.value)}
              className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-main focus:border-main focus:z-10 sm:text-sm"
              placeholder="Invite Key"
            />
          </div>
          {error && <div className="text-red-500 text-sm">{error}</div>}
          <div>
            <button
              type="submit"
              className="group text-white relative w-full flex justify-center py-2 px-4 border border-transparent text-2xl font-light rounded-md bg-main hover:opacity-80 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-main"
            >
              Register
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SignupPage;
