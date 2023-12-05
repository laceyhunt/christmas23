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

def nativity_lights():
    global running
    try:
        while running:
            # star
            GPIO.output(RELAY_PINS[7], GPIO.LOW)
            # donkey
            time.sleep(27.95)
            GPIO.output(RELAY_PINS[6], GPIO.LOW)
            # camel
            time.sleep(11.12)
            GPIO.output(RELAY_PINS[5], GPIO.LOW)
            # lamb
            time.sleep(4.66)
            GPIO.output(RELAY_PINS[4], GPIO.LOW)
            # cow
            time.sleep(5.73)
            GPIO.output(RELAY_PINS[3], GPIO.LOW)
            # wisemen
            time.sleep(5.5)
            GPIO.output(RELAY_PINS[2], GPIO.LOW)
            # joseph and mary
            time.sleep(2.79)
            GPIO.output(RELAY_PINS[1], GPIO.LOW)
            # jesus
            time.sleep(6.54)
            GPIO.output(RELAY_PINS[0], GPIO.LOW)
            time.sleep(125.71)
    finally:
        for pin in RELAY_PINS:
                GPIO.output(pin, GPIO.HIGH)


def signal_handler(signal,frame):
    global running
    running=False
    sys.exit(0)

if __name__ == "__main__":
    try:
        mp3_file = "ChristmasTrain2.mp3"  # Replace with the path to your MP3 file
        audio_thread = threading.Thread(target=play_mp3, args=(mp3_file,))
        lights_thread = threading.Thread(target=nativity_lights)
        
        audio_thread.start()
        lights_thread.start()
        
        signal.signal(signal.SIGINT,signal_handler)

        audio_thread.join()

    except KeyboardInterrupt:
        print("Script interrupted")
        for pin in RELAY_PINS:
                GPIO.output(pin, GPIO.HIGH)
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        running = False  # Stop the lights thread
        lights_thread.join()  # Wait for the lights thread to finish
        # audio_thread.join()  # Wait for the audio thread to finish
        GPIO.cleanup()# Clean up GPIO
        
        