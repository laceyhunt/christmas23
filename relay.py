import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
RELAY_PINS = [17, 18, 27, 22, 23, 24, 25, 4]  # Adjust these pins according to your setup

for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

try:
    while True:
        # Turn on each relay channel for 1 second and then turn it off
        for pin in RELAY_PINS:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(1)

except KeyboardInterrupt:
    # Handle keyboard interrupt (e.g., Ctrl+C) to ensure GPIO cleanup
    GPIO.cleanup()
