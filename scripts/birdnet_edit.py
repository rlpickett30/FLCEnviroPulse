# birdnet_edit.py
# This script is meant to be inserted as a modification to BirdNET.
# It generates a minimal event payload whenever a detection occurs.
"""
def generate_avis_event(taxonomy_id, confidence, timestamp):
    return {
        "event_type": "avis_detected",
        "taxonomy": taxonomy_id,
        "confidence": confidence,
        "time": timestamp  # Seconds since midnight UTC
    }

"""
import random
from node import node_confidence_manager

BIRD_SPECIES = [
    "American Robin",
    "Northern Cardinal",
    "Blue Jay",
    "Mourning Dove",
    "Red-tailed Hawk",
    "Black-capped Chickadee",
    "House Finch",
    "Eastern Bluebird",
    "Downy Woodpecker",
    "American Goldfinch",
    "European Starling",
    "White-breasted Nuthatch",
    "Song Sparrow",
    "Great Horned Owl",
    "Northern Flicker",
    "Carolina Wren",
    "Killdeer",
    "Chipping Sparrow",
    "Barn Swallow",
    "Dark-eyed Junco"
]

def get_mock_birdnet_detection():
    species = random.choice(BIRD_SPECIES)
    raw_confidence = int(random.uniform(0, 100))  # float from 0–100
    confidence_label = node_confidence_manager.bin_confidence(raw_confidence)

    print(f"[SIM] {species} detected with {raw_confidence:.2f}% confidence → {confidence_label}")

    return {
        "species": species,
        "confidence": confidence_label
    }