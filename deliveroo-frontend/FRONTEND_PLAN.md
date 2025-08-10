# Deliveroo Frontend Development Plan

## Phase 1 – Project Setup & Base Architecture
**Goal:** Get the development environment ready with structure, routing, and state management.

### 1. Initialize Project
- Create React app (Vite or CRA)
- Install dependencies:
npm install react-router-dom axios @reduxjs/toolkit react-redux @react-google-maps/api
- Create `.env` for API URLs & Google Maps API key

### 2. Folder Structure
api/ # Backend calls
features/ # Redux slices
pages/ # Full-screen routes
components/ # Reusable UI components
utils/ # Helper functions


### 3. Routing
- `App.jsx` with routes:
  - `/login`
  - `/register`
  - `/` (dashboard)
  - `/parcels`
  - `/admin`

### 4. Redux Store
- `store.js`
- Create empty `authSlice` and `parcelsSlice`

---

## Phase 2 – Authentication Flow
**Goal:** Let users register, log in, and stay logged in.

### UI
- `LoginPage.jsx` (username/password form)
- `RegisterPage.jsx` (name, email, password form)

### Redux Logic (`authSlice`)
- `loginSuccess`
- `logout`
- Save token & user in state and `localStorage`

### API Calls (`authApi.js`)
- `loginUser(credentials)`
- `registerUser(data)`

### Route Protection
- `PrivateRoute.jsx` for authenticated routes
- Redirect to `/login` if not logged in

---

## Phase 3 – Parcel Management (User)
**Goal:** Users can create, view, edit, and cancel their parcel orders.

### Parcel List Page
- Show list of parcels with status
- Button to view details
- Button to cancel (only if not delivered)

### Parcel Detail Page
- Show pickup/destination on a map
- Show computed distance & duration (Google API)
- Show current status & location
- Allow **Change Destination** if not delivered

### Create Parcel Form
- Pickup location (input + map picker)
- Destination location (input + map picker)
- Weight (for price quote)
- Submit to backend

### API Calls (`parcelApi.js`)
- `getParcels()`
- `getParcelById(id)`
- `createParcel(data)`
- `updateParcel(id, data)`
- `cancelParcel(id)`

### Redux (`parcelsSlice.js`)
- `setParcels`
- `addParcel`
- `updateParcel`
- `removeParcel`

---

## Phase 4 – Google Maps Integration
**Goal:** Display locations, routes, and distance.

### Map Component (`Map.jsx`)
- Props: pickup, destination
- Markers for each location
- Polyline connecting them

### Distance Calculation
- Use Google Maps **DirectionsService** or **DistanceMatrix API**
- Show travel time & distance on Parcel Detail Page

---

## Phase 5 – Admin Features
**Goal:** Admin can manage parcels.

### Admin Dashboard
- List all parcels
- Update status
- Update current location
- Changes trigger **email notifications** (backend handles)

### API Calls
- `updateParcelStatus(id, status)`
- `updateParcelLocation(id, location)`

---

## Phase 6 – Optional Enhancements
- Real-time updates (polling or websockets)
- Better form validation (Formik + Yup)
- Notifications in UI
- TailwindCSS or shadcn/ui for styling

---

## Development Order Recommendation
1. Setup & Redux store
2. Auth flow (login/register/logout)
3. User parcel management (create, list, details, cancel, change destination)
4. Google Maps integration
5. Admin dashboard
6. Styling & enhancements


