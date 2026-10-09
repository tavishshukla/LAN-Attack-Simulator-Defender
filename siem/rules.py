SIEM_RULES = {
    4625: {
        "name": "FAILED_LOGON",
        "severity": "HIGH",
        "description": "A Windows authentication failure was recorded.",
    },
    4688: {
        "name": "PROCESS_CREATED",
        "severity": "LOW",
        "description": "A new process creation event was recorded.",
    },
    7045: {
        "name": "SERVICE_INSTALLED",
        "severity": "HIGH",
        "description": "A Windows service installation event was recorded.",
    },
    1102: {
        "name": "AUDIT_LOG_CLEARED",
        "severity": "CRITICAL",
        "description": "The Windows Security audit log was cleared.",
    },
}


def classify(event):
    rule = SIEM_RULES.get(event["event_id"])
    if not rule:
        return None

    return {
        **event,
        "rule": rule["name"],
        "severity": rule["severity"],
        "description": rule["description"],
    }
