# startup_simulator.py

import sys
import os
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from gateway.gateway_server_inbound_event_packer import ServerEventPacker
from gateway.gateway_object_constructor import GatewayEventConstructor
from gateway.gateway_dispatcher import dispatch_event as dispatch_gateway
from gateway.gateway_logger import GatewayLogger
from utils.protocol import Protocol
from gateway.gateway_lora_packet_source import receive_packet
# ✅ Use clean injection layer instead of driver
from gateway.gateway_lora_packet_source import inject_simulated_packet

# ✅ Ensure simulation mode is active
USE_SIMULATION = True

packer = ServerEventPacker()
constructor = GatewayEventConstructor()
logger = GatewayLogger()
protocol = Protocol("config/maps")

def print_debug(event, stage="DISPATCH"):
    uid = event["gateway_header"].get("uid", "UID_MISSING")
    print("\n--- DEBUG ---")
    print(f"[{stage}] UID: {uid} | Event: {event.get('event_type')} | Target: {event.get('target')}")
    print("--------------\n")

def simulate_server_event(raw_json):
    event = packer.build(raw_json)
    constructed = constructor.construct(event)
    print_debug(constructed, stage="GATEWAY INPUT")
    logger.log_event(constructed)
    dispatch_gateway(constructed)

def simulate_inbound_lora_event(event_type, raw_bytes):
    try:
        print ("hi")
        decoded = protocol.decode(event_type, raw_bytes)
        constructed = constructor.construct(decoded)
        print_debug(constructed, stage="LORA INPUT")
        logger.log_event(constructed)
        dispatch_gateway(constructed)
    except Exception as e:
        print(f"[LORA DECODE ERROR] {e}")


def show_menu():
    print("\n==== STARTUP SIMULATOR ====\n")
    print("INBOUND SERVER EVENTS\n")
    print("[1] Start Project")
    print("[2] Change Mode")
    print("[3] Recalibrate\n")
    print("INBOUND LORA EVENTS\n")
    print("[4] ACK")
    print("[5] Startup ACK")
    print("[6] Weather")
    print("[7] Avis Lite")
    print("[8] Avis TDOA")
    print("[9] Telemetry")
    print("[10] Unknown Format")
    print("[11] Quit")
    return input("Select event: ").strip()

def main():
    while True:
        choice = show_menu()

        if choice == "1":
            simulate_server_event({"event_type": "start_project"})

        elif choice == "2":
            simulate_server_event({
                "event_type": "change_mode",
                "mode": "avis_tdoa"
            })

        elif choice == "3":
            simulate_server_event({"event_type": "recalibrate"})

        elif choice == "4":
            print("[SIM] Injecting ACK packet...")
            ack_packet = (
                b"\x07" +             # event_type (7 = ack_retry_event)
                b"\x01" +             # type (1 = ACK)
                b"\x02" +             # $responds_to (2 = weather, for example)
                b"\x01" +             # node_id
                b"\x00\x00\x00\x04"   # uid (4)
            )
            inject_simulated_packet(ack_packet)
            receive_packet()
        
        
        elif choice == "5":
            startup_packet=(b"\x04\x00\x00\x00\x03\x01\x01\x01\x01\x00\x00\x00\x03")
            inject_simulated_packet(startup_packet)
            receive_packet()
        

        elif choice == "6":
            print("[SIM] Injecting weather packet...")
            weather_packet=(
                b"\x03\x00\x00\x00\x02"
                b"\x41\xB8\x00\x00"  # temperature: 23.0
                b"\x42\x48\x00\x00"  # humidity: 50.0
                b"\x44\x7A\x00\x00"  # pressure: 1000.0
                b"\x01\x00\x00\x00"  # wind speed
                b"\x02"              # wind direction
            )
            inject_simulated_packet(weather_packet)
            receive_packet()   

        elif choice == "7":
            avis_lite_packet=(b"\x01\x00\x00\x00\x04\x00\xC9\x03\x05\x00\x00\x00\x04")
            inject_simulated_packet(avis_lite_packet)
            receive_packet()
            
        elif choice == "8":
            avis_tdoa_packet=(b"\x01\x00\x00\x00\x05\x01\xA5\x02\x06\x00\x00\x00\x05")
            inject_simulated_packet(avis_tdoa_packet)
            receive_packet()
            
        elif choice == "9":
            print("[SIM] Injecting telemetry packet...")
            telemetry_packet = (
                b"\x02" +                        # event_type
                b"\x00\x00\x00\x64" +            # timestamp = 100
                b"\x42\x17\x8F\x5C" +            # lat = 37.7749
                b"\xC2\xF4\xA5\xE3" +            # lon = -122.419
                b"\x08\x08" +                    # altitude = 2056
                b"\x01" +                        # pps_valid = 1
                b"\x04" +                        # fix_quality = 4
                b"\x00\x17" +                    # avg_count = 23
                b"\x06" +                        # node_id = 6
                b"\x00\x0C\x0C\x13"              # uid = 789123
                )
            inject_simulated_packet(telemetry_packet)
            receive_packet()
            
        elif choice == "10":
            inject_simulated_packet(b"\xFF\xFF\xFF")

        elif choice == "11":
            print("Exiting simulator.")
            break

        else:
            print("Invalid choice. Try again.")

        time.sleep(0.5)

if __name__ == "__main__":
    main()
