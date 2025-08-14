import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { logout } from "../features/auth/authSlice";

export default function Dashboard() {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
  };

  return (
    <div style={{ padding: "1rem" }}>
      <h1>Dashboard</h1>
      {user ? (
        <>
          <p>Welcome, <strong>{user.name}</strong>!</p>
          <p>Email: {user.email}</p>
        </>
      ) : (
        <p>Loading profile...</p>
      )}
      <button onClick={handleLogout} style={{ marginTop: "1rem" }}>
        Logout
      </button>
    </div>
  );
}

