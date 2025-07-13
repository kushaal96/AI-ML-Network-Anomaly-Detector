import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
} from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip);

const TrafficGraph = ({ packets }) => {
  const maxPacketsToShow = 50;
  const [packetWindow, setPacketWindow] = useState([]);

  useEffect(() => {
    if (packets.length === 0) return;

    setPacketWindow((prev) => {
      const updated = [...prev, packets[packets.length - 1]];
      return updated.length > maxPacketsToShow ? updated.slice(1) : updated;
    });
  }, [packets]);

  const anomalyScores = packetWindow.map((p) => p.anomaly_score);
  const timestamps = packetWindow.map((p) =>
    new Date(p.timestamp).toLocaleTimeString("en-US", {
      minute: "2-digit",
      second: "2-digit",
    })
  );

  const yMin = Math.min(...anomalyScores, 0);
  const yMax = Math.max(...anomalyScores, 1);

  const data = {
    labels: timestamps,
    datasets: [
      {
        label: "Anomaly Score",
        data: anomalyScores,
        borderColor: "#007bff",
        backgroundColor: "rgba(0, 123, 255, 0.1)",
        borderWidth: 2,
        pointRadius: 2,
        tension: 0.4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 300,
      easing: "easeInOutQuart",
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Time",
          color: "#444",
        },
        ticks: {
          autoSkip: true,
          maxTicksLimit: 10,
        },
      },
      y: {
        title: {
          display: true,
          text: "Anomaly Score",
          color: "#444",
        },
        min: yMin - 0.2,
        max: yMax + 0.2,
        ticks: {
          stepSize: 0.1,
        },
      },
    },
    plugins: {
      tooltip: {
        callbacks: {
          label: (context) => `Score: ${context.parsed.y.toFixed(4)}`,
        },
      },
    },
  };

  return (
    <div className="traffic-graph">
      <h3>📊 Live Anomaly Graph</h3>
      <div style={{ height: "300px", width: "100%" }}>
        <Line data={data} options={options} />
      </div>
    </div>
  );
};

export default TrafficGraph;
