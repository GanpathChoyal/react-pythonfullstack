import React from "react";
import { NavLink } from "react-router-dom";

function Navbar() {
  const linkStyle = ({ isActive }) => ({
    margin: "0 10px",
    textDecoration: "none",
    padding: "6px 12px",
    borderRadius: "6px",
    color: isActive ? "white" : "#333",
    backgroundColor: isActive ? "#007bff" : "transparent",
  });

  return (
    <nav style={{ padding: "10px", borderBottom: "1px solid #ddd" }}>
      <NavLink to="/" style={linkStyle}>Home</NavLink>
      <NavLink to="/login" style={linkStyle}>Login</NavLink>
      <NavLink to="/register" style={linkStyle}>Register</NavLink>
      <NavLink to="/logout" style={linkStyle}>Logout</NavLink>
    </nav>
  );
}

export default Navbar;
