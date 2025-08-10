import { configureStore } from "@reduxjs/toolkit";
import authReducer from "../features/auth/authSlice";
import parcelsReducer from "../features/parcels/parcelsSlice";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    parcels: parcelsReducer,
  },
});
