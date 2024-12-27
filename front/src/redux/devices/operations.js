import { createAsyncThunk } from "@reduxjs/toolkit";
import { authInstance } from "../auth/operations";

// Fetch devices in a specific network
export const fetchDevices = createAsyncThunk(
  "devices/fetchDevices",
  async (networkId, thunkApi) => {
    try {
      const { data } = await authInstance.get(`/networks/${networkId}/devices`);
      return data;
    } catch (error) {
      return thunkApi.rejectWithValue(
        error.response?.data?.message || error.message
      );
    }
  }
);

// Add a device to a specific network
export const addDevice = createAsyncThunk(
  "devices/addDevice",
  async ({ networkId, deviceData }, thunkApi) => {
    try {
      const { data } = await authInstance.post(
        `/networks/${networkId}/devices`,
        deviceData
      );
      return data;
    } catch (error) {
      return thunkApi.rejectWithValue(
        error.response?.data?.message || error.message
      );
    }
  }
);

// Delete a device from a specific network
export const deleteDevice = createAsyncThunk(
  "devices/deleteDevice",
  async ({ networkId, deviceId }, thunkApi) => {
    try {
      await authInstance.delete(`/networks/${networkId}/devices/${deviceId}`);
      return deviceId;
    } catch (error) {
      return thunkApi.rejectWithValue(
        error.response?.data?.message || error.message
      );
    }
  }
);
