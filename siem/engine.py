import json
import time

from siem.rules import classify
from siem.windows_events import WindowsEventCollector


class SIEM:
    def __init__(self, db, interval=2.0):
        self.db = db
        self.interval = interval
        self.collector = WindowsEventCollector()

    def poll_once(self):
        results = []
        for raw in self.collector.poll():
            if "error" in raw:
                print(f"[SIEM] Collector warning: {raw['error']}")
                continue

            self.db.insert_siem_event(raw)
            classified = classify(raw)
            if classified:
                self.db.insert_siem_alert(classified)
                results.append(classified)
                print(
                    f"[SIEM ALERT] {classified['severity']} "
                    f"{classified['rule']} "
                    f"(Event ID {classified['event_id']}, "
                    f"Record {classified['record_id']})"
                )
        return results

    def run(self):
        print("\n=== LAN DEFENDER | MINI SIEM ===")
        print("Read-only Windows Event Log monitoring. Press Ctrl+C to stop.\n")

        try:
            while True:
                self.poll_once()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\nSIEM stopped.")
