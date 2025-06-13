# main_interactive_lora_receiver_sim.py

from node.node_message_decoder import MessageDecoder
from node.node_inbound_message_builder import InboundBuilder
from node.node_dispatch import Dispatcher
from node.node_constructor import ConstructedEvent

class InboundSimulator:
    def __init__(self):
        self.decoder = MessageDecoder()
        self.builder = InboundBuilder()
        self.dispatcher = Dispatcher()

        self.test_messages = {
            "1": bytes.fromhex("07000000010006020000000A"),  # Valid 12-byte ACK
            "2": bytes.fromhex("07000000020103020000000B"),  # Retry for Change Mode, UID 11
            "3": bytes.fromhex("070000000302050200000011"),
            "4": bytes.fromhex("060000000101020000000C"),  
            "5": bytes.fromhex("050000000D0000000D"),                
            "6": bytes.fromhex("0200000000" + "3f99999a" + "40066666" + "01C2" + "01" + "02" + "001E" + "02" + "0000000E"),
            "7": bytes.fromhex("0300000001193C2790020000000F"),       # Fail
        }

    def run(self):
        while True:
            print("\n[INBOUND SIM MENU]")
            for key, label in [
                ("1", "Send ACK"),
                ("2", "Send Retry"),
                ("3", "Send Fail"),
                ("4", "Change Mode → Avis TDOA"),
                ("5", "Send Init"),
                ("6", "Send Telemetry"),
                ("7", "Send Weather"),
                ("8", "Quit"),
            ]:
                print(f"{key}. {label}")

            choice = input("Select a message to simulate: ").strip()

            if choice == "8":
                print("Exiting inbound simulator.")
                break
            elif choice in self.test_messages:
                self.process_message(self.test_messages[choice])
            else:
                print("Invalid selection. Try again.")

    def process_message(self, raw):
        try:
            print(f"\n[RAW]: {raw.hex()}")
            decoded = self.decoder.decode_and_validate(raw)
            print(f"[DECODED]: {decoded}")
            constructed = self.builder.build(decoded)
            if constructed:
                print(f"[EVENT]: {constructed.to_dict()}")
                self.dispatcher.handle_event(constructed)
            else:
                print("[WARN] Event construction failed.")
        except Exception as e:
            print(f"[ERROR] Failed to process message: {e}")


if __name__ == "__main__":
    sim = InboundSimulator()
    sim.run()
