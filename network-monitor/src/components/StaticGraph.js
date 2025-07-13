import React, { useState } from "react";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, LineElement, CategoryScale, LinearScale, PointElement, Tooltip } from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip);

const StaticGraph = ({ packets }) => {
  const [snapshot, setSnapshot] = useState(null);

  const generateSnapshot = () => {
    // 📌 Get the last 5 mins of packets
    const fiveMinutesAgo = Date.now() - 5 * 60 * 1000;
    const recentPackets = packets.filter(packet => new Date(packet.timestamp).getTime() >= fiveMinutesAgo);

    // ✅ Compute severity counts for snapshot
    const severityCounts = { High: 0, Medium: 0, Low: 0, Normal: 0 };
    recentPackets.forEach(packet => {
      severityCounts[packet.prediction] = (severityCounts[packet.prediction] || 0) + 1;
    });

    // ✅ Format data for Line Chart
    setSnapshot({
      labels: ["High", "Medium", "Low", "Normal"],
      datasets: [
        {
          label: "Severity Count (Last 5 Mins)",
          data: [
            severityCounts.High || 0,
            severityCounts.Medium || 0,
            severityCounts.Low || 0,
            severityCounts.Normal || 0,
          ],
          borderColor: "#007bff",
          backgroundColor: "rgba(0, 123, 255, 0.2)",
          borderWidth: 2,
          pointRadius: 3,
          tension: 0.3, // Smooth curve
        },
      ],
    });
  };

  return (
    <div className="graph-container">
      <h2>📊 Static Anomaly Snapshot</h2>
      <button className="export-button" onClick={generateSnapshot}>📸 Capture Snapshot</button>
      {snapshot && (
        <div style={{ height: "300px", width: "100%" }}>
          <Line data={snapshot} />
        </div>
      )}
    </div>
  );
};

export default StaticGraph;
