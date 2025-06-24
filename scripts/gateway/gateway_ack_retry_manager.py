# gateway_ack_retry_manager.py

import time
import threading

class PendingMessage:
    def __init__(self, event_obj, encoded_bytes, timestamp=None, retries=0):
        self.event_obj = event_obj
        self.encoded_bytes = encoded_bytes
        self.timestamp = timestamp or time.time()
        self.retries = retries

    def increment_retry(self):
        self.retries += 1
        self.timestamp = time.time()


class AckRetryManager:
    def __init__(self, dispatcher, send_function, max_retries=3, retry_interval=2.5):
        self.dispatcher = dispatcher
        self.send_function = send_function
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.pending = {}  # uid: PendingMessage
        self.lock = threading.Lock()
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._retry_loop, daemon=True).start()

    def stop(self):
        self.running = False

    def register(self, uid, event_obj, encoded_bytes):
        with self.lock:
            self.pending[uid] = PendingMessage(event_obj, encoded_bytes)

    def acknowledge(self, uid):
        with self.lock:
            if uid in self.pending:
                del self.pending[uid]

    def _retry_loop(self):
        while self.running:
            now = time.time()
            retry_list = []

            with self.lock:
                for uid, message in list(self.pending.items()):
                    if now - message.timestamp >= self.retry_interval:
                        if message.retries < self.max_retries:
                            retry_list.append((uid, message))
                        else:
                            self._handle_failure(uid, message)

            for uid, message in retry_list:
                message.increment_retry()
                print(f"[GatewayAckRetry] Retry {message.retries} for UID {uid}")
                self.send_function(message.encoded_bytes)

            time.sleep(1)

    def _handle_failure(self, uid, message):
        print(f"[GatewayAckRetry] Max retries reached for UID {uid}. Dispatching failure event.")
        fail_event = self.dispatcher.build_ack_retry_failure(message.event_obj)
        self.send_function(fail_event.encode())
        with self.lock:
            del self.pending[uid]
