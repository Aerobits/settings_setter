import argparse
import yaml
import serial
from typing import Dict
import sys
from time import sleep

argparse = argparse.ArgumentParser(
    prog="Aerobits settings setter",
    description="Automatically program Aerobits devices"
    "with configuration described in .yaml",
)

argparse.add_argument("-p", "--port", help="Device port", required=True)

argparse.add_argument("-f", "--file", help="Input yaml with settings", required=True)

argparse.add_argument("-b", "--baud", help="Desired baudrate", default=115200)

args = argparse.parse_args()

config: Dict
try:
    with open(args.file) as stream:
        config = yaml.safe_load_all(stream)
        config = list(
            config
        )  # coerce generator evaluation so that stream can be closed
except FileNotFoundError:
    print(f"Requested file {args.file} could not be found", file=sys.stderr)
    sys.exit(1)

# destructure the dict
config = config[0]
dev_settings = config[list(config.keys())[0]]


def device_read(device: serial.Serial):
    line = b""
    while line == b"":
        line = device.read_all()

    device.read_all()
    return line


with serial.Serial(
    port=args.port, baudrate=args.baud, bytesize=8, parity="N", timeout=0.3
) as device:
    device.read_all()
    device.write("AT+CONFIG=1\n".encode("ASCII"))
    # clear the read buffer
    device.read_all()

    for setting, setting_value in dev_settings.items():
        command = f"AT+{setting}"

        command += f"={setting_value}" if setting_value is not None else ""
        command += "\r\n"
        command = command.encode(encoding="ASCII")

        print(f"Transmit: {command}", file=sys.stderr)
        device.write(command)
        print(f"Response: {device_read(device)}", file=sys.stderr)

    device.read_all()
    device.write("AT+SETTINGS?\n".encode("ASCII"))
    sleep(0.2)
    print(device_read(device).decode("ASCII").removeprefix("AT+OK"))
    device.write("AT+CONFIG=0\n".encode("ASCII"))

print("Done.", file=sys.stderr)
