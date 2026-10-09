from dataclasses import dataclass
from datetime import datetime, timezone
import json

import win32evtlog


@dataclass
class WindowsEvent:
    channel: str
    record_id: int
    event_id: int
    timestamp: str
    computer: str
    source: str
    message: str
    level: str
    data: dict

    def as_dict(self):
        return {
            "channel": self.channel,
            "record_id": self.record_id,
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "computer": self.computer,
            "source": self.source,
            "message": self.message,
            "level": self.level,
            "data": self.data,
        }


class WindowsEventCollector:
    """Read-only Windows Event Log collector using the local Event Log API."""

    CHANNELS = ("Security", "System", "Application")

    def __init__(self, batch_size=50):
        self.batch_size = batch_size
        self._last_record = {}

    def _open(self, channel):
        return win32evtlog.OpenEventLog(None, channel)

    def _read_latest(self, handle):
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        return win32evtlog.ReadEventLog(handle, flags, 0) or []

    @staticmethod
    def _event_level(event):
        return str(getattr(event, "EventType", "UNKNOWN"))

    @staticmethod
    def _message(event):
        inserts = getattr(event, "StringInserts", None) or []
        return " | ".join(str(x) for x in inserts)

    def poll(self):
        """Return only records newer than the last record seen per channel."""
        output = []

        for channel in self.CHANNELS:
            handle = None
            try:
                handle = self._open(channel)
                records = self._read_latest(handle)
            except Exception as exc:
                output.append({
                    "error": f"{channel}: {exc}",
                    "channel": channel,
                })
                continue
            finally:
                if handle:
                    try:
                        win32evtlog.CloseEventLog(handle)
                    except Exception:
                        pass

            previous = self._last_record.get(channel, 0)
            new_records = [
                r for r in records
                if r.RecordNumber > previous
            ]

            for record in reversed(new_records[: self.batch_size]):
                event = WindowsEvent(
                    channel=channel,
                    record_id=record.RecordNumber,
                    event_id=record.EventID & 0xFFFF,
                    timestamp=record.TimeGenerated.replace(tzinfo=timezone.utc).isoformat(),
                    computer=record.ComputerName,
                    source=record.SourceName,
                    message=self._message(record),
                    level=self._event_level(record),
                    data={"strings": list(record.StringInserts or [])},
                )
                output.append(event.as_dict())

            if records:
                self._last_record[channel] = max(
                    self._last_record.get(channel, 0),
                    max(r.RecordNumber for r in records),
                )

        return output
