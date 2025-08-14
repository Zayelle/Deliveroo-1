import axios from "axios";

const API_URL = "http://localhost:5000/auth"; // Backend URL

// Attach token automatically to every request
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Login
export const loginUser = async (credentials) => {
  const res = await axios.post(`${API_URL}/login`, credentials);
  return res.data; // Expect { token, user }
};

// Register
export const registerUser = async (data) => {
  const res = await axios.post(`${API_URL}/register`, data);
  return res.data; // Expect { token, user }
};

// Get current user
export const getCurrentUser = async (token) => {
  const res = await axios.get(`${API_URL}/profile`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
};

