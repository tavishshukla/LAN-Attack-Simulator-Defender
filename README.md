# LAN Attack Simulator + Defender

An educational LAN cybersecurity lab that simulates suspicious network activity and demonstrates defensive detection, alerting, incident management, and simulated response.

**Safety:** this project does not perform real attacks. It uses local event simulation and an application-level response model.

## Architecture

Simulator -> Event Pipeline -> Detection Rules -> Alerts -> Incidents -> Simulated Response -> SQLite -> Rich Dashboard

## Features

- Port-scan pattern simulation
- Connection-burst simulation
- Failed-login simulation
- HTTP-request burst simulation
- Sliding-window detection
- Configurable thresholds and severity
- SQLite event, alert, and incident history
- Rich terminal output
- Automated tests

## Setup

Requires Python 3.11+.

    python -m venv .venv
    pip install -r requirements.txt

Windows activation: `.venv\Scripts\activate`
Linux/macOS: `source .venv/bin/activate`

## Usage

    python main.py lab
    python main.py simulator
    python main.py incidents
    python main.py stats
    python main.py config\n    python main.py web\n\nThen open http://127.0.0.1:5000 in your browser. The web dashboard is local-only and the button runs the same safe simulated lab.

The first run creates `data/lab.db`.

## Detection rules

| Rule | Default | Severity |
|---|---|---|
| PORT_SCAN_01 | 10 unique ports / 5s | HIGH |
| CONNECTION_BURST_01 | 30 connections / 5s | MEDIUM |
| FAILED_LOGIN_01 | 5 failures / 30s | HIGH |
| HTTP_BURST_01 | 50 requests / 10s | MEDIUM |

Thresholds live in `config/config.json`.

## Testing

    pytest

## Security model

No password cracking, Wi-Fi attacks, ARP poisoning, credential theft, malware, exploitation, DDoS, stealth/evasion, packet interception, or real firewall changes are implemented. The simulator is designed for defensive cybersecurity education.

## Future improvements

- Dockerized multi-host lab
- Web dashboard
- PCAP replay
- Network topology visualization
- Additional detection rules
- SIEM integration
- ML anomaly detection
