import pygame
import RPi.GPIO as GPIO
import time
import threading
import sys
import signal

# Set up GPIO
GPIO.setmode(GPIO.BCM)
RELAY_PINS = [17, 18, 27, 22, 23, 24, 25, 4]

# Set as output and turn off
for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

running = True

def play_mp3(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Wait for the audio to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(30)  # Adjust the tick rate as needed
    pygame.mixer.quit()
    for pin in RELAY_PINS:
            GPIO.output(pin, GPIO.HIGH)

def nativity_lights():
    time.sleep(14)
    GPIO.output(RELAY_PINS[7], GPIO.LOW)
    time.sleep(14)
    GPIO.output(RELAY_PINS[6], GPIO.LOW)
    time.sleep(11)
    GPIO.output(RELAY_PINS[5], GPIO.LOW)
    time.sleep(6)
    GPIO.output(RELAY_PINS[4], GPIO.LOW)
    time.sleep(6)
    GPIO.output(RELAY_PINS[3], GPIO.LOW)
    time.sleep(3)
    GPIO.output(RELAY_PINS[2], GPIO.LOW)
    time.sleep(8)
    GPIO.output(RELAY_PINS[1], GPIO.LOW)
    time.sleep(14)
    GPIO.output(RELAY_PINS[0], GPIO.LOW)

def signal_handler(signal,frame):
    global running
    running=False
    sys.exit(0)

if __name__ == "__main__":
    try:
        mp3_file = "ChristmasTrain2.mp3"  # Replace with the path to your MP3 file
        audio_thread = threading.Thread(target=play_mp3, args=(mp3_file,))
        lights_thread = threading.Thread(target=nativity_lights)
        
        lights_thread.start()
        audio_thread.start()

        signal.signal(signal.SIGINT,signal_handler)

        lights_thread.join()
    except KeyboardInterrupt:
        print("Script interrupted")
        GPIO.cleanup()
    finally:
        running = False  # Stop the audio thread
        audio_thread.join()  # Wait for the audio thread to finish