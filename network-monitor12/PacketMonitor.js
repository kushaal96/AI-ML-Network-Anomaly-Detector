import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';

const PacketMonitor = () => {
    const [packets, setPackets] = useState([]);
    const socket = io('http://localhost:5000');  // Connect to the backend Flask server

    useEffect(() => {
        // Listen for new packets from the backend
        socket.on('new_packet', (data) => {
            setPackets((prevPackets) => [...prevPackets, data]);
        });
    }, []);

    return (
        <div>
            <h1>📡 Network Anomaly Scanner</h1>
            <table>
                <thead>
                    <tr>
                        <th>Source IP</th>
                        <th>Destination IP</th>
                        <th>Protocol</th>
                        <th>Packet Length</th>
                        <th>Source Port</th>
                        <th>Destination Port</th>
                        <th>Prediction</th>
                    </tr>
                </thead>
                <tbody>
                    {packets.map((packet, index) => (
                        <tr key={index}>
                            <td>{packet.src_ip}</td>
                            <td>{packet.dst_ip}</td>
                            <td>{packet.protocol}</td>
                            <td>{packet.packet_length}</td>
                            <td>{packet.src_port}</td>
                            <td>{packet.dst_port}</td>
                            <td>{packet.prediction}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default PacketMonitor;
