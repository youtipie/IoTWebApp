import { createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

export const authInstance = axios.create({
  baseURL: "http://127.0.0.1:5000",
});

export const setToken = (token) => {
  authInstance.defaults.headers.common["X-CSRF-TOKEN"] = token;
};

export const clearToken = () => {
  delete authInstance.defaults.headers.common["X-CSRF-TOKEN"];
};

// Register user
export const register = createAsyncThunk(
  "auth/register",
  async (userData, thunkApi) => {
    try {
      const { data } = await authInstance.post("/auth/register", userData);
      return data;
    } catch (error) {
      return thunkApi.rejectWithValue(error.response?.data?.message || "Error");
    }
  }
);

// Login user
export const login = createAsyncThunk(
  "auth/login",
  async (userData, thunkApi) => {
    try {
      const response = await authInstance.post("/auth/login", userData);
      const csrfToken = response.headers["csrf_access_token"];
      setToken(csrfToken);
      return { message: response.data.message, csrfToken };
    } catch (error) {
      return thunkApi.rejectWithValue(error.response?.data?.message || "Error");
    }
  }
);

// Logout user
export const logout = createAsyncThunk("auth/logout", async (_, thunkApi) => {
  try {
    const { data } = await authInstance.post("/auth/logout");
    clearToken();
    return data;
  } catch (error) {
    return thunkApi.rejectWithValue(error.response?.data?.message || "Error");
  }
});
