# 
#   server.py
#       handles all server hosting and HTTP stuff for nativity
#       thread initialized in main.py
#   Scott Denton
#   2023
# 
#   If you run this script on the PI, and then send it a http request from a computer on the same network,
#   You should see it return the value of "state" to the browser, and it should print out the value of
#   "state" to the PI commandline.
#       if state is 2 then initialize Nativity lights and audio
#       else standby
#   From the computer, you would format the http request like the following:
#   http://<your pi's IP>:8000/?state=7
#       :8000 specifies the port, and the ?state=7 is just a
#       "get" request which can be parsed out on the server side.
# 
#   MY PI IP: 192.168.117.114/24
# 

import http.server
import socketserver
import urllib

# "state_value" global allows us to be able to communicate from the server to the pygame loop running
state_value = None

# server running variable
running = True

# 
# Custom HTTP request handler
#   Handles HTTP GET requests by parsing query parameters, updating a global state variable,
#   and sending an HTTP response with the current state value.
# 
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

# 
# Just put this in here in case there is an exception and if there isn't good cleanup maybe we can restart the script without having to reboot.
# 
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

# 
# start_server()->None
#   Start HTTP server on port 8000
#
def start_server():
    global running
    with ThreadedTCPServer(("", 8000), CustomHandler) as httpd:
        print("Serving at port", 8000)
        while running:
            httpd.handle_request()
        print("Server closed")
