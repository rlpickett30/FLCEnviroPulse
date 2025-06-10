# main_interactive_sim.py

from node.node_message_decoder import MessageDecoder
from node.node_inbound_message_builder import InboundBuilder
from node.node_dispatch import Dispatcher

class ManualSimulator:
    def __init__(self):
        self.decoder = MessageDecoder()
        self.builder = InboundBuilder()
        self.dispatcher = Dispatcher()

        # Predefined raw messages (hex → bytes)
        self.test_messages = {
            "1": bytes.fromhex("01070000"),        # ACK
            "2": bytes.fromhex("02070001"),        # Retry
            "3": bytes.fromhex("0307000201"),      # Change Mode to TDOA
            "4": bytes.fromhex("04070003"),        # Init
            "5": bytes.fromhex("060700055A2C"),    # Telemetry
            "6": bytes.fromhex("07070006193201"),  # Weather
            "7": bytes.fromhex("08070007"),        # Error
            "8": bytes.fromhex("09070008"),        # Fail
        }

    def run(self):
        while True:
            print("\n[SIM MENU]")
            print("1. Send ACK")
            print("2. Send Retry")
            print("3. Change Mode → Avis TDOA")
            print("4. Send Init")
            print("5. Send Telemetry")
            print("6. Send Weather")
            print("7. Send Error")
            print("8. Send Fail")
            print("9. Quit")

            choice = input("Select a message to simulate: ").strip()

            if choice == "9":
                print("Exiting simulator.")
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
    sim = ManualSimulator()
    sim.run()
