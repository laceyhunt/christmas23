import RPi.GPIO as GPIO
# import pygame
import time
import threading

GPIO.setmode(GPIO.BCM)

PIR_PIN = 14  # Adjust this pin according to your setup
RELAY_PINS = [17, 18, 27, 22, 23, 24, 25, 4]  # Adjust these pins according to your setup

for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
GPIO.setup(PIR_PIN, GPIO.IN)

# Function to control relays based on PIR sensor trigger
def control_relays():
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion detected!")
            for pin in RELAY_PINS:
                GPIO.output(pin, GPIO.LOW)
                print("Relay num %d", pin)
                time.sleep(.5)
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(.5)

        #     for pin in RELAY_PINS:
        #         GPIO.output(pin, GPIO.LOW)

            # time.sleep(2)  # Add a delay to prevent rapid re-triggering

        # time.sleep(0.1)  # Adjust the sleep time based on your needs

# Start a new thread for controlling relays
relay_thread = threading.Thread(target=control_relays)

try:
    # Start the relay control thread
    relay_thread.start()

    # Your main program can continue here
    while True:
        # Your main program logic goes here
        print("main function running...")
        time.sleep(10)
        pass

except KeyboardInterrupt:
    # Handle keyboard interrupt (e.g., Ctrl+C) to ensure GPIO cleanup
    GPIO.cleanup()