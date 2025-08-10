import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  parcels: [],       // List of parcels
  loading: false,    // Loading state for fetch/create/update
  error: null,       // Error message
};

const parcelsSlice = createSlice({
  name: "parcels",
  initialState,
  reducers: {
    fetchParcelsStart(state) {
      state.loading = true;
      state.error = null;
    },
    fetchParcelsSuccess(state, action) {
      state.loading = false;
      state.parcels = action.payload;
    },
    fetchParcelsFailure(state, action) {
      state.loading = false;
      state.error = action.payload;
    },
    addParcel(state, action) {
      state.parcels.push(action.payload);
    },
    updateParcel(state, action) {
      const index = state.parcels.findIndex(p => p.id === action.payload.id);
      if (index !== -1) {
        state.parcels[index] = action.payload;
      }
    },
    deleteParcel(state, action) {
      state.parcels = state.parcels.filter(p => p.id !== action.payload);
    },
  },
});

export const {
  fetchParcelsStart,
  fetchParcelsSuccess,
  fetchParcelsFailure,
  addParcel,
  updateParcel,
  deleteParcel,
} = parcelsSlice.actions;

export default parcelsSlice.reducer;
