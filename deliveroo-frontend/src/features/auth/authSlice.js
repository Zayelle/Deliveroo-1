import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

// ==================
// API Base URL (auto switch for prod/dev)
// ==================
const API_URL =
  process.env.NODE_ENV === "production"
    ? "https://your-production-backend.com/auth"
    : "http://localhost:5000/auth";

// ==================
// Helpers
// ==================
const saveAuthData = ({ token, user }) => {
  localStorage.setItem("token", token);
  localStorage.setItem("user", JSON.stringify(user));
};

const getToken = () => localStorage.getItem("token");

// Safe localStorage parser with silent cleanup
const getStoredUser = () => {
  try {
    const rawUser = localStorage.getItem("user");
    return rawUser ? JSON.parse(rawUser) : null;
  } catch {
    localStorage.removeItem("user");
    return null;
  }
};

// Redirect helper
const redirectToLogin = () => {
  const currentPath = window.location.pathname + window.location.search;
  const redirectUrl = `/login?redirect=${encodeURIComponent(currentPath)}`;
  window.location.href = redirectUrl;
};

// ==================
// Async Thunks
// ==================

// LOGIN
export const loginUser = createAsyncThunk(
  "auth/loginUser",
  async ({ email, password }, { rejectWithValue }) => {
    try {
      const res = await axios.post(`${API_URL}/login`, { email, password });
      saveAuthData(res.data);

      // Redirect after login if ?redirect= was provided
      const params = new URLSearchParams(window.location.search);
      const redirectPath = params.get("redirect");
      if (redirectPath) {
        window.location.href = redirectPath;
      } else {
        window.location.href = "/";
      }

      return res.data; // { token, user }
    } catch (err) {
      return rejectWithValue(err.response?.data?.message || "Login failed");
    }
  }
);

// REGISTER
export const registerUser = createAsyncThunk(
  "auth/registerUser",
  async ({ name, email, password }, { rejectWithValue }) => {
    try {
      const res = await axios.post(`${API_URL}/register`, { name, email, password });
      saveAuthData(res.data);

      // Same redirect logic as login
      const params = new URLSearchParams(window.location.search);
      const redirectPath = params.get("redirect");
      if (redirectPath) {
        window.location.href = redirectPath;
      } else {
        window.location.href = "/";
      }

      return res.data; // { token, user }
    } catch (err) {
      return rejectWithValue(err.response?.data?.message || "Registration failed");
    }
  }
);

// GET PROFILE
export const fetchProfile = createAsyncThunk(
  "auth/fetchProfile",
  async (_, { rejectWithValue }) => {
    try {
      const token = getToken();
      if (!token) return rejectWithValue("No token found");

      const res = await axios.get(`${API_URL}/profile`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      return { user: res.data, token };
    } catch (err) {
      const status = err.response?.status;

      // Auto logout & redirect on invalid/expired token
      if (status === 401 || status === 422) {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        redirectToLogin();
      }

      return rejectWithValue(err.response?.data?.message || "Failed to load profile");
    }
  }
);

// ==================
// Initial State
// ==================
const initialState = {
  user: getStoredUser(),
  token: getToken() || null,
  loading: false,
  error: null,
};

// ==================
// Slice
// ==================
const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    logout(state) {
      state.user = null;
      state.token = null;
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      redirectToLogin();
    },
    clearError(state) {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    const setPending = (state) => {
      state.loading = true;
      state.error = null;
    };
    const setFulfilled = (state, action) => {
      state.loading = false;
      state.user = action.payload.user;
      state.token = action.payload.token;
    };
    const setRejected = (state, action) => {
      state.loading = false;
      state.error = action.payload;
    };

    builder
      // LOGIN
      .addCase(loginUser.pending, setPending)
      .addCase(loginUser.fulfilled, setFulfilled)
      .addCase(loginUser.rejected, setRejected)

      // REGISTER
      .addCase(registerUser.pending, setPending)
      .addCase(registerUser.fulfilled, setFulfilled)
      .addCase(registerUser.rejected, setRejected)

      // FETCH PROFILE
      .addCase(fetchProfile.pending, setPending)
      .addCase(fetchProfile.fulfilled, setFulfilled)
      .addCase(fetchProfile.rejected, setRejected);
  },
});

// ==================
// Exports
// ==================
export const { logout, clearError } = authSlice.actions;
export default authSlice.reducer;
