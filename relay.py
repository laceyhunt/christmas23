
# SAMPLE DEMO FOR FINAL PRESENTATION

import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
RELAY_PINS = [17, 18, 27, 22, 23, 24, 25, 4]

# Set as output and turn off
for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

try:
    while True:
        # Turn on each relay channel for 1 second and then turn it off
        for pin in RELAY_PINS:
            GPIO.output(pin, GPIO.LOW)
            time.sleep(1)
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(1)

# Handle keyboard interrupt (e.g., Ctrl+C) to ensure GPIO cleanup
except KeyboardInterrupt:
    GPIO.cleanup()
