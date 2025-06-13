import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# main_interactive_sim_environmental.py

import struct
import json

from node.node_message_decoder import MessageDecoder
from node.node_inbound_message_builder import InboundBuilder
from node.node_dispatch import Dispatcher
from node.node_constructor import ConstructedEvent
from utils.protocol import Protocol
from node.node_unique_id_manager import UniqueIdManager
from node import node_time

# Mock sensor imports (match full pipeline behavior)
from node import node_weather_sampler as weather_sampler
from node import node_telemetry as telemetry
from scripts import birdnet_edit


from node.node_time_mode_manager import get_mode
print(f"[DEBUG] Current node_time mode: {get_mode()}")

def split_hex_chunks(packed_hex, field_lengths):
    """
    Takes a hex string and a list of field lengths (in bytes),
    returns a list of hex chunks corresponding to each field.
    """
    chunks = []
    index = 0
    for length in field_lengths:
        hex_chars = length * 2  # 1 byte = 2 hex chars
        chunk = packed_hex[index:index + hex_chars]
        chunks.append(chunk)
        index += hex_chars
    return chunks

def print_delim_and_translated(decoded, packed_hex, field_lengths):
    # --- DELIM: show chunked raw bytes ---
    chunks = split_hex_chunks(packed_hex, field_lengths)
    print(f"[DELIM]: {' | '.join(chunks)}")

    # --- DECODE HEADER AND CONTENT ---
    header = decoded.get("header", {})
    content = decoded.get("content", {})

    event_name = header.get("event_id", "")
    timestamp = header.get("timestamp", "")
    node = content.get("node_id", "")
    uid = content.get("uid", "")

    # Prebuild common fields
    parts = [
        f"Event=Avis Detection" if event_name == "avis_event" else f"Event={event_name}",
        f"Time={timestamp}",
        
    ]

    # Event-specific fields
    if event_name == "avis_event":
        species = content.get("taxonomy", "")
        confidence = content.get("confidence", "")
        parts += [
            f"Species={species}",
            f"Confidence={confidence}",
        ]

    elif event_name == "weather_event":
        temp = content.get("temp", 0.0)
        humid = content.get("humidity", 0.0)
        pressure = content.get("pressure", 0.0)
        parts += [
            f"Temp={temp:.1f}°C",
            f"Humidity={humid:.1f}%",
            f"Pressure={pressure:.1f}hPa",
        ]

    elif event_name == "telemetry_event":
        lat = content.get("latitude", 0.0)
        lon = content.get("longitude", 0.0)
        alt = content.get("altitude", 0.0)
        parts += [
            f"Lat={lat:.5f}",
            f"Lon={lon:.5f}",
            f"Alt={alt:.1f}m",
        ]
    parts.append(f"Node={node}")
    parts.append(f"UID={uid}")
    print(f"[TRANS]: {' | '.join(parts)}")


class ManualSimulator:
    def __init__(self):
        self.structures = self.load_protocol_structure()
        self.protocol = Protocol(map_directory="config/maps")
        self.uid_manager = UniqueIdManager(persistence_file="config/uid_counter.txt")
        self.decoder = MessageDecoder()
        self.builder = InboundBuilder()
        self.dispatcher = Dispatcher()
        
    def safe_int(self, value, fallback=0):
        try:
            return int(value)
        except (TypeError, ValueError):
            return fallback    
        
    def load_protocol_structure(self):  # ← now a class method 
        base_path = os.path.dirname(os.path.abspath(__file__))
        relative_path = os.path.join(base_path, "..", "config", "structure_protocol", "structure_protocol.json")
        structure_path = os.path.abspath(relative_path)

        with open(structure_path, "r") as f:
            return json.load(f)


    def run(self):
        while True:
            print("\n[SIM MENU]")
            print("1. Simulate Avis Detection")
            print("2. Simulate Weather Sample")
            print("3. Simulate Telemetry Sample")
            print("4. Quit")

            choice = input("Select a message to simulate: ").strip()

            if choice == "1":
                self.simulate_avis_detection()
            elif choice == "2":
                self.simulate_weather_sample()
            elif choice == "3":
                self.simulate_telemetry_sample()
            elif choice == "4":
                print("Exiting simulator.")
                break
            else:
                print("Invalid selection. Try again.")

    def pack_and_process(self, event_key, values):
        try:
            def print_event_readable(decoded):
                print("\n[DECODED]: {")
                print("  'header': {")
                for key, value in decoded.get("header", {}).items():
                    print(f"    '{key}': {repr(value)},")
                print("  },")
                print("  'content': {")
                for key, value in decoded.get("content", {}).items():
                    print(f"    '{key}': {repr(value)},")
                print("  }\n}")
                
            structure = self.structures[event_key]
            fmt = structure["format"]
            
