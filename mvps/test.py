#!/usr/bin/env python3

# Open Pixel Control client: All lights to solid white
import json,math
import numpy as np
import opc, time

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

numLEDs = 256
client = opc.Client('localhost:7890')

# Start with Setting them to black
pixelColors = [(0,0,0)]*numLEDs
radius = 8.0
c = 0.0
colorRange = 60
dir = 1

while True:
    # Reset Color
    pixelColors = [(20-math.pow(abs(math.sin(c)),5)*20,0,0)]*numLEDs
    client.put_pixels(pixelColors)
