# gateway/rak2287_driver.py

import subprocess
import json
import platform


def receive_packet():
    """
    Attempts to read the most recent LoRa packet from the packet log.
    Skips operation on Windows systems.
    """
    print("[RECEIVE] Inside receive_packet()")

    # ❌ Hardware receive unsupported on Windows
    if platform.system() == "Windows":
        print("[RAK2287] Skipping hardware receive — not supported on Windows.")
        return None

    try:
        # Read the last line from the packet log
        result = subprocess.run(
            ["tail", "-n", "1", "/var/log/lora/packets.jsonl"],
            capture_output=True,
            text=True,
            timeout=0.5
        )

        line = result.stdout.strip()
        if not line:
            return None

        packet = json.loads(line)
        if "data" in packet:
            return bytes.fromhex(packet["data"])

    except (subprocess.SubprocessError, json.JSONDecodeError, KeyError) as e:
        print(f"[RAK2287] Error reading packet: {e}")

    return None
