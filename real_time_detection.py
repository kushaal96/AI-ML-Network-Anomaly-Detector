from scapy.all import sniff, IP, TCP, UDP, ARP
import pandas as pd
import joblib
import time
import numpy as np
import os

# Load trained model & scaler
model = joblib.load("anomaly_detector.pkl")
scaler = joblib.load("scaler.pkl")

# Define ignored ports (safe services like DNS, HTTPS, DHCP, Facebook Messenger, etc.)
ignored_ports = {53, 443, 123, 67, 68, 5353, 5222}

# Initialize base time for timestamp normalization
base_time = time.time()

# Anomaly severity thresholds
LOW_RISK_THRESHOLD = -0.05
MEDIUM_RISK_THRESHOLD = -0.15
HIGH_RISK_THRESHOLD = -0.5

# Log file for storing high-risk anomalies
log_file = "anomaly_log.csv"
if not os.path.exists(log_file):
    pd.DataFrame(columns=["timestamp", "protocol", "packet_length", "src_ip", "dst_ip", "src_port", "dst_port", "anomaly_score", "risk_level"]).to_csv(log_file, index=False)

# Debug mode (Set to False for clean output)
DEBUG_MODE = False  

# Function to process packets
def process_packet(packet):
    global base_time

    # Extract base packet details
    protocol = packet.proto if hasattr(packet, "proto") else 0
    packet_length = len(packet)
    timestamp = time.time() - base_time

    # Extract IP layer details
    if not packet.haslayer(IP):
        return  # Ignore non-IP packets

    src_ip = packet[IP].src
    dst_ip = packet[IP].dst

    # Ignore invalid IPs (0.0.0.0 packets)
    if src_ip == "0.0.0.0" or dst_ip == "0.0.0.0":
        return  

    # Extract ports if applicable
    src_port, dst_port = 0, 0
    if packet.haslayer(TCP):
        src_port, dst_port = packet[TCP].sport, packet[TCP].dport
    elif packet.haslayer(UDP):
        src_port, dst_port = packet[UDP].sport, packet[UDP].dport

    # Ignore known safe services
    if src_port in ignored_ports or dst_port in ignored_ports:
        return  

    # Ignore ARP & ICMPv6 ND packets (normal network behavior)
    if packet.haslayer(ARP) or "ICMPv6ND_" in packet.summary():
        return  

    # Prepare data for model
    data = pd.DataFrame([[protocol, packet_length, timestamp, src_port, dst_port]], 
                         columns=['protocol', 'packet_length', 'timestamp', 'src_port', 'dst_port'])

    # Apply feature scaling
    data_scaled = scaler.transform(data)

    # Predict anomaly (-1 = anomaly, 1 = normal)
    prediction = model.predict(data_scaled)[0]
    score = model.decision_function(data_scaled)[0]

    # Determine Risk Level
    if prediction == -1:
        if score >= LOW_RISK_THRESHOLD:
            risk_level = "🟡 Low Risk"
        elif score >= MEDIUM_RISK_THRESHOLD:
            risk_level = "🟠 Medium Risk"
        else:
            risk_level = "🔴 High Risk"
    else:
        risk_level = "✅ Normal"

    # Structured Output
    print("\n================= PACKET ANALYSIS =================")
    print(f"Protocol:        {'TCP' if protocol == 6 else 'UDP' if protocol == 17 else 'Other'}")
    print(f"Packet Length:   {packet_length} bytes")
    print(f"Timestamp:       {timestamp:.4f} sec")
    print(f"Source IP:       {src_ip}")
    print(f"Destination IP:  {dst_ip}")
    print(f"Source Port:     {src_port}")
    print(f"Destination Port:{dst_port}")
    print(f"Anomaly Score:   {score:.6f}")
    print(f"Risk Level:      {risk_level}")

    # Show debug info only if enabled
    if DEBUG_MODE:
        print(f"[DEBUG] Packet Summary: {packet.summary()}")

    # Log only HIGH-RISK anomalies
    if prediction == -1 and score < HIGH_RISK_THRESHOLD:
        print("\n🚨 [ALERT] High-Risk Anomaly Detected! 🚨")

        # Log to CSV
        anomaly_data = pd.DataFrame([[timestamp, protocol, packet_length, src_ip, dst_ip, src_port, dst_port, score, risk_level]],
                                    columns=["timestamp", "protocol", "packet_length", "src_ip", "dst_ip", "src_port", "dst_port", "anomaly_score", "risk_level"])
        anomaly_data.to_csv(log_file, mode='a', header=False, index=False)

    print("===================================================\n")

# Start live packet capture
print("🔍 Monitoring network traffic for anomalies... Press Ctrl+C to stop.")
sniff(prn=process_packet, store=False)
