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
            print("State value received:", state_value)
            # Nativity Triggered
            if state_value=='1':
                print("Hello, ")
                time.sleep(1)
                print ("World")
            elif state_value=='2':
                pygame.mixer.init()
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()

                for pin in RELAY_PINS:
                    GPIO.output(pin, GPIO.LOW)
                    time.sleep(1)
                    GPIO.output(pin, GPIO.HIGH)
                    time.sleep(1)
                time.sleep(pygame.mixer.music.get_length())  # Wait for audio to finish
                pygame.mixer.quit()
                # reset state_value
            # turn off all pins
            elif state_value=='4':
                for pin in RELAY_PINS:
                    GPIO.output(pin,GPIO.HIGH)
            state_value = None


except KeyboardInterrupt:
    print("Pygame loop interrupted")
finally:
    print("Cleaning up...")
    # Signal the server thread to stop
    running = False
    # Join the server thread here so we can exit it with another CTRL-C
    server_thread.join()