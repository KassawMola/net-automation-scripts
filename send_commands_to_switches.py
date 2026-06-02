import csv
import os
import time
from datetime import datetime
from pathlib import Path

import paramiko


DEVICES_FILE = Path("assets/sample_devices.csv")
COMMANDS_FILE = Path("assets/commands.txt")
OUTPUT_FOLDER = Path("outputs")


def read_devices(file_path):
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def read_commands(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def safe_name(value):
    return "".join(char if char.isalnum() or char in ("-", "_") else "_" for char in value)


def send_commands(device, commands):
    host = device["host"]
    target = device.get("ip") or host
    username = device["username"]
    password = device["password"]

    print(f"[+] Connecting to {host} ({target})")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(target, username=username, password=password, look_for_keys=False)
        shell = client.invoke_shell()
        output = ""

        for command in commands:
            shell.send(command + "\n")
            time.sleep(1)
            while shell.recv_ready():
                output += shell.recv(9999).decode(errors="replace")

        return output
    except Exception as exc:
        return f"[!] Failed to connect to {host} ({target}): {exc}"
    finally:
        client.close()


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    devices = read_devices(DEVICES_FILE)
    commands = read_commands(COMMANDS_FILE)

    for device in devices:
        host = device["host"]
        result = send_commands(device, commands)
        output_file = OUTPUT_FOLDER / f"output_{safe_name(host)}_{timestamp}.txt"
        output_file.write_text(result, encoding="utf-8")
        print(f"[+] Output saved for {host}")


if __name__ == "__main__":
    main()
