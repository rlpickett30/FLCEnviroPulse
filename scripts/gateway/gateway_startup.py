import subprocess

# All launched in background with their own logging if needed
scripts = [
    "gateway_receive_over_lora.py",
    "gateway_server_inbound_listener.py"
]

# Optional: Add logging if needed
for script in scripts:
    print(f"Launching {script}...")
    subprocess.Popen(["python3", f"/home/pi/enviroPulse/gateway/{script}"])
