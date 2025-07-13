from scapy.all import rdpcap, IP, TCP, UDP
import pandas as pd

# Load the pcap file
packets = rdpcap("network_traffic2_1.pcap")  # Replace with your actual file name

# List to store extracted features
data = []

for pkt in packets:
    if IP in pkt:  # Check if packet has IP layer
        features = {
            "src_ip": pkt[IP].src,
            "dst_ip": pkt[IP].dst,
            "protocol": pkt[IP].proto,
            "packet_length": len(pkt),
            "timestamp": pkt.time
        }
        if TCP in pkt:
            features["src_port"] = pkt[TCP].sport
            features["dst_port"] = pkt[TCP].dport
        elif UDP in pkt:
            features["src_port"] = pkt[UDP].sport
            features["dst_port"] = pkt[UDP].dport
        data.append(features)

# Convert to DataFrame and save as CSV
df = pd.DataFrame(data)
df.to_csv("network_features.csv", index=False)
print("Feature extraction complete. Saved as network_features.csv")
