import paramiko
import csv
import os
from datetime import datetime

DEVICES_FILE = "assets/sample_devices.csv"
UPGRADE_FILE = "assets/upgrade_image.txt"
OUTPUT_FOLDER = "outputs"

def read_devices(file_path):
    devices = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            devices.append(row)
    return devices

def read_upgrade_command(file_path):
    with open(file_path, "r") as f:
        return f.read().strip()

def upgrade_device(device, upgrade_path):
    ip = device["ip"]
    username = device["username"]
    password = device["password"]

    print(f"[+] Upgrading {ip}")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password, look_for_keys=False)

        shell = client.invoke_shell()
        shell.send("terminal length 0\n")
        shell.send(f"copy {upgrade_path} flash:\n")
        shell.send("reload\n")

        output = ""
        while not shell.recv_ready():
            pass
        output += shell.recv(65535).decode()

        client.close()
        return output

    except Exception as e:
        return f"[!] Upgrade failed on {ip}: {str(e)}"

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    upgrade_path = read_upgrade_command(UPGRADE_FILE)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    devices = read_devices(DEVICES_FILE)

    for device in devices:
        ip = device["ip"]
        result = upgrade_device(device, upgrade_path)

        with open(f"{OUTPUT_FOLDER}/upgrade_{ip}_{timestamp}.txt", "w") as f:
            f.write(result)
        print(f"[✓] Upgrade log saved for {ip}")

if __name__ == "__main__":
    main()
