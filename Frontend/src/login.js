import React, { useState } from "react";

function Login({ setIsLoggedIn }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      });

      const data = await response.json();

      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        setIsLoggedIn(true);
      } else {
        alert("Login failed ❌");
      }
    } catch (error) {
      alert("Server error ❌");
    }
  };

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#121212",
        color: "white",
      }}
    >
      <div
        style={{
          backgroundColor: "#1e1e1e",
          padding: "30px",
          borderRadius: "10px",
          width: "300px",
          textAlign: "center",
        }}
      >
        <h2>🍕 QuickBite Login</h2>

        <input
          type="text"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
          style={{ width: "100%", padding: "10px", margin: "10px 0" }}
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
          style={{ width: "100%", padding: "10px", margin: "10px 0" }}
        />

        <button
          onClick={handleLogin}
          style={{
            width: "100%",
            padding: "10px",
            backgroundColor: "#ff5722",
            border: "none",
            color: "white",
            cursor: "pointer",
          }}
        >
          Login
        </button>
      </div>
    </div>
  );
}

export default Login;