# birdnet_edit.py
# This script is meant to be inserted as a modification to BirdNET.
# It generates a minimal event payload whenever a detection occurs.

def generate_avis_event(taxonomy_id, confidence, timestamp):
    return {
        "event_type": "avis_detected",
        "taxonomy": taxonomy_id,
        "confidence": confidence,
        "time": timestamp  # Seconds since midnight UTC
    }
