import React, { useState } from "react";

const TestCredentialStates = {
  PENDING_VERIFICATION: "Pending verification",
  WAITING_FOR_SERVER: "Waiting for server",
  INCORRECT: "Incorrect",
  CORRECT: "Correct",
};

const ProfileSetup = ({
  user, 
  fullName,
  currency,
  setFullName,
  setCurrency,
  creditCardCredentials,
  setSetupCreditCardCredentials,
  errorMessage,
}) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [id, setId] = useState("");
  const [credentialsState, setCredentialsState] = useState(
    creditCardCredentials != null
      ? TestCredentialStates.CORRECT
      : TestCredentialStates.PENDING_VERIFICATION
  );

  const testCredentials = async () => {
    setCredentialsState(TestCredentialStates.WAITING_FOR_SERVER);
    try {
      const accessToken = user.accessToken;
      const response = await fetch("/api/users/test-cc-credentials", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          username,
          password,
          id,
        }),
      });
      setCredentialsState(TestCredentialStates.WAITING_FOR_SERVER);

      if (!response.ok) {
        setCredentialsState(TestCredentialStates.INCORRECT);
        const errorData = await response.json();
        throw new Error(
          errorData.message || "Error occurred while testing credentials"
        );
      }

      const data = await response.json();

      setCredentialsState(TestCredentialStates.CORRECT);
      setSetupCreditCardCredentials({
        username,
        password,
        id,
      });
    } catch (error) {
      console.error("Error checking credentials:", error);
      setCredentialsState(TestCredentialStates.INCORRECT);
    }
  };

  const creditCardFormDisabled =
    credentialsState == TestCredentialStates.CORRECT ||
    credentialsState == TestCredentialStates.WAITING_FOR_SERVER;

  return (
    <div className="max-w-md mx-auto mt-10">
      <div className="mb-6">
        <legend className="block mb-2 text-xl font-medium text-gray-900">
          Profile
        </legend>
        <label
          htmlFor="fullName"
          className="block mb-2 text-sm font-medium text-gray-900"
        >
          Full Name
        </label>
        <input
          type="text"
          id="fullName"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
          placeholder="John Doe"
          required
        />
      </div>

      <div className="mb-6">
        <label
          htmlFor="currency"
          className="block mb-2 text-sm font-medium text-gray-900"
        >
          Choose Currency
        </label>
        <select
          id="currency"
          value={currency}
          onChange={(e) => setCurrency(e.target.value)}
          className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
        >
          <option value="₪">₪ - Shekel</option>
          <option value="$">$ - Dollar</option>
        </select>
      </div>

      <fieldset className="mb-6">
        <legend className="block mb-2 text-xl font-medium text-gray-900">
          Credit Card Provider's Credentials
        </legend>
        <div className="mb-4">
          <label
            htmlFor="email"
            className="block mb-2 text-sm font-medium text-gray-900"
          >
            Email
          </label>
          <input
            type="email"
            id="ccProviderEmail"
            name="ccProviderEmail"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="bg-gray-50 border border-gray-300 disabled:text-gray-400 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
            placeholder="email@example.com"
            disabled={creditCardFormDisabled}
            required
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="password"
            className="block mb-2 text-sm font-medium text-gray-900"
          >
            Password
          </label>
          <input
            type="password"
            id="ccProviderPassword"
            name="ccProviderPassword"
            placeholder="**********"
            disabled={creditCardFormDisabled}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="new-password"
            className="bg-gray-50 border border-gray-300 disabled:text-gray-400 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
            required
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="cc-id"
            className="block mb-2 text-sm font-medium text-gray-900"
          >
            Identity Number
          </label>
          <input
            type="text"
            id="ccId"
            name="ccId"
            value={id}
            onChange={(e) => setId(e.target.value)}
            className="bg-gray-50 border border-gray-300 disabled:text-gray-400 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
            placeholder="000000000"
            disabled={creditCardFormDisabled}
            required
          />
        </div>
        <div className="flex flex-row justify-between">
          <button
            type="button"
            onClick={testCredentials}
            className={`text-white enabled:bg-blue-700 bg-blue-400 ${
              credentialsState == TestCredentialStates.CORRECT && "bg-green-600"
            } enabled:hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center`}
            disabled={creditCardFormDisabled}
          >
            {credentialsState == TestCredentialStates.CORRECT
              ? "Authenticated successfully"
              : "Test Credentials"}
          </button>
          {credentialsState == TestCredentialStates.WAITING_FOR_SERVER && (
            <div className="flex items-center">
              <svg
                className="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-500"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 0116 0H4z"
                ></path>
              </svg>
              <span className="text-sm font-medium text-gray-500">
                Waiting for server response...
              </span>
            </div>
          )}
          {credentialsState == TestCredentialStates.INCORRECT && (
            <div
              className="p-2 bg-red-800 items-center text-red-100 leading-none lg:rounded-full flex lg:inline-flex"
              role="alert"
            >
              <span className="flex rounded-full bg-red-500 uppercase px-2 py-1 text-xs font-bold mr-3">
                Error
              </span>
              <span className="font-semibold mr-2 text-left flex-auto">
                Incorrect Credentials
              </span>
            </div>
          )}
        </div>
        {errorMessage && (
          <div className="flex items-center justify-center mt-5">
            <div
              className="p-2 bg-red-800 items-center text-red-100 leading-none lg:rounded-full flex lg:inline-flex"
              role="alert"
            >
              <span className="flex rounded-full bg-red-500 uppercase px-2 py-1 text-xs font-bold mr-3">
                Error
              </span>
              <span className="font-semibold mr-2 text-left flex-auto">
                {errorMessage}
              </span>
            </div>
          </div>
        )}
      </fieldset>
    </div>
  );
};

export default ProfileSetup;
