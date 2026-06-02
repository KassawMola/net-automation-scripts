import csv
import os
import time
from datetime import datetime
from pathlib import Path

import paramiko


DEVICES_FILE = Path("assets/sample_devices.csv")
UPGRADE_FILE = Path("assets/upgrade_image.txt")
OUTPUT_FOLDER = Path("outputs")


def read_devices(file_path):
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def read_upgrade_path(file_path):
    return file_path.read_text(encoding="utf-8").strip()


def safe_name(value):
    return "".join(char if char.isalnum() or char in ("-", "_") else "_" for char in value)


def upgrade_device(device, upgrade_path):
    host = device["host"]
    target = device.get("ip") or host
    username = device["username"]
    password = device["password"]

    print(f"[+] Starting demo upgrade workflow for {host} ({target})")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(target, username=username, password=password, look_for_keys=False)
        shell = client.invoke_shell()
        shell.send("terminal length 0\n")
        shell.send(f"copy {upgrade_path} flash:\n")
        shell.send("reload\n")
        time.sleep(2)

        output = ""
        while shell.recv_ready():
            output += shell.recv(65535).decode(errors="replace")

        return output
    except Exception as exc:
        return f"[!] Upgrade workflow failed on {host} ({target}): {exc}"
    finally:
        client.close()


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    upgrade_path = read_upgrade_path(UPGRADE_FILE)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    devices = read_devices(DEVICES_FILE)

    for device in devices:
        host = device["host"]
        result = upgrade_device(device, upgrade_path)
        output_file = OUTPUT_FOLDER / f"upgrade_{safe_name(host)}_{timestamp}.txt"
        output_file.write_text(result, encoding="utf-8")
        print(f"[+] Upgrade log saved for {host}")


if __name__ == "__main__":
    main()
