# gateway_server_inbound_object_builder.py

from gateway.gateway_base_object import build_base_event, ensure_uid

"""
Builds a decoded event object from raw JSON issued by the server.

Expected input format:
{
  "event_type": "start_project",
  "project_name": "Molas_Ridge",
  "mode": "avis_lite",
  "timestamp": 1718652392,
  "node_list": [3, 5, 9]
}
"""

def build_server_event(raw_json):
    # Wrap with gateway header
    event = build_base_event(raw_payload=None)  # No binary payload from server

    # Optional node info if targeting a specific node
    node_header = {}
    if "node_id" in raw_json:
        node_header["node_id"] = raw_json["node_id"]

    event.update({
        "event_type": raw_json.get("event_type", "unknown"),
        "node_header": node_header,
        "payload": {k: v for k, v in raw_json.items()
                    if k not in ("event_type", "node_id")}
    })

    # Assign UID if needed
    event = ensure_uid(event)

    return event
