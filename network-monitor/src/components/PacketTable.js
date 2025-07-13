import React from "react";

const PacketTable = ({ packets = [], ipDomains = {} }) => {
  return (
    <div className="table-container">
      <table className="packet-table">
        <thead>
          <tr>
            <th>Source IP</th>
            <th>Destination IP</th>
            <th>Protocol</th>
            <th>Packet Length</th>
            <th>Source Port</th>
            <th>Destination Port</th>
            <th>Domain</th>
            <th>Anomaly Score</th>
            <th>Severity</th>
          </tr>
        </thead>
        <tbody>
          {packets.map((packet, index) => (
            <tr key={index} className={packet.prediction?.toLowerCase()}>
              <td>{packet.src_ip}</td>
              <td>{packet.dst_ip}</td>
              <td>{packet.protocol}</td>
              <td>{packet.packet_length}</td>
              <td>{packet.src_port}</td>
              <td>{packet.dst_port}</td>
              <td>{ipDomains?.[packet.src_ip] || "Resolving..."}</td>
              <td>{packet.anomaly_score?.toFixed(6)}</td>
              <td>{packet.prediction}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PacketTable;