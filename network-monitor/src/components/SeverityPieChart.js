import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
ChartJS.register(ArcElement, Tooltip, Legend);

const SeverityPieChart = ({ packets }) => {
  const getSeverityCounts = () => {
    const counts = { High: 0, Medium: 0, Low: 0, Normal: 0 };
    packets.forEach((packet) => {
      if (counts[packet.prediction] !== undefined) {
        counts[packet.prediction]++;
      }
    });
    return counts;
  };

  const severityCounts = getSeverityCounts();

  const pieData = {
    labels: ["High", "Medium", "Low", "Normal"],
    datasets: [
      {
        data: [
          severityCounts.High || 0,
          severityCounts.Medium || 0,
          severityCounts.Low || 0,
          severityCounts.Normal || 0,
        ],
        backgroundColor: ["#FF4D4D", "#FFA500", "#FFD700", "#90EE90"],
        hoverBackgroundColor: ["#D43F3F", "#CC8400", "#CCB800", "#77DD77"],
      },
    ],
  };

  return (
    <div className="pie-chart">
      <h2>📊 Severity Distribution</h2>
      <Pie data={pieData} />
    </div>
  );
};

export default SeverityPieChart;
