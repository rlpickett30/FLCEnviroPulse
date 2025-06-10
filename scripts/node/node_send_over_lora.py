# node_send_over_lora.py

import sys

try:
    import serial
    SERIAL_AVAILABLE = True
except ImportError:
    serial = None
    SERIAL_AVAILABLE = False

class LoRaSender:
    def __init__(self, port="/dev/ttyS0", baudrate=9600, timeout=1):
        self.ser = None
        if SERIAL_AVAILABLE:
            try:
                self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
            except Exception as e:
                print(f"[LoRaSender] Could not open serial port {port}: {e}", file=sys.stderr)
                self.ser = None
        else:
            print("[LoRaSender] pyserial not installed; running in simulation mode", file=sys.stderr)

    def send(self, payload_bytes: bytes):
        """
        Send bytes out over LoRa (or simulate if no serial).
        """
        if self.ser:
            try:
                self.ser.write(payload_bytes + b'\n')
            except Exception as e:
                print(f"[LoRaSender] Serial write failed: {e}", file=sys.stderr)
        else:
            # Simulation fallback: just print
            print(f"[LoRaSender] (simulated) payload → {payload_bytes!r}")
