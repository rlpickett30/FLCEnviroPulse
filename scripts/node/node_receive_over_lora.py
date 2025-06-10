# node_receive_over_lora.py

import os

try:
    import serial
except ImportError:
    serial = None  # Allow simulator-only environments

from lora_simulator import LoraSimulator


class LoRaReceiver:
    def __init__(self, mode='simulated', port='/dev/ttyS0', baudrate=9600, timeout=2):
        self.mode = mode
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

        if self.mode == 'real':
            if serial is None:
                raise ImportError("pyserial is required for real LoRa mode.")
            self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
        elif self.mode == 'simulated':
            self.sim = LoraSimulator()
        else:
            raise ValueError("Mode must be 'real' or 'simulated'")

    def receive_message(self):
        if self.mode == 'real':
            if self.ser.in_waiting:
                raw_bytes = self.ser.read_until(b'\n')
                return raw_bytes.strip()
            return None
        else:
            return self.sim.get_next_message()
