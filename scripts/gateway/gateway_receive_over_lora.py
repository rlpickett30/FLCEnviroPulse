import socket
import struct
import json
import binascii
from datetime import datetime

# === Configuration ===
UDP_IP = "0.0.0.0"      # Listen on all interfaces
UDP_PORT = 1700         # LoRa packet forwarder default port

# === Setup UDP socket ===
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"[{datetime.utcnow()}] Listening for LoRa packets on {UDP_IP}:{UDP_PORT}...\n")

while True:
    data, addr = sock.recvfrom(4096)  # Receive UDP packet
    if len(data) < 4:
        continue  # Ignore malformed packets

    version = data[0]
    token = data[1:3]
    pkt_type = data[3]
    payload = data[4:]

    if pkt_type == 0x00:  # PUSH_DATA
        # Send PUSH_ACK back to sender
        ack = struct.pack("!B2sB", version, token, 0x01)
        sock.sendto(ack, addr)

        try:
            json_start = data.find(b'{')
            if json_start != -1:
                json_payload = json.loads(data[json_start:].decode("utf-8"))

                if "rxpk" in json_payload:
                    for packet in json_payload["rxpk"]:
                        ts = packet.get("time", "unknown")
                        freq = packet.get("freq", "unknown")
                        datr = packet.get("datr", "unknown")
                        rssi = packet.get("rssi", "unknown")
                        snr = packet.get("lsnr", "unknown")
                        raw_data = packet.get("data", "")

                        print(f"[{ts}] LoRa packet received:")
                        print(f"  Frequency: {freq} MHz")
                        print(f"  Data rate: {datr}")
                        print(f"  RSSI: {rssi} dBm, SNR: {snr} dB")
                        print(f"  Base64 payload: {raw_data}")

                        # Optional: decode base64 if payload is known to be ASCII
                        try:
                            decoded = binascii.a2b_base64(raw_data).decode("utf-8")
                            print(f"  Decoded: {decoded}")
                        except:
                            print(f"  [!] Payload could not be decoded as UTF-8")

                        print("-" * 40)

        except Exception as e:
            print(f"[!] Failed to parse incoming packet: {e}")
