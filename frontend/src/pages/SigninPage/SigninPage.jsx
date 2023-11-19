import React, { useState } from "react";
import useStore from "@/store/store";
import { useNavigate } from 'react-router-dom';

const SigninPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const { user, setUser } = useStore();
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    const credentials = { email, password };

    try {
      const response = await fetch("/api/users/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(credentials),
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
      setError("Network error or unexpected problem occurred.");
      console.error(error)
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-bgColor">
      <div className="mb-4 text-5xl text-main font-thin text-dashboard-text">
        Expenses Tracker
      </div>
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-dashboard-text">
            Sign in to your account
          </h2>
        </div>
        <form className="mt-8" onSubmit={handleSubmit}>
          <input
            id="email-address"
            name="email"
            type="email"
            autoComplete="email"
            required
            className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-main focus:border-main focus:z-10 sm:text-sm"
            placeholder="Email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
            className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-main focus:border-main focus:z-10 sm:text-sm"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <div>
            <button
              type="submit"
              className="group text-white relative w-full flex justify-center py-2 px-4 mt-8 border border-transparent text-2xl font-light rounded-md text-dashboard-text bg-main hover:opacity-80 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-main"
            >
              Sign in
            </button>
          </div>
          {error && <div className="text-red-500 text-sm">{error}</div>}
        </form>
        <div className="text-center">
          <p className="text-dashboard-text text-md">
            Don't have an account?
            <a
              href="/signup"
              className="font-medium text-main hover:text-dashboard-text ml-1"
            >
              Sign Up
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SigninPage;
