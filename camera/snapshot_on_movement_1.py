# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# Snapshot on Movement Example
#
# Note: You will need an SD card to run this example.
#
# This example demonstrates using frame differencing with your OpenMV Cam to do
# motion detection. After motion is detected your OpenMV Cam will take picture.

import sensor
import random
import os
import machine
import network
import socket


def connect_to_wifi():
    SSID='NOS-FFFC'
    KEY='MRZ2Q2NH'

    print ("Trying to connect. Note this may take a while...")
    wlan = network.WLAN(network.STA_IF)
    wlan.deinit()
    wlan.active(True)
    wlan.connect(SSID, KEY)


def SendImage(img):
    s = socket.socket()
    s.connect(("192.168.1.254", 8080))  # Replace with Raspberry Pi's IP address

    # Convert image to JPEG
    img_compressed = img.compressed(quality=50)

    # Send image size
    s.send(str(len(img_compressed)))

    # Send image data
    s.send(img_compressed)

    # Close the socket
    s.close()

connect_to_wifi()

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
sensor.set_auto_whitebal(False)  # Turn off white balance.

led = machine.LED("LED_RED")

if not "temp" in os.listdir():
    os.mkdir("temp")  # Make a temp directory

while True:
    print("About to save background image...")
    sensor.skip_frames(time=2000)  # Give the user time to get ready.

    sensor.snapshot().save("temp/bg.bmp")
    print("Saved background image - Now detecting motion!")

    diff = 10  # We'll say we detected motion after 10 frames of motion.
    while diff:
        img = sensor.snapshot()
        img.difference("temp/bg.bmp")
        stats = img.statistics()
        # Stats 5 is the max of the lighting color channel. The below code
        # triggers when the lighting max for the whole image goes above 20.
        # The lighting difference maximum should be zero normally.
        if stats[5] > 20:
            diff -= 1

    led.on()
    print("Movement detected! Saving image...")
    sensor.snapshot().save("temp/snapshot-%d.jpg" % random.getrandbits(32))  # Save Pic.
    img = sensor.snapshot()

    SendImage(img)

    led.off()
