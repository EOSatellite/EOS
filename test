import serial
import sys
import subprocess
import re
import math
from time import sleep
import argparse

parser = argparse.ArgumentParser(description="send data to Arduino via serial connection")

parser.add_argument("filename", type=str, help="path to file that will be transmitted")
parser.add_argument("port", type=str, help="communication port of Arduino",
                    nargs="?", default="/dev/ttyACM0")
parser.add_argument("baud", type=int, help="communication speed via serial",
                    nargs="?", default=38400)

args = parser.parse_args()

ser = serial.Serial(args.port, args.baud, timeout=0)
print("Connection established")

data = subprocess.check_output(["xxd", "-p", args.filename]).decode().strip()
data = re.findall(".{1,6}", data)

print(data)

exit(0)

sleep(2)
for d in range(len(data)):
    if d % 32 == 0:
        ser.reset_input_buffer()

    print(f"{math.ceil(d/len(data)*100)}%", ":: sending", data[d])
    ser.write(data[d].encode())
    sleep(0.1)
