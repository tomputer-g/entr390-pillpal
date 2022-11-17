# Wireless
import ssl, wifi, socketpool, adafruit_requests
# Capacitive Touch
import time, board, touchio
# Neopixel
import neopixel
# Secrets (secrets.py)
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

### Constants
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
OFF = (0, 0, 0)

### Initializations
touch = touchio.TouchIn(board.A0) #TODO ??
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3, auto_write=False)

### Helper funcs
def led(color):
    pixel.fill(color)
    pixel.show()

### Booting up
led(YELLOW)

# Connect to wifi
wifi.radio.connect(secrets["ssid"], secrets["password"])
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

### Waiting for press
led(OFF)


'''
Logic for demo:
Set next due time from database.
If pressed: blink and move database time.
If time expires: blink red, log to database.
Repeat.
'''