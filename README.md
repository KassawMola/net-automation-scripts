# Net Automation Scripts

Reusable Python utilities for network operations labs and demo environments. The scripts are written for safe portfolio use: devices are loaded from a sample inventory, credentials are demo-only, and no customer names or production addresses are included.

## What is included

| Script | Purpose |
| --- | --- |
| `send_commands_to_switches.py` | Send one or more CLI commands to devices over SSH. |
| `backup_configs.py` | Collect running configuration output and save it locally. |
| `check_port_status.py` | Capture interface status output for quick operational checks. |
| `upgrade_switch_ftp.py` | Demonstrate an image copy and reload workflow using a lab upgrade path. |

## Demo inventory

The repository uses `assets/sample_devices.csv` for demo input.

```csv
host,ip,username,password,platform
catalyst-demo-01,192.168.1.1,admin,admin123!,cisco_ios
```

`admin/admin123!` and `192.168.1.1` are included only as lab/demo values. Replace them before using the scripts in any real environment.

## Quick start

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python send_commands_to_switches.py
```

## Notes

- Keep production hostnames, addresses, passwords, and customer details out of the repository.
- Store sensitive values in a secrets manager or environment-specific inventory file.
- Use these scripts as portfolio-safe examples for NetOps and SecOps automation.

Created by Kassaw Mola.
