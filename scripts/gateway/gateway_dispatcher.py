# gateway_dispatcher.py

from gateway.gateway_logger import GatewayLogger
from gateway.gateway_push_to_server import ServerReceiver
from gateway.gateway_send_over_lora import LoraOutboundSender
from gateway.gateway_ack_retry_manager import AckRetryManager

"""
This dispatcher routes finalized gateway events to their target subsystems.
Each event is assumed to be fully constructed and validated.
"""

# Instantiate subsystems
logger = GatewayLogger()
server = ServerReceiver()
lora = LoraOutboundSender()

# Ack manager requires binary payloads, so we register it after outbound encoding
# Dispatcher must provide callback to build failure events
ack_manager = AckRetryManager(dispatcher=None, send_function=lora.send)
ack_manager.start()


def dispatch_event(event):
    uid = event.get("gateway_header", {}).get("uid", "UID_MISSING")
    raw_targets = event.get("target", "unknown")

    # Allow for multi-target delivery (e.g. "ack_retry_manager+push_to_server")
    targets = raw_targets.split("+") if "+" in raw_targets else [raw_targets]

    for target in targets:
        target = target.strip()

        if target == logger.get_target():
            logger.log_event(event, stage="DISPATCH")

        elif target == server.get_target():
            server.receive_event(event)

        elif target == lora.get_target():
            lora.send(event)

            # If event needs ack tracking, register it here
            if is_ack_required(event["event_type"]):
                try:
                    from gateway.gateway_lora_outbound_object_builder import build_lora_payload
                    encoded = build_lora_payload(event)
                    ack_manager.register(uid, event, encoded)
                except Exception as e:
                    print(f"[ACK REGISTER ERROR] {e}")

        elif target == "ack_retry_manager":
            uid = (
                event.get("uid") or
                event.get("gateway_header", {}).get("uid")
            )
            ack_manager.acknowledge(uid)

        else:
            print(f"[DISPATCH WARNING] Unknown target: {target}")
    print(f"[DISPATCHED] Event UID {uid} type: {event['event_type']} → {raw_targets}")


def is_ack_required(event_type):
    return event_type in {"telemetry", "avis_lite", "avis_tdoa"}


# Optional for graceful shutdown (e.g. on SIGINT)
def stop_dispatcher():
    ack_manager.stop()
