#!/usr/bin/env python3
'''
bmpsnap.py : save a single frame of BMP data from Arducam Mini

Copyright (C) Simon D. Levy 2017

This file is part of BreezyArduCAM.

BreezyArduCAM is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
BreezyArduCAM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with BreezyArduCAM.  If not, see <http://www.gnu.org/licenses/>.
'''
import subprocess
import time
import serial
from sys import stdout

from helpers import *
from detection import *

# Modifiable params -------------------------------------------------------------------

# PORT = '/dev/ttyACM0' # Ubuntu
# PORT = 'COM9'         # Windows
CAMERA_PORT = '/dev/tty.usbmodem144101'
SENSOR_PORT = '/dev/tty.usbmodem14301'

CAMERA_BAUD = 921600
SENSOR_BAUD = 9600

OUTFILENAME = 'test.bmp'


# helpers  --------------------------------------------------------------------------

def num2bytes(n):
    return [n & 0xFF, (n >> 8) & 0xFF, (n >> 16) & 0xFF, (n >> 24) & 0XFF]


def dump(msg):
    stdout.write(msg)
    stdout.flush()


# BMP header for 320x240 image ------------------------------------------------------
# See: http://www.fastgraph.com/help/bmp_header_format.html
# See: https://upload.wikimedia.org/wikipedia/commons/c/c4/BMPfileFormat.png
header = [
    0x42, 0x4D,  # signature, must be 4D42 hex
    0x36, 0x58, 0x02, 0x00,  # size of BMP file in bytes (unreliable)
    0x00, 0x00,  # reserved, must be zero
    0x00, 0x00,  # reserved, must be zero
    0x42, 0x00, 0x00, 0x00,  # offset to start of image data in bytes
    0x28, 0x00, 0x00, 0x00,  # size of BITMAPINFOHEADER structure, must be 40
    0x40, 0x01, 0x00, 0x00,  # image width in pixels
    0xF0, 0x00, 0x00, 0x00,  # image height in pixels
    0x01, 0x00,  # number of planes in the image, must be 1
    0x10, 0x00,  # number of bits per pixel
    0x03, 0x00, 0x00, 0x00,  # compression type
    0x00, 0x58, 0x02, 0x00,  # size of image data in bytes (including padding)
    0xC4, 0x0E, 0x00, 0x00,  # horizontal resolution in pixels per meter (unreliable)
    0xC4, 0x0E, 0x00, 0x00,  # vertical resolution in pixels per meter (unreliable)
    0x00, 0x00, 0x00, 0x00,  # number of colors in image, or zero
    0x00, 0x00, 0x00, 0x00,  # number of important colors, or zero
    0x00, 0xF8, 0x00, 0x00,  # red channel bitmask
    0xE0, 0x07, 0x00, 0x00,  # green channel bitmask
    0x1F, 0x00, 0x00, 0x00  # blue channel bitmask
]

# main ------------------------------------------------------------------------------
MIN_DISTANCE_TO_ALERT = 10


def audio_output(content):
    subprocess.call(["say", content])


def handle_camera_output(line):
    if cameraAck == 'capture enabled\r\n':
        print(cameraAck)
        # Send "start capture" message
        sendbyte(cameraPort, 1)

        dump('\nWriting file %s (may appear upside-down) ...' % OUTFILENAME)

        # Open output file
        outfile = open(OUTFILENAME, 'wb')

        # Write BMP header
        outfile.write(bytearray(header))

        # Read bytes from serial and write them to file
        for k in range(320 * 240):
            c = outfile.write(cameraPort.read(2))

        # Send "stop" message
        sendbyte(cameraPort, 0)

        # Close output file
        outfile.close()

        print('\nDone')

        detections = detect(OUTFILENAME)
        objects = ','.join(eachObject['name'] for eachObject in detections)
        if not len(objects):
            audio_output('Nothing in front of you')
        else:
            audio_output('{} in front of you'.format(objects))


def handle_sensor_output(line):
    if not len(line):
        return

    try:
        sensors = sensorAck.split(";")
    except IOError as e:
        return

    if len(sensors) < 2:
        return
    left, right = int(sensors[0]), int(sensors[1])
    print("left", left, "right", right)
    if left < MIN_DISTANCE_TO_ALERT and right < MIN_DISTANCE_TO_ALERT:
        audio_output("Obstacle on both sides")
    elif left < MIN_DISTANCE_TO_ALERT:
        audio_output("Obstacle on your left")
    elif right < MIN_DISTANCE_TO_ALERT:
        audio_output("Obstacle on your right")


if __name__ == '__main__':

    # Open connection to Arduino with a timeout of two seconds
    cameraPort = serial.Serial(CAMERA_PORT, CAMERA_BAUD, timeout=2)
    sensorPort = serial.Serial(SENSOR_PORT, SENSOR_BAUD, timeout=2)

    dump('Starting capture ...')

    # Report acknowledgment from camera
    getack(cameraPort)

    # Wait a spell
    time.sleep(0.2)

    while True:
        # getack(sensorPort)
        cameraAck = cameraPort.readline().decode()
        # sensorAck = sensorPort.readline().decode()

        # handle_sensor_output(sensorAck)
        handle_camera_output(cameraAck)