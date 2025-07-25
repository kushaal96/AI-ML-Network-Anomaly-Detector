import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { BrowserRouter } from "react-router-dom";
import { PacketProvider } from "./components/PacketDataContext";
import "./index.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <PacketProvider>
        <App />
      </PacketProvider>
    </BrowserRouter>
  </React.StrictMode>
);