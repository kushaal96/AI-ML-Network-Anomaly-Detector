import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";
import usePacketData from "./usePacketData"; // Make sure it's using the correct custom hook
import "../styles/TrafficAnalysis.css";

const TrafficAnalysis = () => {
  const {
    packets, // Change rawPackets to packets here
    ipDomains = {},
  } = usePacketData(); // get data from usePacketData

  const navigate = useNavigate();

  const [liveData, setLiveData] = useState({
    ipPairs: {},
    srcPorts: {},
    dstPorts: {},
    domainCounts: {},
  });

  useEffect(() => {
    const ipPairs = {};
    const srcPorts = {};
    const dstPorts = {};
    const domainCounts = {};

    packets.forEach((p) => { // Use packets here
      const pair = `${p.src_ip} → ${p.dst_ip}`;
      ipPairs[pair] = (ipPairs[pair] || 0) + 1;

      srcPorts[p.src_port] = (srcPorts[p.src_port] || 0) + 1;
      dstPorts[p.dst_port] = (dstPorts[p.dst_port] || 0) + 1;

      const domain = ipDomains[p.src_ip] || "Unknown";
      domainCounts[domain] = (domainCounts[domain] || 0) + 1;
    });

    setLiveData({
      ipPairs,
      srcPorts,
      dstPorts,
      domainCounts,
    });
  }, [packets, ipDomains]); // Make sure packets is included in the dependency array

  const commonIPPairs = Object.entries(liveData.ipPairs).sort((a, b) => b[1] - a[1]);
  const sortedSrcPorts = Object.entries(liveData.srcPorts).sort((a, b) => b[1] - a[1]);
  const sortedDstPorts = Object.entries(liveData.dstPorts).sort((a, b) => b[1] - a[1]);
  const sortedDomains = Object.entries(liveData.domainCounts).sort((a, b) => b[1] - a[1]);

  return (
    <div className="analysis-container">
      <button className="back-button" onClick={() => navigate("/", { replace: true })}>
        ← Back to Dashboard
      </button>

      <h2>📊 Traffic Analysis</h2>
      <p className="live-count">Total Packets: {packets.length}</p>

      <div className="tables-row">
        {/* Common IP Pairs */}
        <div className="table-box">
          <h3>Common IP Pairs</h3>
          <table>
            <thead><tr><th>Pair</th><th>Count</th></tr></thead>
            <tbody>
              {commonIPPairs.map(([pair, count], i) => (
                <tr key={i}><td>{pair}</td><td>{count}</td></tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Common Source Ports */}
        <div className="table-box">
          <h3>Common Source Ports</h3>
          <table>
            <thead><tr><th>Port</th><th>Count</th></tr></thead>
            <tbody>
              {sortedSrcPorts.map(([port, count], i) => (
                <tr key={i}><td>{port}</td><td>{count}</td></tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Common Destination Ports */}
        <div className="table-box">
          <h3>Common Destination Ports</h3>
          <table>
            <thead><tr><th>Port</th><th>Count</th></tr></thead>
            <tbody>
              {sortedDstPorts.map(([port, count], i) => (
                <tr key={i}><td>{port}</td><td>{count}</td></tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Repeated Domains */}
        <div className="table-box">
          <h3>Repeated Domains</h3>
          <table>
            <thead><tr><th>Domain</th><th>Count</th></tr></thead>
            <tbody>
              {sortedDomains.map(([domain, count], i) => (
                <tr key={i}><td>{domain}</td><td>{count}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default TrafficAnalysis;