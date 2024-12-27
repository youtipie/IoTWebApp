import { createSlice } from "@reduxjs/toolkit";
import { fetchUserProfile } from "./operations";

const initialState = {
  user: null, // Дані користувача
  isLoading: false,
  error: null,
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUserProfile.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchUserProfile.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload; // Збереження даних користувача
      })
      .addCase(fetchUserProfile.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload; // Помилка, якщо не вдалося отримати профіль
      });
  },
});

export const userReducer = userSlice.reducer;
