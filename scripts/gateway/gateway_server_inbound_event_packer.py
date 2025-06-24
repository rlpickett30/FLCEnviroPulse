# gateway_server_inbound_event_packer.py

from gateway.gateway_unique_id_manager import assign_uid  

class ServerEventPacker:
    def __init__(self):
        self.event_targets = {
            "start_project": "send_over_lora",
            "change_mode": "send_over_lora",
            "recalibrate": "send_over_lora",
        }

    def build(self, raw_json):
        event_type = raw_json.get("event_type", "unknown")        
        payload= {k: v for k, v in raw_json.items()
                     if k not in ("event_type")}
        
        # Build base object
        event_obj = {
            "gateway_header": {},
            "server_header":{ 
                "uid": assign_uid()
            },
            "event_type": event_type,
            "payload": payload,       
            "target": self._get_target(event_type)                    
        }
#        print("s inbound")
#        print (event_obj)
        return event_obj

    def _get_target(self, event_type):
        return self.event_targets.get(event_type, "send_over_lora")
