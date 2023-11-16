// SignupPage.jsx - A page component for registering a new user account in the Expenses Tracker app

import React from "react";

// SignupPage functional component
const SignupPage = () => {
  // JSX for SignupPage, includes form with fields for account registration
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-bgColor">
      <div className="mb-4 text-5xl text-main font-thin">
        Expenses Tracker
      </div>
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold">
            Register a new account
          </h2>
        </div>
        <form className="mt-8 space-y-6" action="#" method="POST">
          <div className="rounded-md shadow-sm -space-y-px">
            {/* Input fields for email, password, invite key, and credit card login credentials */}
            <input
              id="email-address"
              name="email"
              type="email"
              autoComplete="email"
              required
              className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-main focus:border-main focus:z-10 sm:text-sm"
              placeholder="Email address"
            />
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="new-password"
              required
              className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-main focus:border-main focus:z-10 sm:text-sm"
              placeholder="Password"
            />
            <input
              id="inviteKey"
              name="inviteKey"
              required
              className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-main focus:border-main focus:z-10 sm:text-sm"
              placeholder="Invite Key"
            />
            <input
              id="appLoginEmail"
              name="appLoginEmail"
              required
              className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-main focus:border-main focus:z-10 sm:text-sm"
              placeholder="Credit Card Login Email"
            />
            <input
              id="appLoginPassword"
              name="appLoginPassword"
              required
              className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-main focus:border-main focus:z-10 sm:text-sm"
              placeholder="Credit Card Login Password"
            />
          </div>
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
