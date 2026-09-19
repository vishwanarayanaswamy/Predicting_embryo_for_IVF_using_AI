

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Register = () => {
    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        email: "",
        contact_number: "",
        address: "",
        username: "",
        password: "",
        id:Math.random()
    });

    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post("http://127.0.0.1:5000/register", formData);
            console.log(response)
            if (response.data.token) {
                localStorage.setItem("token", response.data.token);  // ✅ Store token
                alert("Registration successful! Redirecting to analysis...");
                navigate("/analyze");  // ✅ Auto-redirect
            } else {
                alert(response.data.error || "Registration failed!");
            }
        } catch (error) {
            console.error("Error during registration:", error);
            alert("Registration error! Please try again.");
        }
    };

    return (
        <div className="auth-container">
        <h2>Register</h2>
        <form onSubmit={handleSubmit}>
          <input type="text" name="first_name" placeholder="First Name" onChange={handleChange} required />
          <input type="text" name="last_name" placeholder="Last Name" onChange={handleChange} required />
          <input type="email" name="email" placeholder="Email" onChange={handleChange} required />
          <input type="text" name="contact_number" placeholder="Contact Number" onChange={handleChange} required />
          <input type="text" name="address" placeholder="Address" onChange={handleChange} required />
          <input type="text" name="username" placeholder="Username" onChange={handleChange} required />
          <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
          <button type="submit">Register</button>
        </form>
        <a href="/login" className="auth-link">Already have an account? Login</a>
      </div>
    );
};

export default Register;
