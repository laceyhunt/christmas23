import threading
import http.server
import socketserver
import urllib
import RPi.GPIO as GPIO
# from pygame import time
import pygame
import time

# LACEY
# If you run this script on the PI, and then send it a http request from a computer on the same network,
# You should see it return the value of "state" to the browser, and it should print out the value of
# "state" to the PI commandline.
# From the computer, you would format the http request like the following:
# http://<your pi's IP>:8000/?state=7

#  MY PI IP: 192.168.117.114/24

#
# Apologies if this is review, but the :8000 specifies the port, and the ?state=7 is just a
# "get" request which can be parsed out on the server side.
#
# There is another LACEY tag down in the pygame loop
#

# Global variable to hold the state value and server running flag
# "state_value" global allows us to be able to communicate from the server to the pygame loop running
state_value = None
running = True
stop_event = threading.Event()
audio_thread = None
lights_thread = None

# Set up GPIO
GPIO.setmode(GPIO.BCM)
RELAY_PINS = [17, 18, 27, 22, 23, 24, 25, 4]
# Set as output and turn off
for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

# Custom HTTP request handler
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global state_value

        # Parse query parameters
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        state = query_components.get("state", [""])[0]
       
        # Update the state value and prepare response text
        state_value = state
        response_text=bytes(str(state_value),'utf-8')

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response_text)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Just put this in here in case there is an exception and if there isn't good cleanup maybe we can restart the script without having to reboot.
    allow_reuse_address = True

# Start HTTP server in a separate thread so that it doesn't block the pygame stuff while waiting for http requests.
def start_server():
    global running
    with ThreadedTCPServer(("", 8000), CustomHandler) as httpd:
        print("Serving at port", 8000)
        while running:
            httpd.handle_request()
        print("Server closed")

# Start the server thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()



def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)

    while not stop_event.is_set():
        pygame.mixer.music.play()

        # Wait for the audio to finish
        while pygame.mixer.music.get_busy() and not stop_event.is_set():
            pygame.time.Clock().tick(30)  # Adjust the tick rate as needed
        pygame.mixer.quit()
    print("Nativity Sound stopped.")

def nativity_lights():
    while not stop_event.is_set():
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
    for pin in RELAY_PINS:
            GPIO.output(pin, GPIO.HIGH)
    print("Nativity Lights Stopped.")

def start_nativity_threads():
    global audio_thread, lights_thread, stop_event

    # allow threads to run
    stop_event.clear()

    # initialize and start lights and audio threads
    audio_thread = threading.Thread(target=play_audio, args=(audio_file,))
    lights_thread = threading.Thread(target=nativity_lights)
    audio_thread.start()
    lights_thread.start()

    return audio_thread,lights_thread

def stop_nativity_threads():
    global audio_thread, lights_thread, stop_event
    stop_event.set()
    if audio_thread is not None:
        audio_thread.join()
    if lights_thread is not None:
        lights_thread.join()

# Pygame loop - put all the normal PYGAME stuff in here
audio_file = "ChristmasTrain2.mp3"  
# clock = time.Clock()
try:
    state_value=None
    while True:
        # Run at 30 FPS
        # clock.tick(30)  # I'm using this for hopefully precise timing, but I think you are just using delays.  

        # LACEY
        # I was thinking that there would be 3 "states", corresponding to each of the songs.
        # So, the nativity would be state 2.  So, you might be able to just put in a loop for pygame that
        # waits for "state_value" to equal 2.  When it does, you could run the light program with delays, etc.
        # Then, after the program runs it would go back to waiting for state 2 again.
        # I will probably also define a 4th state that is "OFF", where the lights are just doing something
        # pretty, or just steady ON, but no audio is playing.

        # Check the state value
        if state_value is not None:
            # print("State value received:", state_value)

            # Tunnels going
            if state_value=='1' or state_value == '3':
                print("State value received:", state_value)
                stop_event.set()

            # Nativity Triggered
            elif state_value=='2':
                print("State value received:", state_value)
                stop_nativity_threads()
                audio_thread,lights_thread=start_nativity_threads()
                lights_thread.join()
                audio_thread.join()
                stop_event.set()

            # Standby
            elif state_value=='4':
                print("State value received:", state_value)
                stop_event.set()
                for pin in RELAY_PINS:
                    GPIO.output(pin,GPIO.HIGH)
                # turn on star
                GPIO.output(RELAY_PINS[7],GPIO.LOW)
            
            # Reset state_value
            state_value = None


except KeyboardInterrupt:
    print("Pygame loop interrupted")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    print("Cleaning up...")
    # Signal lights and audio to stop
    stop_event.set()
    stop_nativity_threads()
    # Signal the server thread to stop
    running = False
    # Join the server thread here so we can exit it with another CTRL-C
    server_thread.join()
    GPIO.cleanup()