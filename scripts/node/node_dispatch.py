# node_dispatch.py

from node.node_logger import Logger
from node.node_time import get_timestamp
from node.node_mode_manager import ModeManager
from node.node_ack_manager import AckManager
from node.node_lora_message_builder import OutboundMessageBuilder
from node.node_send_over_lora import LoRaSender
from node.node_initial_launch import InitialLaunch

class Dispatcher:
    def __init__(self):
        self.logger = Logger()
        self.mode_manager = ModeManager()
        self.ack_manager = AckManager()
        self.outbound_builder = OutboundMessageBuilder()
        self.sender = LoRaSender()

    def handle_event(self, constructed_event):
        event_type = constructed_event.base.event_type

        # Log all events
        self.logger.log(constructed_event)

        # Handle event-specific actions
        if event_type == "start_project":
            updated = InitialLaunch(constructed_event.inbound).handle()
            if updated:
                self.handle_event(updated)
            return

        if event_type == "Change Mode":
            self.mode_manager.update_mode(constructed_event.inbound)

        elif event_type == "Telemetry Update":
            self.time_manager.update(constructed_event.inbound)

        elif event_type == "Init" or event_type == "Startup ACK":
            self.mode_manager.initialize(constructed_event.inbound)

        # Handle ACK or retry logic
        if event_type in {"ACK", "Retry"}:
            ack_msg = self.ack_manager.build_response(constructed_event)
            if ack_msg:
                self.sender.send(self.outbound_builder.build(ack_msg))

        # Forward Telemetry or other outbound events
        if event_type in {"Avis Lite", "Avis TDOA", "Weather", "Telemetry"}:
            lora_msg = self.outbound_builder.build(constructed_event)
            if lora_msg:
                self.sender.send(lora_msg)

        # Handle telemetry timestamp update
        if event_type == "Telemetry Update":
            ts = get_timestamp()
            print(f"[Dispatch] Current timestamp: {ts}")
