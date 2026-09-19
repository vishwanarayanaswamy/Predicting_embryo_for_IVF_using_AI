import React from "react";
import Register from "./components/Register";
import Login from "./components/Login"

import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import EmbryoAnalyzer from "./embrioAnalyser"
function App() {
  const authToken = localStorage.getItem("token");
console.log("token",authToken)
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/analyze" element={authToken ? <EmbryoAnalyzer/> : <Navigate to="/login" />} />
        <Route path="/"  element={authToken ? <EmbryoAnalyzer/> : <Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
