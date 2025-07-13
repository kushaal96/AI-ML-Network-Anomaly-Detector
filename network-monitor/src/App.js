import React, { useState, useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import PacketMonitor from "./components/PacketMonitor";
import TrafficAnalysis from "./components/TrafficAnalysis";
import "./App.css";

function App() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    document.body.classList.toggle("dark-theme", darkMode);
  }, [darkMode]);

  return (
    <div className={`app-container ${darkMode ? "dark-mode" : "light-mode"}`}>
      <button onClick={() => setDarkMode(prev => !prev)} className="theme-toggle-button">
        {darkMode ? "☀ Light Mode" : "🌙 Dark Mode"}
      </button>

      <Routes>
        <Route path="/" element={<PacketMonitor />} />
        <Route path="/traffic-analysis" element={<TrafficAnalysis />} />
      </Routes>
    </div>
  );
}

export default App;