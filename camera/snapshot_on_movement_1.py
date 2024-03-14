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
    SSID='iPhone de Inês (2)'
    KEY='odiogoelindo'

    print ("Trying to connect. Note this may take a while...")
    wlan = network.WLAN(network.STA_IF)
    wlan.deinit()
    wlan.active(True)
    wlan.connect(SSID, KEY)

def detect_motion():
    old = sensor.snapshot().save("temp/image.bmp")
    diff = 5  # We'll say we detected motion after 10 frames of motion.

    while diff:
        img = sensor.snapshot()
        img.difference("/temp/image.bmp")
        stats = img.statistics()
        if stats[5] > 50:
            diff -= 1

def wait_for_no_motion():
    old = sensor.snapshot()

    diff = 5
    while diff:
        img = sensor.snapshot()
        img.difference(old)
        stats = img.statistics()
        if stats[5] < 100:
            diff -= 1
        else:
            diff = 10
            old = img


def SendImage(img):
    s = socket.socket()
    s.connect(("172.20.10.7", 8080))  # Replace with Raspberry Pi's IP address

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
    sensor.skip_frames(time=2000)  # Give the user time to get ready.

    print("waiting for motion")
    detect_motion()
    print("waiting for no motion")
    wait_for_no_motion()

    led.on()
    print("Movement detected! Saving image...")
    img = sensor.snapshot()
    SendImage(img)
    led.off()

    print("waiting for motion")
    detect_motion()
    print("waiting for no motion")
    wait_for_no_motion()
