# 🛠️ Net Automation Scripts

This repository includes a set of useful scripts to automate daily networking and security tasks.  
Ideal for managing Cisco switches, FortiGate firewalls, and general network diagnostics.

## 📌 Included Scripts

- **cisco_backup.py** – Automatically connect to Cisco switches and download configurations.
- **fortigate_monitor.py** – Query CPU, session and interface status from FortiGate firewalls.
- **ping_sweep.py** – Scan a subnet for live hosts and output the results.
- **port_checker.py** – Check open TCP/UDP ports on target devices.
- **switch_reboot.py** – Schedule or trigger remote reboots for network switches.

## 🚀 Usage

```bash
python cisco_backup.py
python fortigate_monitor.py
python ping_sweep.py
```

> Make sure you have Python 3.7+ and install dependencies with:
```bash
pip install -r requirements.txt
```

## 📂 Requirements

- `netmiko`
- `paramiko`
- `pythonping`
- `requests`

## 🔐 Notes
Make sure to update IP addresses, credentials, and paths inside each script to match your environment.

---
Created by Kassaw Mola – Senior Network & Security Engineer
