import { createSlice } from "@reduxjs/toolkit";
import { fetchDevices, addDevice, deleteDevice } from "./operations";

const devicesSlice = createSlice({
  name: "devices",
  initialState: {
    devices: [],
    loading: false,
    error: null,
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDevices.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDevices.fulfilled, (state, action) => {
        state.loading = false;
        state.devices = action.payload;
      })
      .addCase(fetchDevices.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(addDevice.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(addDevice.fulfilled, (state, action) => {
        state.loading = false;
        state.devices.push(action.payload);
      })
      .addCase(addDevice.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(deleteDevice.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteDevice.fulfilled, (state, action) => {
        state.loading = false;
        state.devices = state.devices.filter(
          (device) => device.id !== action.payload
        );
      })
      .addCase(deleteDevice.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const devicesReducer = devicesSlice.reducer;
