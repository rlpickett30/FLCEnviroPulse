# node_confidence_manager.py

def bin_confidence(confidence_value):
    """
    Converts a float confidence score into a string label that matches
    the confidence_scale_map.json (8-bin nonlinear scale).
    """
    bins = [
        (0, 50, "0-50%"),
        (51, 65, "51-65%"),
        (66, 74, "66-74%"),
        (75, 80, "75-80%"),
        (81, 85, "81-85%"),
        (86, 90, "86-90%"),
        (91, 95, "91-95%"),
        (96, 100, "96-100%")
]

    for lower, upper, label in bins:
        if lower <= confidence_value <= upper:
            return label
        
    print(f"[DEBUG] Binning raw confidence: {confidence_value:.2f} → {label}")

    return "Unknown"