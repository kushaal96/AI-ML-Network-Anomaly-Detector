import React, { createContext, useContext, useEffect, useState } from "react";
import socket from "../socket";
import axios from "axios";

const PacketContext = createContext();

export const PacketProvider = ({ children }) => {
  const [packets, setPackets] = useState([]);
  const [isLive, setIsLive] = useState(true);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/packets")
      .then(res => setPackets(res.data))
      .catch(err => console.error("Initial fetch error:", err));
  }, []);

  useEffect(() => {
    const handleNewPacket = (packet) => {
      setPackets(prev => [packet, ...prev]);
    };

    if (isLive) {
      socket.on("new_packet", handleNewPacket);
    }

    return () => socket.off("new_packet", handleNewPacket);
  }, [isLive]);

  return (
    <PacketContext.Provider value={{ packets, setPackets, isLive, setIsLive }}>
      {children}
    </PacketContext.Provider>
  );
};

export const usePacketContext = () => useContext(PacketContext);