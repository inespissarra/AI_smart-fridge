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
import os
import machine
import network
import socket
import time


def connect_to_wifi():
    SSID='NOS-FFFC'
    KEY='MRZ2Q2NH'

    print ("Trying to connect. Note this may take a while...")
    wlan = network.WLAN(network.STA_IF)
    wlan.deinit()
    wlan.active(True)
    wlan.connect(SSID, KEY)

def detect_motion():
    sensor.snapshot().save("temp/bg.bmp")
    diff = 20  # We'll say we detected motion after 10 frames of motion.

    while diff:
        img = sensor.snapshot()
        img.difference("temp/bg.bmp")
        stats = img.statistics()
        if stats[5] > 30:
            diff -= 1


def SendImage(img):
    s = socket.socket()
    s.connect(("192.168.1.12", 8080))  # Replace with Raspberry Pi's IP address

    # Convert image to JPEG
    img = img.compressed(quality=100)

    # Send image size
    s.sendall(len(img).to_bytes(4, 'big'))

    # Send image data
    s.sendall(img)

    # Close the socket
    s.close()

connect_to_wifi()

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
sensor.set_auto_whitebal(False)  # Turn off white balance.

led = machine.LED("LED_RED")
led2 = machine.LED("LED_GREEN")
led3 = machine.LED("LED_BLUE")

if not "temp" in os.listdir():
    os.mkdir("temp")  # Make a temp directory

sensor.snapshot().save("temp/bg.bmp")

while True:
    sensor.skip_frames(time=2000)  # Give the user time to get ready.

    print("waiting for motion")
    led2.on()
    detect_motion()
    print("motion detected")
    led2.off()
    time.sleep(3)

    led.on()
    print("Movement detected! Saving image...")
    img = sensor.snapshot()
    SendImage(img)
    img.save("temp/snapshot.jpg")
    led.off()

    print("waiting for motion")
    led3.on()
    detect_motion()
    led3.off()
    time.sleep(3)
