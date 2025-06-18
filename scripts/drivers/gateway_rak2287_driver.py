# gateway_rak2287_driver.py

import subprocess
import json

def receive_packet():
    """
    Reads a LoRa packet from the RAK2287 concentrator using packet-forwarder JSON output.
    This function assumes you're using a custom concentrator config that writes to a known
    stdout/log stream or socket with JSON-formatted packets.

    Returns:
        bytes: Raw LoRa payload, or None if nothing received.
    """
    try:
        # This is a placeholder — replace with your real log reading or pipe logic
        result = subprocess.run([
            "tail", "-n", "1", "/var/log/lora/packets.jsonl"
        ], capture_output=True, text=True, timeout=0.5)

        line = result.stdout.strip()
        if not line:
            return None

        packet = json.loads(line)
        if 'data' in packet:
            return bytes.fromhex(packet['data'])

    except (subprocess.SubprocessError, json.JSONDecodeError, KeyError) as e:
        print(f"[RAK2287] Error reading packet: {e}")

    return None
