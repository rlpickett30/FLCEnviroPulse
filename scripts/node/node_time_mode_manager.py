# node_time_mode_manager.py
current_mode = "lite"

def set_mode(mode):
    global current_mode
    if mode in ["lite", "tdoa"]:
        current_mode = mode

def get_mode():
    return current_mode

