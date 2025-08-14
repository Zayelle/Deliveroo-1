import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { loginUser, clearError} from "../features/auth/authSlice";

export default function LoginPage() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { loading, error, token } = useSelector((state) => state.auth);
  const [credentials, setCredentials] = useState({ email: "", password: "" });

  const handleChange = (e) => {
    if (error) { 
       // optionally dispatch an action to clear the error
     dispatch(clearError());
    }
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Dispatch loginUser and wait for it to succeed or fail
      await dispatch(loginUser(credentials)).unwrap();
      // If successful, navigate immediately
      navigate("/");
    } catch (err) {
      // err is the rejected value from thunk (error message)
      // You could optionally handle error here if you want additional UI
      console.error("Login failed:", err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1>Login</h1>
      <input
        name="email"
        type="email"
        placeholder="Email"
        value={credentials.email}
        onChange={handleChange}
        required
        disabled={loading}
      />
      <input
        name="password"
        type="password"
        placeholder="Password"
        value={credentials.password}
        onChange={handleChange}
        required
        disabled={loading}
      />
      <button type="submit" disabled={loading}>
        {loading ? "Logging in..." : "Login"}
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}
