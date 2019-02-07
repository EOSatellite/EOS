import binascii
import sys
import re
import argparse

parser = argparse.ArgumentParser(description="rebuild a file from a hexdump")

parser.add_argument("filename", type=str, help="hexdump file")
parser.add_argument("output", type=str, help="output file")

args = parser.parse_args()

f = open(args.filename, "rb")
data = f.readlines()
data = re.findall("..", "".join([d.decode().strip() for d in data]))
f.close()

f = open(args.output, "wb")
for d in data:
    f.write(binascii.unhexlify(d))
f.close()
