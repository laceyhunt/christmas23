# 
#   nativity.py
#       handles all GPIO (light and audio) stuff for nativity
#   Lacey Hunt
#   2023
#
#   Lights and Audio are run in their own respective threads, initialized in this file
# 
#   if state is 2 then initialize Nativity lights and audio
#   else standby
# 

import RPi.GPIO as GPIO
import pygame
import time
import threading

# event to trigger proper stop of nativity lights and audio
stop_event = threading.Event()

# threads for Nativity lights and audio
audio_thread = None
lights_thread = None

# audio to play with lights
audio_file = "ChristmasTrain2.mp3"  
lightsOff=True

# Set up GPIO
GPIO.setmode(GPIO.BCM)
RELAY_PINS = [17, 18, 27, 22, 23, 24, 25, 4]
for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)

# 
# lights_off()->None
#   set all GPIO pins in RELAY_PINS to off
#
def lights_off():
    for pin in RELAY_PINS:
        GPIO.output(pin, GPIO.HIGH)
    lightsOff=True
lights_off()

# 
# play_audio(string)->None
#   initialzes mixer and plays audio while stop_event is not set
# 
def play_audio(file_path):

    # start mixer
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # play while audio is still going and stop_event is not set
    while pygame.mixer.music.get_busy() and not stop_event.is_set():
        pygame.time.Clock().tick(30)

    # quit
    pygame.mixer.quit()
    print("Nativity Sound stopped.")

# 
# nativity_lights()->None
#   control nativity lights while stop_event is not set
#   
def nativity_lights():
    global lightsOff
    # light control loop
    while not stop_event.is_set():
        lightsOff=False
        print("star")
        # star
        GPIO.output(RELAY_PINS[7], GPIO.LOW)
        if stop_event.is_set():
                break
        time.sleep(27.95)

        print("donkey")
        # donkey
        GPIO.output(RELAY_PINS[6], GPIO.LOW)
        if stop_event.is_set():
                break
        time.sleep(11.12)

        print("camel")
        # camel
        GPIO.output(RELAY_PINS[5], GPIO.LOW)
        if stop_event.is_set():
                break
        time.sleep(4.66)

        print("lamb")
        # lamb
        GPIO.output(RELAY_PINS[4], GPIO.LOW)
        if stop_event.is_set():
                break
        time.sleep(5.73)

        print("cow")
        # cow
        GPIO.output(RELAY_PINS[3], GPIO.LOW)
        if stop_event.is_set():
                break
        time.sleep(5.5)

        print("wisemen")
        # wisemen
        GPIO.output(RELAY_PINS[2], GPIO.LOW)
        if stop_event.is_set():
                break
        time.sleep(9)

        print("joseph and mary")
        # joseph and mary
        GPIO.output(RELAY_PINS[1], GPIO.LOW)
        GPIO.output(RELAY_PINS[0], GPIO.LOW)
        time.sleep(65)
        stop_event.set()
    
    # turn off lights
    print("Nativity Lights Stopped.")

# 
# start_nativity_threads()->Tuple[Thread, Thread]
#   clear stop_event then initialize then start new light and audio threads
#   
def start_nativity_threads():
    global audio_thread, lights_thread, stop_event

    # clear stop_event so threads can run
    stop_event.clear()

    # initialize and start threads
    # audio_thread = threading.Thread(target=play_audio, args=(audio_file,))
    lights_thread = threading.Thread(target=nativity_lights)
    # audio_thread.start()
    lights_thread.start()

    # return audio_thread,lights_thread
    return lights_thread


# 
# stop_nativity_threads()->None
#   set stop_event and join threads
#   
def stop_nativity_threads():
    global audio_thread, lights_thread, stop_event

    # stop currently running threads
    stop_event.set()

    # join threads if they exist
    # if audio_thread is not None:
    #     audio_thread.join()
    if lights_thread is not None:
        lights_thread.join()