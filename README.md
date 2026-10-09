# LAN Attack Simulator + Defender

A safe educational cybersecurity lab that simulates suspicious LAN activity, detects it, creates alerts/incidents, and demonstrates defensive response. It also includes read-only local network monitoring and a local Windows Event Log SIEM.

> **Safety:** This project is defensive and educational. The simulator does not perform real attacks, password cracking, Wi-Fi attacks, ARP poisoning, credential theft, malware, exploitation, DDoS, packet interception, or real firewall changes.

## What this project does

The project has several modes:

- **Lab:** runs the complete safe simulation pipeline.
- **Simulator:** lets you choose individual simulated events.
- **Monitor:** observes real network connections on your own computer in read-only mode.
- **SIEM:** reads supported Windows Event Logs locally.
- **Web dashboard:** shows events/incidents in a browser.
- **Incidents/Stats:** displays stored security information.
- **Config:** prints the current detection configuration.

## Requirements

- Windows, Linux, or macOS
- Python **3.11 or newer**
- Git
- Internet access for the initial package installation

## 1. Install Python

### Windows

Download Python from the official Python website:

https://www.python.org/downloads/

During installation, **check "Add Python to PATH"** before clicking Install.

Open a new Command Prompt and check:

```bat
python --version
```

You should see Python 3.11 or newer.

If `python` does not work, try:

```bat
py --version
```

### Linux/macOS

Check:

```bash
python3 --version
```

Install Python 3.11+ using your operating system's normal package manager if necessary.

## 2. Install Git

Download Git from:

https://git-scm.com/downloads

After installation, open a new terminal and run:

```bash
git --version
```

## 3. Clone the repository

Open Command Prompt, PowerShell, Terminal, or Git Bash.

Run:

```bash
git clone https://github.com/tavishshukla/LAN-Attack-Simulator-Defender.git
```

Enter the project folder:

```bash
cd LAN-Attack-Simulator-Defender
```

## 4. Create a virtual environment

### Windows

```bat
python -m venv .venv
.venv\\Scripts\\activate
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

When the virtual environment is active, you should normally see `.venv` in your terminal prompt.

## 5. Install the dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Then install the project packages:

```bash
python -m pip install -r requirements.txt
```

> You normally do **not** need to download pip separately. Modern Python installations include pip.

## 6. Run the safe cybersecurity lab

Run:

```bash
python main.py lab
```

This generates harmless simulated security events and sends them through the detection pipeline.

## 7. Run the interactive simulator

Run:

```bash
python main.py simulator
```

You will get a menu similar to:

```
1. Port Scan
2. Connection Burst
3. Failed Login
4. HTTP Burst
```

Choose one, or choose `a` to run all simulations.

## 8. Run the real local network monitor

Run:

```bash
python main.py monitor
```

This mode uses read-only local connection telemetry. It does **not** attack anything or modify your network.

Press:

```
Ctrl+C
```

to stop it.

## 9. Run the Windows Event Log SIEM

On Windows, run:

```bash
python main.py siem
```

The SIEM is designed to inspect local Windows Security/System/Application event logs.

Some Windows event logs may require elevated permissions. If access is denied, close the program and retry from an appropriately authorized terminal.

## 10. Run the web dashboard

Start it with:

```bash
python main.py web
```

You should see Flask start on:

```
http://127.0.0.1:5000
```

Open that address in your browser.

The dashboard is intentionally bound to `127.0.0.1`, so it is local-only.

Stop it with:

```
Ctrl+C
```

## 11. View incidents

```bash
python main.py incidents
```

## 12. View statistics

```bash
python main.py stats
```

## 13. View configuration

```bash
python main.py config
```

Detection thresholds are stored in:

```
config/config.json
```

## 14. Run the tests

Make sure the virtual environment is active, then run:

```bash
python -m pytest
```

## Detection rules

| Rule | Default threshold | Severity |
|---|---:|---|
| PORT_SCAN_01 | More than 10 unique ports / 5 seconds | HIGH |
| CONNECTION_BURST_01 | More than 30 connections / 5 seconds | MEDIUM |
| FAILED_LOGIN_01 | More than 5 failures / 30 seconds | HIGH |
| HTTP_BURST_01 | More than 50 requests / 10 seconds | MEDIUM |

## Project structure

```
lan-attack-sim/
├── main.py
├── requirements.txt
├── config/
├── simulator/
├── defender/
├── dashboard/
├── database/
├── core/
├── monitor/
├── siem/
├── webapp/
└── tests/
```

## Data files

The application creates local runtime data such as:

```
data/lab.db
```

This contains the local event, alert, and incident history.

## Troubleshooting

### "python is not recognized"

Reinstall Python and enable **Add Python to PATH**, then open a new terminal.

### "pip is not recognized"

Use:

```bash
python -m pip --version
```

Then install packages with:

```bash
python -m pip install -r requirements.txt
```

### "No module named flask" or another missing module

Make sure the virtual environment is activated and run:

```bash
python -m pip install -r requirements.txt
```

### Git says the repository already exists

You may already have the project. Enter it with:

```bash
cd LAN-Attack-Simulator-Defender
```

## Security model

This project is intentionally limited to defensive education and authorized local monitoring. Do not point the simulator or any future modifications at systems you do not own or have permission to test.
