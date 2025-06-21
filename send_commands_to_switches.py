import paramiko
import csv
import os
from datetime import datetime

DEVICES_FILE = "assets/sample_devices.csv"
COMMANDS_FILE = "assets/commands.txt"
OUTPUT_FOLDER = "outputs"

def read_devices(file_path):
    devices = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            devices.append(row)
    return devices

def read_commands(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def send_commands(device, commands):
    ip = device["ip"]
    username = device["username"]
    password = device["password"]

    print(f"[+] Connecting to {ip}")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=username, password=password, look_for_keys=False)

        shell = client.invoke_shell()
        output = ""

        for cmd in commands:
            shell.send(cmd + "\n")
            while not shell.recv_ready():
                pass
            output += shell.recv(9999).decode()

        client.close()
        return output

    except Exception as e:
        return f"[!] Failed to connect to {ip}: {str(e)}"

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    devices = read_devices(DEVICES_FILE)
    commands = read_commands(COMMANDS_FILE)

    for device in devices:
        ip = device["ip"]
        result = send_commands(device, commands)

        with open(f"{OUTPUT_FOLDER}/output_{ip}_{timestamp}.txt", "w") as f:
            f.write(result)
        print(f"[✓] Output saved for {ip}")

if __name__ == "__main__":
    main()
    
