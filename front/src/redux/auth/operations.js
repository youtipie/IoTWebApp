import { createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

export const authInstance = axios.create({
  baseURL: "http://127.0.0.1:5000/auth",
});

export const setToken = (token) => {
  authInstance.defaults.headers.common.Authorization = `Bearer ${token}`;
};

export const clearToken = () => {
  authInstance.defaults.headers.common.Authorization = "";
};

export const register = createAsyncThunk(
  "auth/register",
  async (userData, thunkApi) => {
    try {
      const { data } = await authInstance.post("/register", userData);
      setToken(data.access_token);
      return data;
    } catch (error) {
      return thunkApi.rejectWithValue(
        error.response?.data?.message || error.message
      );
    }
  }
);

export const login = createAsyncThunk(
  "auth/login",
  async (userData, thunkApi) => {
    try {
      const { data } = await authInstance.post("/login", userData);
      setToken(data.access_token);
      return data;
    } catch (error) {
      return thunkApi.rejectWithValue(
        error.response?.data?.message || error.message
      );
    }
  }
);

export const logout = createAsyncThunk("/logout", async (_, thunkApi) => {
  try {
    clearToken();
    return {};
  } catch (error) {
    return thunkApi.rejectWithValue(error.message);
  }
});

export const refreshUser = createAsyncThunk(
  "auth/refreshUser",
  async (_, thunkApi) => {
    const state = thunkApi.getState();
    const token = state.auth.access_token;

    if (!token) return thunkApi.rejectWithValue("No valid refresh token");

    try {
      const { data } = await authInstance.post("/refresh", {
        access_token: token,
      });
      setToken(data.access_token);
      return data;
    } catch (error) {
      return thunkApi.rejectWithValue(
        error.response?.data?.message || error.message
      );
    }
  }
);
