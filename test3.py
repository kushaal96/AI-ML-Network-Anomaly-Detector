from scapy.all import sniff

packets = sniff(count=10)  # Capture 10 packets
packets.summary()
