import { createAsyncThunk } from "@reduxjs/toolkit";
import { authInstance } from "../auth/operations";

export const fetchUserProfile = createAsyncThunk(
  "user/fetchUserProfile",
  async (_, { rejectWithValue }) => {
    try {
      const response = await authInstance.get("/me", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(
        error.response.data.message || "Failed to fetch user profile."
      );
    }
  }
);
