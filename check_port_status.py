import csv
import os
import time
from datetime import datetime
from pathlib import Path

import paramiko


DEVICES_FILE = Path("assets/sample_devices.csv")
OUTPUT_FOLDER = Path("outputs")


def read_devices(file_path):
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def safe_name(value):
    return "".join(char if char.isalnum() or char in ("-", "_") else "_" for char in value)


def check_ports(device):
    host = device["host"]
    target = device.get("ip") or host
    username = device["username"]
    password = os.getenv(device.get("password_env", ""))
    if not password:
        return f"[!] Missing password environment variable for {host}"

    print(f"[+] Checking port status on {host} ({target})")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(target, username=username, password=password, look_for_keys=False)
        shell = client.invoke_shell()
        shell.send("terminal length 0\n")
        shell.send("show interfaces status\n")
        time.sleep(2)

        output = ""
        while shell.recv_ready():
            output += shell.recv(65535).decode(errors="replace")

        return output
    except Exception as exc:
        return f"[!] Error on {host} ({target}): {exc}"
    finally:
        client.close()


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    devices = read_devices(DEVICES_FILE)

    for device in devices:
        host = device["host"]
        result = check_ports(device)
        output_file = OUTPUT_FOLDER / f"ports_{safe_name(host)}_{timestamp}.txt"
        output_file.write_text(result, encoding="utf-8")
        print(f"[+] Port status saved for {host}")


if __name__ == "__main__":
    main()
