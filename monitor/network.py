import socket
import time
import uuid
from datetime import datetime, timezone

import psutil

from core.events import Event


class NetworkMonitor:
    """Read-only monitor for network sockets belonging to this machine."""

    def __init__(self, interval=1.0):
        self.interval = interval
        self._seen = set()

    @staticmethod
    def _connection_key(conn):
        local = getattr(conn, "laddr", None)
        remote = getattr(conn, "raddr", None)
        return (
            getattr(conn, "fd", -1),
            getattr(conn, "type", 0),
            getattr(local, "ip", ""),
            getattr(local, "port", 0),
            getattr(remote, "ip", ""),
            getattr(remote, "port", 0),
        )

    @staticmethod
    def _event_from_connection(conn):
        local = conn.laddr
        remote = conn.raddr
        protocol = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
        return Event(
            event_type="PORT_CONNECTION",
            source=local.ip,
            destination=remote.ip,
            port=remote.port,
            protocol=protocol,
            metadata={
                "status": conn.status,
                "pid": conn.pid,
                "collector": "psutil",
                "mode": "real",
            },
            simulation_id="",
            timestamp=datetime.now(timezone.utc),
            event_id=str(uuid.uuid4()),
        )

    def snapshot(self):
        """Return newly observed established/connecting Internet sockets."""
        events = []
        current = set()

        try:
            connections = psutil.net_connections(kind="inet")
        except (psutil.AccessDenied, psutil.Error) as exc:
            raise RuntimeError(
                "Could not read network connections. Try running PowerShell as Administrator."
            ) from exc

        for conn in connections:
            if not conn.raddr or not conn.laddr:
                continue
            if conn.family not in (socket.AF_INET, socket.AF_INET6):
                continue

            key = self._connection_key(conn)
            current.add(key)
            if key in self._seen:
                continue

            # Ignore listeners and sockets without a meaningful remote endpoint.
            if conn.status == psutil.CONN_LISTEN:
                continue

            events.append(self._event_from_connection(conn))

        self._seen = current
        return events

    def stream(self):
        """Yield newly observed connections until interrupted."""
        while True:
            for event in self.snapshot():
                yield event
            time.sleep(self.interval)
