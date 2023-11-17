# Install the required Python libraries using the following command:
# pip install pygame RPi.GPIO
# Now, you can use the following Python script:

import RPi.GPIO as GPIO
import pygame
import time
import threading

# Set up GPIO
GPIO.setmode(GPIO.BCM)
PIR_PIN = 17  # Adjust this pin according to your setup
RELAY_PINS = [18, 27, 22, 23, 24, 25, 4, 5]  # Adjust these pins according to your setup

for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)
GPIO.setup(PIR_PIN, GPIO.IN)

# Load the audio file
audio_file = "your_audio_file.mp3"  # Replace with the path to your audio file

# Function to control relays based on PIR sensor trigger
def control_relays():
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion detected! Playing audio and activating relays.")
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            for pin in RELAY_PINS:
                GPIO.output(pin, GPIO.HIGH)

            time.sleep(pygame.mixer.music.get_length())  # Wait for audio to finish
            pygame.mixer.quit()

            for pin in RELAY_PINS:
                GPIO.output(pin, GPIO.LOW)

            time.sleep(2)  # Add a delay to prevent rapid re-triggering

        time.sleep(0.1)  # Adjust the sleep time based on your needs

# Start a new thread for controlling relays
relay_thread = threading.Thread(target=control_relays)

try:
    # Start the relay control thread
    relay_thread.start()

    # Your main program can continue here
    while True:
        # Your main program logic goes here
        pass

except KeyboardInterrupt:
    # Handle keyboard interrupt (e.g., Ctrl+C) to ensure GPIO cleanup
    GPIO.cleanup()