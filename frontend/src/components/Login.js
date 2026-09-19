import { useState } from "react";
import axios from "axios";
import "./style.css";
import { useNavigate } from "react-router-dom";


const Login = ({ setAuthToken }) => {
  
  const [credentials, setCredentials] = useState({ username: "", password: "" });

  const handleChange = (e) => setCredentials({ ...credentials, [e.target.name]: e.target.value });
    const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/login", credentials);
      localStorage.setItem("token", response.data.token);
     
      navigate("/analyze");  // ✅ Auto-redirect

    } catch (error) {
      console.error("Login error:", error);
      alert("Invalid credentials");
    }
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="username" placeholder="Username" onChange={handleChange} required />
        <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
        <button type="submit">Login</button>
      </form>
      <a href="/register" className="auth-link">Don't have an account? Register</a>
    </div>
  );
};

export default Login;
