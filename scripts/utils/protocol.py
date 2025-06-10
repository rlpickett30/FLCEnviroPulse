# scripts/utils/protocol.py

import json
import struct
from typing import Any, Dict, Optional, Union

from node.node_registries_manager import get_event_code, get_taxonomy_code


# ──────────────────────────────────────────────────────────────────────────────
# Compression maps (static for now; you may later load these from JSON files)
# ──────────────────────────────────────────────────────────────────────────────

CONFIDENCE_MAP: Dict[str, int] = {
    "0–24%":   0,
    "25–49%":  1,
    "50–64%":  2,
    "65–74%":  3,
    "75–84%":  4,
    "85–92%":  5,
    "93–97%":  6,
    "98–100%": 7
}


# ──────────────────────────────────────────────────────────────────────────────
# Example: Avis Lite binary encoder / decoder (for reference or unit tests)
# ──────────────────────────────────────────────────────────────────────────────

def encode_avis_lite_event(event: Dict[str, Any]) -> Optional[bytes]:
    """
    Encode an Avis Lite event into a fixed 8-byte packet:
      [ event_type (1B) | timestamp (4B) | taxonomy_id (2B) | confidence (1B) ]
    """
    try:
        event_type   = get_event_code("avis_lite_event")
        timestamp    = int(event["time"])
        taxonomy_id  = int(event["taxonomy"])
        confidence   = int(event["confidence"])

        return struct.pack(">B I H B", event_type, timestamp, taxonomy_id, confidence)

    except Exception as e:
        print(f"[protocol][encode_avis_lite_event] error: {e}")
        return None


def decode_avis_lite_packet(payload: bytes) -> Optional[Dict[str, Any]]:
    """
    Decode an 8-byte Avis Lite packet back into its fields.
    """
    try:
        event_type, timestamp, taxonomy_id, confidence = struct.unpack(">B I H B", payload)
        return {
            "event_type": event_type,
            "time":       timestamp,
            "taxonomy":   taxonomy_id,
            "confidence": confidence
        }
    except Exception as e:
        print(f"[protocol][decode_avis_lite_packet] error: {e}")
        return None


# ──────────────────────────────────────────────────────────────────────────────
# Public API: Message Decode / Encode (simulation stubs, replace later)
# ──────────────────────────────────────────────────────────────────────────────

def decode_message(raw_bytes: bytes) -> Dict[str, Any]:
    """
    Bypass stub for incoming LoRa packets.
    Looks at the first byte to pick an event type string, then returns
    a fully-formed 'header' + 'content' dict for your pipeline.
    """
    event_lookup = {
        0x01: "ACK",
        0x02: "Retry",
        0x03: "Change Mode",
        0x04: "Init",
        0x05: "Startup ACK",
        0x06: "Telemetry",
        0x07: "Weather",
        0x08: "Error",
        0x09: "Fail"
    }

    event_id   = raw_bytes[0]
    event_type = event_lookup.get(event_id, "Unknown")

    return {
        "header": {
            "event_id": event_type,
            "timestamp": 1718040000,
            "sender":    "simulator",
            "version":   "v0.1"
        },
        "content": {
            "node_id":    7,
            "mode":       "Avis TDOA",
            "confidence": 3,
            "taxonomy":   893,
            "time":       27645
        }
    }


def encode_message(message_dict: Dict[str, Any]) -> bytes:
    """
    Bypass stub for outgoing LoRa packets.
    Serializes the full message object to JSON for visibility.
    Later, replace this with real struct packing.
    """
    return json.dumps(message_dict).encode("utf-8")
