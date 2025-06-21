# 🛠️ Net Automation Scripts

This repository includes a set of useful scripts to automate daily networking and security tasks.  
Ideal for managing Cisco switches.

## 📌 Included Scripts

| Script Name                  | Purpose                                                                 |
|-----------------------------|-------------------------------------------------------------------------|
| `send_commands_to_switches.py` | Send one or more CLI commands to multiple network devices via SSH       |
| `backup_configs.py`         | Retrieve and save the `running-config` from each switch/router          |
| `check_port_status.py`      | Run `show interfaces status` or equivalent to check port statuses       |
| `upgrade_switch_ftp.py`     | Initiate image upgrade using a specified FTP path, followed by reload   |


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
