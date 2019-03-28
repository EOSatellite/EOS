import serial
import sys
import subprocess
import re
import math
import argparse
from time import sleep

# Setup program arguments
parser = argparse.ArgumentParser(description="send data to Arduino via serial connection")
parser.add_argument("filename", type=str, help="path to file that will be transmitted")
parser.add_argument("port", type=str, help="communication port of Arduino", nargs="?", default="/dev/ttyACM0")
parser.add_argument("baud", type=int, help="communication speed via serial", nargs="?", default=38400)

args = parser.parse_args()

# Try to connect to the Arduino
try:
    ser = serial.Serial(args.port, args.baud, timeout=0)
except:
    print(f"Error connecting to port {args.port}")
    exit(1)

print(f"Connection to {args.port} established")

# Create a hexdump of the input file
data = subprocess.check_output(["xxd", "-p", args.filename]).decode().strip()
# Create chunks of 6 (ex. ff12dc)
data = re.findall(".{1,6}", data)
# If the last value doesn't have 6, add padding
data[-1] = data[-1].ljust(6, '0')

# Wait for Arduino
sleep(2)

# Send each code in the data array
for d in range(len(data)):
    # Reset the buffer to avoid slowdown
    if d % 32 == 0:
        ser.reset_input_buffer()

    print(f"{math.ceil(d/len(data)*100)}%", ":: sending", data[d])
    ser.write(data[d].encode())
    sleep(0.1)

    # Send code `deadff` at the end to tell the receiver we are done sending
    if d == len(data) - 1:
        ser.write(b"deadff")