#            for i, val in enumerate(values):
#                print(f"[CHECK] Value {i}: {val} ({type(val).__name__})")
            
            packed = struct.pack(fmt, *values)
            print(f"\n[RAW]: {packed.hex()}")

            # Define byte lengths for this event (update per event type below)
            event_field_lengths = {
                "avis_event":      [1, 4, 2, 1, 1, 4],  # event_type | timestamp | taxonomy | confidence | node_id | uid
                "weather_event": [1, 4, 4, 4, 4, 1, 4],
                "telemetry_event": [1, 4, 4, 4, 2, 1, 1, 2, 1, 4],
            }

            # Lookup current field sizes
            field_lengths = event_field_lengths.get(event_key, [])

            # Decode and print breakdowns
            packed_hex = packed.hex()
            decoded = self.decoder.decode_and_validate(packed)
            print_delim_and_translated(decoded, packed_hex, field_lengths)
            print_event_readable(decoded)
            constructed = self.builder.build(decoded)
            if constructed:
                print(f"[EVENT]: {constructed.to_dict()}")
                self.dispatcher.handle_event(constructed)
            else:
                print("[WARN] Event construction failed.")
        except Exception as e:
            print(f"[ERROR] {event_key}: {e}")

    def simulate_avis_detection(self):
        print("[SIM] Simulating Avis Detection")

        # Step 1: Get mock detection and timestamp
        detection = birdnet_edit.get_mock_birdnet_detection()
        timestamp = int(node_time.get_timestamp())

        # Step 2: Validate and encode confidence
#        print(f"[DEBUG] Encoding label: '{detection['confidence']}'")
        if detection["confidence"] == "Unknown":
            print("[WARN] Skipping detection: confidence label was 'Unknown'")
            return

        encoded_conf = self.protocol.encode_confidence_level(detection["confidence"])
#        print(f"[DEBUG] Encoded confidence level: {encoded_conf}")

        # Step 3: Encode taxonomy
        encoded_taxonomy = self.protocol.encode_taxonomy(detection["species"])
#        print(f"[DEBUG] Taxonomy: '{detection['species']}' → {encoded_taxonomy} ({type(encoded_taxonomy).__name__})")

        # Step 4: Build packed values
        values = [
            self.protocol.encode_event_type("avis_event"),
            timestamp,
            encoded_taxonomy,
            encoded_conf,      # confidence before node_id ✅
            7,                 # node_id
            self.uid_manager.next_id()
        ]

        # Step 5: Run full pipeline
        self.pack_and_process("avis_event", values)


    def simulate_weather_sample(self):
        print("[SIM] Simulating Weather Sample")

        sample = weather_sampler.sample_weather()
        timestamp = int(node_time.get_timestamp())
        temp = sample.get("temperature", 0.0)
        humid = sample.get("humidity", 0.0)
        pressure = sample.get("pressure", 0.0)


       

        # --- Pack and Dispatch ---
        values = [
            self.protocol.encode_event_type("weather_event"),
            timestamp,
            temp,
            humid,
            pressure,
            7,
            self.uid_manager.next_id()
        ]

        self.pack_and_process("weather_event", values)




    def simulate_telemetry_sample(self):
        print("[SIM] Simulating Telemetry Sample")

        sample = telemetry.process_telemetry()
        timestamp = int(node_time.get_timestamp())

        values = [
            self.protocol.encode_event_type("telemetry_event"),
            timestamp,
            sample["latitude"],
            sample["longitude"],
            int(sample["calibrated_altitude_gps"]),
            int(sample["pps_valid"]) if "pps_valid" in sample else 1,
            int(sample["fix_quality"]) if "fix_quality" in sample else 2,
            int(sample["avg_count"]) if "avg_count" in sample else 5,
            7,  # node_id
            self.uid_manager.next_id()
        ]

        self.pack_and_process("telemetry_event", values)

if __name__ == "__main__":
    sim = ManualSimulator()
    sim.run()
