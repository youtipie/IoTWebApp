import { createAsyncThunk } from "@reduxjs/toolkit";
import { authInstance } from "../auth/operations";

export const fetchNetworks = createAsyncThunk(
  "networks/fetchNetworks",
  async (_, thunkApi) => {
    try {
      const { data } = await authInstance.get("/networks");
      console.log("Fetch Networks Response:", data); // Лог відповіді
      return data;
    } catch (error) {
      console.error("Fetch Networks Error:", error); // Лог помилки
      return thunkApi.rejectWithValue(
        error.response?.data?.message || error.message
      );
    }
  }
);

export const createNetwork = createAsyncThunk(
  "networks/createNetwork",
  async (networkData, thunkApi) => {
    try {
      const { data } = await authInstance.post("/networks", networkData);
      console.log("Network Created:", data); // Лог створеної мережі
      return data;
    } catch (error) {
      console.error("Create Network Error:", error); // Лог помилки
      return thunkApi.rejectWithValue(
        error.response?.data?.message || error.message
      );
    }
  }
);

export const deleteNetwork = createAsyncThunk(
  "networks/deleteNetwork",
  async (networkId, thunkApi) => {
    try {
      // Виконання запиту до API для видалення мережі
      const response = await authInstance.delete(`/networks/${networkId}`);
      console.log(response);

      return networkId; // Повертаємо ID мережі, яку треба видалити
    } catch (error) {
      // Обробка помилок на сервері (наприклад, 404, 403)
      const errorMessage =
        error.response?.data?.message || "Failed to delete network.";
      return thunkApi.rejectWithValue(errorMessage);
    }
  }
);

export const updateNetworkName = createAsyncThunk(
  "networks/updateNetworkName",
  async ({ id, name }, { rejectWithValue }) => {
    try {
      const response = await authInstance.put(
        `http://127.0.0.1:5000/networks/${id}`,
        {
          name: name,
        }
      );
      return response.data;
    } catch (error) {
      return rejectWithValue(
        error.response.data.message || "Failed to update network."
      );
    }
  }
);
