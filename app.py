from flask import Flask, jsonify
from flask_socketio import SocketIO
import pandas as pd
import joblib
from scapy.all import sniff, IP, TCP, UDP
import threading
from flask_cors import CORS  # CORS for handling cross-origin requests

app = Flask(__name__)
CORS(app)  # Enable CORS
socketio = SocketIO(app, cors_allowed_origins="*")

# Load trained model & scaler
model = joblib.load("trained_model.pkl")  # Path to your trained model
scaler = joblib.load("scaler.pkl")  # If you have a scaler saved for preprocessing

detected_packets = []

def process_packet(packet):
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = packet.proto
        packet_length = len(packet)
        src_port, dst_port = 0, 0

        if packet.haslayer(TCP):
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
        elif packet.haslayer(UDP):
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport

        # Placeholder for anomaly score and prediction
        result = {
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "protocol": "TCP" if protocol == 6 else "UDP" if protocol == 17 else "Other",
            "packet_length": packet_length,
            "src_port": src_port,
            "dst_port": dst_port,
            "anomaly_score": 0,  # Placeholder
            "prediction": "Normal"  # Placeholder
        }

        detected_packets.append(result)
        socketio.emit('new_packet', result)  # Emit packet data to frontend

@app.route('/packets')
def get_packets():
    return jsonify(detected_packets)

def start_sniffing():
    sniff(prn=process_packet, store=False)

if __name__ == '__main__':
    threading.Thread(target=start_sniffing, daemon=True).start()
    socketio.run(app, debug=True, port=5000)
