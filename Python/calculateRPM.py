from __future__ import print_function
import argparse
import re
import matplotlib.pyplot as plt
from serial import Serial
from time import sleep
import numpy

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=str, nargs="?", default="/dev/ttyACM0")
parser.add_argument("-b", "--baud", type=int, nargs="?", default=57600)
args = parser.parse_args()

def read_serial():
    """
    Read the serial port to capture the FG input data
    """
    try:
        ser = Serial(args.port, args.baud)
    except Exception as e:
        print("Ccould not connect to", args.port)
        print(e)
        exit(1)

    data = []
    for i in range(250):
        line = ser.readline().decode().strip().split()
        if len(line) is 2: data.append(line)

    return data

def parse_data(data):
    """
    Parse the data into a usable format for the `get_rpm` function
    """
    if data is None: return

    xs = [int(d[0])/1000000 for d in data]
    ys = "".join([d[1] for d in data])

    y_splits = re.split(r'(?<=0)(?=1)|(?<=1)(?=0)', ys)
    x_splits = []

    i = 0
    while 1:
        try:
            x_splits.append(xs[:len(y_splits[i])])
            xs = xs[len(y_splits[i]):]
        except: break
        i += 1

    return [[x_splits[i], y_splits[i]] for i in range(len(x_splits))\
            if len(x_splits[i]) is not 1]

def get_rpm(data):
    try:
        for i in range(len(data)):
            Tstart = data[i][0][0]
            Tend = data[i + 3][0][-1]

            T = Tend - Tstart
            freq = 1/T
            rpm = (freq * 120) / 4

            if rpm <= 8000 and rpm >= 0:
                print(f"Hz = {round(freq, 2)}\trpm = {round(rpm, 2)}", end="\r")
    except: return

def update_line(hl, new_data):
    hl.set_xdata(numpy.append(hl.get_xdata(), new_data))
    hl.set_ydata(numpy.append(hl.get_ydata(), new_data))
    plt.draw()

def show_plot(data):
    """
    Graph the data to show the signal
    """
    ys = list("".join(d[1] for d in data))

    plt.plot(ys)
    plt.show()

while 1:
    data = parse_data(read_serial())
    #print("".join(d[1] for d in data))
    get_rpm(data)
