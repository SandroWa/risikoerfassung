import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import App from "./App";
import LandingPage from "./pages/LandingPage";
import RisikenPage from "./pages/RisikenPage";
import { Toaster } from "react-hot-toast";
import "./styles.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<App />}>
          <Route path="/" element={<LandingPage />} />
          <Route path="/risiken" element={<RisikenPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
    <Toaster
      position="bottom-center"
      toastOptions={{
        duration: 2500,
        style: {
          background: "#1f2937",
          color: "#f9fafb",
          fontSize: "0.9rem",
        },
        success: {
          iconTheme: { primary: "#10b981", secondary: "#f9fafb" },
        },
      }}
    />
  </React.StrictMode>
);
