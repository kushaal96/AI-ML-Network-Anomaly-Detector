from scapy.all import sniff

def packet_callback(packet):
    print(packet.summary())  # Print a summary of each captured packet

print("📡 Listening for packets...")
sniff(prn=packet_callback, count=10)  # Capture 10 packets
