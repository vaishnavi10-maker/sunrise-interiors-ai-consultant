import { useState } from "react";

function App() {
  const [phoneNumber, setPhoneNumber] = useState("");
  const [status, setStatus] = useState("");

  const handleCall = async () => {
  if (!phoneNumber) {
    setStatus("Please enter your phone number");
    return;
  }

  setStatus("Sending call request...");

  try {
    const response = await fetch(
      "http://localhost:8000/api/calls",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          phone_number: phoneNumber,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Call failed");
    }

    setStatus(data.message);
  } catch (error) {
    setStatus(error.message);
  }
};

  return (
    <div className="app">
      <div className="card">
        <p className="eyebrow">
          SUNRISE INTERIORS
        </p>

        <h1>
          Design your dream home
        </h1>

        <p className="description">
          Get a quick consultation with our interior design team.
        </p>

        <label>
          Your phone number
        </label>

        <input
          type="tel"
          placeholder="+91 9876543210"
          value={phoneNumber}
          onChange={(event) => {
            setPhoneNumber(event.target.value);
          }}
        />

        <button onClick={handleCall}>
          Receive a Call
        </button>

        {status && (
          <p className="status">
            {status}
          </p>
        )}
      </div>
    </div>
  );
}

export default App;