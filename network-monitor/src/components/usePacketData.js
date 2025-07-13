import { useMemo, useState } from "react";
import { usePacketContext } from "./PacketDataContext";

const usePacketData = () => {
  const { packets, isLive, setIsLive } = usePacketContext();
  const [searchQuery, setSearchQuery] = useState("");
  const [filter, setFilter] = useState("All");

  const ipDomains = {}; // If using domain resolution, update this

  // Filtered packets based on search and severity
  const filteredPackets = useMemo(() => {
    return packets.filter(packet => {
      const query = searchQuery.toLowerCase();
      const matchesQuery = (
        packet.src_ip.includes(query) ||
        packet.dst_ip.includes(query) ||
        packet.protocol.toLowerCase().includes(query) ||
        packet.src_port.toString().includes(query) ||
        packet.dst_port.toString().includes(query) ||
        packet.packet_length.toString().includes(query) ||
        packet.anomaly_score.toFixed(6).includes(query) ||
        packet.prediction.toLowerCase().includes(query)
      );
      const matchesFilter = filter === "All" || packet.prediction === filter;
      return matchesQuery && matchesFilter;
    });
  }, [packets, searchQuery, filter]);

  // Enrich packets (optional use in tables)
  const enrichedPackets = filteredPackets.map(p => ({
    ...p,
    encryption: p.protocol.toLowerCase().includes("https") ? "TLS/SSL"
      : p.protocol.toLowerCase().includes("ssh") ? "SSH"
      : p.protocol.toLowerCase().includes("ipsec") ? "IPSec"
      : "None"
  }));

  // Stats (based on filteredPackets)
  const packetCount = filteredPackets.length;

  const ipPairs = {};
  const srcPorts = {};
  const dstPorts = {};
  const domainCounts = {};

  filteredPackets.forEach(p => {
    const ipKey = `${p.src_ip} → ${p.dst_ip}`;
    ipPairs[ipKey] = (ipPairs[ipKey] || 0) + 1;

    srcPorts[p.src_port] = (srcPorts[p.src_port] || 0) + 1;
    dstPorts[p.dst_port] = (dstPorts[p.dst_port] || 0) + 1;

    const domain = ipDomains[p.src_ip] || "Unknown";
    domainCounts[domain] = (domainCounts[domain] || 0) + 1;
  });

  const commonIPPairs = Object.entries(ipPairs).sort((a, b) => b[1] - a[1]);
  const sortedSrcPorts = Object.entries(srcPorts).sort((a, b) => b[1] - a[1]);
  const sortedDstPorts = Object.entries(dstPorts).sort((a, b) => b[1] - a[1]);
  const repeatedDomains = Object.entries(domainCounts).sort((a, b) => b[1] - a[1]);

  return {
    packets, // Full packet list for TrafficAnalysis
    filteredPackets, // Filtered list for dashboard
    enrichedPackets, // Optional use in table
    isLive,
    toggleLiveTraffic: () => setIsLive(prev => !prev),
    ipDomains,
    searchQuery,
    setSearchQuery,
    filter,
    setFilter,
    packetCount,
    commonIPPairs,
    sortedSrcPorts,
    sortedDstPorts,
    repeatedDomains,
  };
};

export default usePacketData;