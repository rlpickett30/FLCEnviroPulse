import time
import json
from datetime import datetime

# ----------------------------
# Config
# ----------------------------
REGISTRY_PATH = "./node_registry.json"
ENCLOSURE_LOOKUP = {
    "3F7": ["2A1C", "4D9E"]
    # Add more mock enclosures here
}
GPS_MOCK_SAMPLES = [
    {"lat": 37.7519, "lon": -107.6814, "alt": 2034.8, "hdop": 0.9},
    {"lat": 37.7520, "lon": -107.6815, "alt": 2035.2, "hdop": 0.8},
    {"lat": 37.7521, "lon": -107.6813, "alt": 2035.5, "hdop": 0.7},
    {"lat": 37.7518, "lon": -107.6816, "alt": 2034.7, "hdop": 1.0},
    {"lat": 37.7517, "lon": -107.6812, "alt": 2035.1, "hdop": 0.9},
    {"lat": 37.7520, "lon": -107.6814, "alt": 2035.0, "hdop": 0.8},
    {"lat": 37.7522, "lon": -107.6815, "alt": 2035.4, "hdop": 0.7},
    {"lat": 37.7519, "lon": -107.6816, "alt": 2034.9, "hdop": 0.8},
    {"lat": 37.7521, "lon": -107.6813, "alt": 2035.3, "hdop": 0.9},
    {"lat": 37.7520, "lon": -107.6812, "alt": 2035.2, "hdop": 0.8}
]

# ----------------------------
# Utility Functions
# ----------------------------
def now():
    return datetime.utcnow().isoformat()

def load_registry():
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)

def save_registry(reg):
    with open(REGISTRY_PATH, "w") as f:
        json.dump(reg, f, indent=2)

def print_node_entry(node):
    print(json.dumps(node, indent=2))

def average(samples, key):
    return round(sum(s[key] for s in samples) / len(samples), 6)

# ----------------------------
# Phase 1: User Input
# ----------------------------
project_name = input("Enter project name: ")
enclosures = input("Enter enclosure IDs (comma-separated): ").split(",")
enclosures = [e.strip() for e in enclosures]
print("\nLaunching simulation...")
time.sleep(1)

# ----------------------------
# Phase 2: Send Startup Command
# ----------------------------
node_ids = []
for enc in enclosures:
    node_ids.extend(ENCLOSURE_LOOKUP.get(enc, []))

registry = load_registry()
for node in registry["nodes"]:
    if node["DevEUI"] in node_ids:
        print(f"\n→ Sending startup message to node {node['DevEUI']}")
        node["status"] = "calibrating"
        node["node_mode"] = "startup"
        node["launch_time"] = now()
        print("   [✓] Status set to 'calibrating'")
        print("   [✓] Launch time recorded:", node["launch_time"])
        print("\nUpdated node registry entry:")
        print_node_entry(node)
        save_registry(registry)
        time.sleep(2)

# ----------------------------
# Phase 3: Acknowledge + Identity
# ----------------------------
for node in registry["nodes"]:
    if node["DevEUI"] in node_ids:
        node["node_type"] = "pi"
        node["firmware"] = "v0.9.3"
        node["taxonomy_version"] = "birdnet_v2"
        print(f"\n← Node {node['DevEUI']} acknowledged startup")
        print(f"   [✓] Status remains: {node['status']}")
        print(f"   [✓] Firmware: {node['firmware']} | Taxonomy: {node['taxonomy_version']}")
        save_registry(registry)
        time.sleep(2)

# ----------------------------
# Phase 4: Silence Period
# ----------------------------
print("\n[GPS CALIBRATION PHASE INITIATED]")
print("All nodes are now silent and collecting GPS data.\n")
for i in range(0, 16):
    print(f"→ {i:02d}:00 / 15:00 elapsed...")
    time.sleep(5)  # Simulate each minute as 5 seconds

print("\n[✓] GPS calibration complete for all nodes.")
print("[✓] Waiting 90 seconds for trailing nodes...")
time.sleep(5)  # Replace 90 with 5 for test speed

# ----------------------------
# Phase 5 & 6: Final Telemetry + Server Update
# ----------------------------
for node in registry["nodes"]:
    if node["DevEUI"] in node_ids:
        print(f"\n→ Node {node['DevEUI']} averaging GPS & altitude data...")

        lat = average(GPS_MOCK_SAMPLES, "lat")
        lon = average(GPS_MOCK_SAMPLES, "lon")
        alt = average(GPS_MOCK_SAMPLES, "alt")
        hdop = average(GPS_MOCK_SAMPLES, "hdop")

        node["gps"] = {
            "lat": lat,
            "lon": lon,
            "alt": alt,
            "hdop": hdop,
            "num_satellites": 8,
            "fix_type": 3,
            "method": "averaged"
        }

        node["status"] = "online"
        node["calibration_time"] = now()
        node["last_telemetry"] = now()

        print(f"   [✓] Averaged GPS: lat={lat}, lon={lon}, alt={alt}")
        print(f"   [✓] Node is now ONLINE.")
        save_registry(registry)
        time.sleep(2)

# ----------------------------
# Phase 7: Normal Mode
# ----------------------------
for node in registry["nodes"]:
    if node["DevEUI"] in node_ids:
        node["node_mode"] = "normal"
        print(f"→ Node {node['DevEUI']} entering NORMAL mode.")
        print("   [✓] Weather and detection services started.")
        save_registry(registry)
        time.sleep(2)

print("\n----------------------------------------")
print(f"Startup Complete for Project: {project_name}\n")
print("Online Nodes:")
for node in registry["nodes"]:
    if node["DevEUI"] in node_ids:
        print(f" - {node['DevEUI']} | model: {node['node_type']} | firmware: {node['firmware']} | lat: {node['gps']['lat']}, lon: {node['gps']['lon']}")
print(f"\nTotal: {len(node_ids)} nodes active")
print("----------------------------------------")
