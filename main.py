# 
#   main.py
#       main pygame loop for nativity light show
#   Scott Denton and Lacey Hunt
#   2023
#

import threading
import server
import nativity

# Start the server thread
server_thread = threading.Thread(target=server.start_server)
server_thread.daemon = True
server_thread.start()

# Pygame loop
try:
    server.state_value=None
    last_state=None
    while True:
        # Check the state value
        if server.state_value is not None:
            # Tunnels going or Standby
            if server.state_value=='1' or server.state_value == '3' or server.state_value == '4':
                print("State value received:", server.state_value)
                nativity.stop_event.set()
                if nativity.lightsOff == False:
                    nativity.lights_off()

            # Nativity Triggered
            elif server.state_value=='2':
                if(last_state!=server.state_value):
                    print("State value received:", server.state_value)
                    nativity.stop_nativity_threads()
                    # nativity.audio_thread, nativity.lights_thread = nativity.start_nativity_threads()
                    nativity.lights_thread = nativity.start_nativity_threads()
            # Reset state value
            
            last_state=server.state_value
            server.state_value = None

# Keyboard Interrupt
except KeyboardInterrupt:
    print("Pygame loop interrupted")
# Other unknown error
except Exception as e:
    print(f"Unexpected error: {e}")
# Clean up
finally:
    print("Cleaning up...")
    # Signal lights and audio to stop
    nativity.stop_event.set()
    nativity.stop_nativity_threads()

    # Signal the server thread to stop
    server.running = False
    # Join the server thread here so we can exit it with another CTRL-C
    server_thread.join()
    
    nativity.GPIO.cleanup()
    exit(0)