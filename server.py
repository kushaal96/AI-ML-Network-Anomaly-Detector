from flask import Flask, jsonify
from flask_cors import CORS  
from flask_socketio import SocketIO
import pandas as pd
import joblib
from scapy.all import sniff, IP, TCP, UDP, DNS, DNSQR
import threading
from datetime import datetime  
import requests
import numpy as np

app = Flask(__name__)
CORS(app)  # Allow CORS for all domains
socketio = SocketIO(app, cors_allowed_origins="*")

print("🚀 Server starting...")

# Load trained model & scaler
try:
    model = joblib.load("anomaly_detector.pkl")
    scaler = joblib.load("scaler.pkl")
    print("✅ Model and Scaler loaded successfully")
except Exception as e:
    print(f"❌ Error loading model/scaler: {e}")
    model, scaler = None, None  # Prevent crashes if files are missing

detected_packets = []  # Store detected packets
ip_to_domain = {}  # Store IP-to-Domain mappings

def resolve_domain(ip):
    """ Try to resolve domain using stored DNS mappings first, then reverse lookup """
    if ip in ip_to_domain:
        return ip_to_domain[ip]  # Return cached domain
    
    try:
        # Reverse DNS lookup fallback
        response = requests.get(f"https://api.hackertarget.com/reverseiplookup/?q={ip}")
        domain = response.text.strip()
        if domain:
            ip_to_domain[ip] = domain
            return domain
    except Exception as e:
        print(f"⚠️ Error resolving domain: {e}")

    return "Unknown"

def dns_sniffer(packet):
    """ Capture DNS queries and store resolved domain names """
    if packet.haslayer(DNS) and packet.getlayer(DNS).qr == 0:  # Only DNS Requests
        domain_name = packet[DNSQR].qname.decode()[:-1]  # Extract domain
        src_ip = packet[IP].src
        ip_to_domain[src_ip] = domain_name  # Store mapping

def process_packet(packet):
    """Process incoming packets and detect anomalies."""
    try:
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            protocol = packet.proto
            packet_length = len(packet)
            timestamp = datetime.now().timestamp()  # Convert to numerical timestamp

            src_port, dst_port = 0, 0
            if packet.haslayer(TCP):
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
            elif packet.haslayer(UDP):
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport

            # Convert to DataFrame for prediction
            data = pd.DataFrame([[protocol, packet_length, timestamp, src_port, dst_port]], 
                 columns=['protocol', 'packet_length', 'timestamp', 'src_port', 'dst_port'])

            # Ensure model and scaler exist
            if model and scaler:
                try:
                    data_scaled = scaler.transform(data)

                    # Predict anomaly
                    prediction = model.predict(data_scaled)[0]
                    score = model.decision_function(data_scaled)[0]

                    # Assign severity levels
                    if score < -0.05:
                        severity = "High"
                    elif score < -0.02:
                        severity = "Medium"
                    elif score < 0:
                        severity = "Low"
                    else:
                        severity = "Normal"

                    domain = resolve_domain(src_ip)  # Get domain name

                    result = {
                        "src_ip": src_ip,
                        "dst_ip": dst_ip,
                        "protocol": "TCP" if protocol == 6 else "UDP" if protocol == 17 else "Other",
                        "packet_length": packet_length,
                        "src_port": src_port,
                        "dst_port": dst_port,
                        "timestamp": timestamp,
                        "anomaly_score": round(score, 6),
                        "prediction": severity,
                        "domain": domain
                    }

                    print(f"📡 New Packet Processed: {result}")
                    detected_packets.append(result)
                    socketio.emit('new_packet', result)  # Send data to frontend

                except Exception as e:
                    print(f"⚠️ Model Prediction Error: {e}")
            else:
                print("⚠️ Model or Scaler not loaded, skipping prediction.")

    except Exception as e:
        print(f"⚠️ Error processing packet: {e}")

@app.route('/')
def home():
    return "✅ Flask server is running!"

@app.route('/packets')
def get_packets():
    """Retrieve detected packets."""
    return jsonify(detected_packets)

@app.route('/get_domain/<ip>')
def get_domain(ip):
    """ Return the resolved domain for a given IP address """
    return jsonify({"domain": resolve_domain(ip)})

def start_sniffing():
    """Start network packet sniffing."""
    print("🔍 Sniffing started...")
    sniff(prn=process_packet, store=False)

# Start DNS sniffer in a separate thread
threading.Thread(target=lambda: sniff(filter="udp port 53", prn=dns_sniffer, store=0), daemon=True).start()

if __name__ == '__main__':
    try:
        threading.Thread(target=start_sniffing, daemon=True).start()
        print("🚀 Running Flask server on port 5000...")
        socketio.run(app, debug=True, port=5000)
    except KeyboardInterrupt:
        print("🛑 Server shutting down...")
