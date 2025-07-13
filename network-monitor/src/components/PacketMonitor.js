import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import usePacketData from "./usePacketData";
import TrafficGraph from "./TrafficGraph";
import StaticGraph from "./StaticGraph";
import PacketTable from "./PacketTable";
import SeverityPieChart from "./SeverityPieChart";
import "../styles/PacketMonitor.css";

const PacketMonitor = () => {
  const {
    filteredPackets,
    isLive,
    toggleLiveTraffic,
    ipDomains,
    searchQuery,
    setSearchQuery,
    filter,
    setFilter,
  } = usePacketData();

  const [showStaticGraph, setShowStaticGraph] = useState(false);
  const navigate = useNavigate();

  return (
    <div className="packet-monitor-container">
      <h1>📡 Network Monitor</h1>

      <div className="search-filter-container">
        <input
          type="text"
          placeholder="Search by IP, Port, Protocol, Severity..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="search-bar"
        />
        <select
          className="dropdown"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        >
          <option value="All">All</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
          <option value="Normal">Normal</option>
        </select>
      </div>

      <div className="button-container">
        <button
          className={`toggle-button ${isLive ? "live" : "stopped"}`}
          onClick={toggleLiveTraffic}
        >
          {isLive ? "🔴 Stop Traffic" : "🟢 Start Traffic"}
        </button>
        <button
          className="export-button"
          onClick={() => setShowStaticGraph((prev) => !prev)}
        >
          📊 {showStaticGraph ? "Hide" : "Show"} Static Graph
        </button>
        <button className="analysis-button" onClick={() => navigate("/traffic-analysis")}>
          📈 More Traffic Analysis
        </button>
      </div>

      <div className="graph-pie-container">
        <TrafficGraph packets={filteredPackets} />
        <SeverityPieChart packets={filteredPackets} />
      </div>

      {showStaticGraph && <StaticGraph packets={filteredPackets} />}
      <PacketTable packets={filteredPackets} ipDomains={ipDomains} />
    </div>
  );
};

export default PacketMonitor;