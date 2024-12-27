import { createSlice } from "@reduxjs/toolkit";
import { fetchNetworks, createNetwork, deleteNetwork } from "./operations";

const networksSlice = createSlice({
  name: "networks",
  initialState: {
    items: [],
    isLoading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      // Fetch Networks
      .addCase(fetchNetworks.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchNetworks.fulfilled, (state, action) => {
        state.isLoading = false;
        state.items = action.payload; // Заміняємо список мереж
      })
      .addCase(fetchNetworks.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })

      // Create Network
      .addCase(createNetwork.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createNetwork.fulfilled, (state, action) => {
        state.isLoading = false;
        state.items = [...state.items, action.payload]; // додаємо нову мережу в масив
      })
      .addCase(createNetwork.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      })

      // Delete Network
      .addCase(deleteNetwork.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(deleteNetwork.fulfilled, (state, action) => {
        state.isLoading = false;
        state.items = state.items.filter(
          (network) => network.id !== action.payload
        );
      })
      .addCase(deleteNetwork.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload;
      });
  },
});

export const networksReducer = networksSlice.reducer;
