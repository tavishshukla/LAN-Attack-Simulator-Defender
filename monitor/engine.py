from defender.detector import Detector
from defender.response import ResponseEngine
from dashboard.terminal import live_event, show_alert


def run_monitor(cfg, db, interval=1.0):
    monitor = __import__("monitor.network", fromlist=["NetworkMonitor"]).NetworkMonitor(interval)
    detector = Detector(cfg["detection"])
    response = ResponseEngine()

    print("\n=== LAN DEFENDER | REAL NETWORK MONITOR ===")
    print("Read-only telemetry from this computer. Press Ctrl+C to stop.\n")

    try:
        for event in monitor.stream():
            db.insert_event(event)
            live_event(event)

            for alert in detector.process(event):
                db.insert_alert(alert)
                db.insert_incident(alert)
                show_alert(alert)

                action = response.respond(alert)
                db.update_incident_response(alert.alert_id, action)
                print(f"[RESPONSE] {action}")

    except KeyboardInterrupt:
        print("\nMonitor stopped.")
