# main_simulate.py

from node_receive_over_lora import LoRaReceiver
from node_message_decoder import MessageDecoder
from node_inbound_message_builder import InboundBuilder
from node_dispatch import Dispatcher

def run_simulation():
    receiver = LoRaReceiver(mode='simulated')
    decoder = MessageDecoder()
    builder = InboundBuilder()
    dispatcher = Dispatcher()

    print("[SIM] Starting LoRa simulation...\n")

    while True:
        raw = receiver.receive_message()
        if raw is None:
            print("[SIM] No more simulated messages.")
            break

        print(f"[SIM] Received raw: {raw}")

        try:
            decoded = decoder.decode_and_validate(raw)
            print(f"[SIM] Decoded: {decoded}")
        except Exception as e:
            print(f"[SIM] Decode error: {e}")
            continue

        event_obj = builder.build(decoded)
        if event_obj:
            print(f"[SIM] Constructed Event: {event_obj.to_dict()}")
            dispatcher.handle_event(event_obj)
        else:
            print("[SIM] Failed to build event.")

        print("-" * 50)

if __name__ == "__main__":
    run_simulation()
