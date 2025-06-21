import paramiko
import csv
import os
from datetime import datetime

DEVICES_FILE = "assets/sample_devices.csv"
OUTPUT_FOLDER = "outputs"

def read_devices(file_path):
    devices = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            devices.append(row)
    return devices

def check_ports(device):
    ip = device["ip"]
    username = device["username"]
    password = device["password"]

    print(f"[+] Checking port status on {ip}")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password, look_for_keys=False)

        shell = client.invoke_shell()
        shell.send("terminal length 0\n")
        shell.send("show interfaces status\n")
        output = ""

        while not shell.recv_ready():
            pass
        output += shell.recv(65535).decode()

        client.close()
        return output

    except Exception as e:
        return f"[!] Error on {ip}: {str(e)}"

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    devices = read_devices(DEVICES_FILE)

    for device in devices:
        ip = device["ip"]
        result = check_ports(device)

        with open(f"{OUTPUT_FOLDER}/ports_{ip}_{timestamp}.txt", "w") as f:
            f.write(result)
        print(f"[✓] Port status saved for {ip}")

if __name__ == "__main__":
    main()
