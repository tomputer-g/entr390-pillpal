# Wireless
import ssl, wifi, socketpool, adafruit_requests
# Time
import adafruit_ntp
from adafruit_datetime import datetime
from time import mktime
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

### Globals
requests = None
ntp = None
### Initializations
touch = touchio.TouchIn(board.A3)
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3, auto_write=False)

### Helper funcs
def led(color):
    pixel.fill(color)
    pixel.show()

def onPress():
    led(YELLOW)
    ret = db_post(secrets["api-post"] + "/default")
    print("Press:",ret.text)
    led(GREEN)
    time.sleep(0.2)
    led(OFF)

def watchdog_post():
    led(YELLOW)
    ret = db_post(secrets["api-post"] + "/default/1") #???
    print("Watchdog:",ret.text)
    led(RED)
    time.sleep(0.2)
    led(OFF)    
    
def db_post(url): #Test OK
    response = None
    while not response:
        try:
            response = requests.post(url)
            failure_count = 0
        except AssertionError as error:
            print("Request failed, retrying...\n", error)
            failure_count += 1
            if failure_count >= 5:
                raise AssertionError(
                    "Failed to resolve hostname, \
                                      please check your router's DNS configuration."
                ) from error
            continue
    return response

def db_post(url):
    response = None
    json_data = {"created_at": str(datetime.fromtimestamp(mktime(ntp.datetime)))}
    while not response:
        try:
            response = requests.post(url, data=json_data)
            failure_count = 0
        except AssertionError as error:
            print("Request failed, retrying...\n", error)
            failure_count += 1
            if failure_count >= 5:
                raise AssertionError(
                    "Failed to resolve hostname, \
                                      please check your router's DNS configuration."
                ) from error
            continue
    return response
    
def wifi_init():
    # Connect to wifi
    global requests
    global ntp
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    ntp = adafruit_ntp.NTP(pool, tz_offset=-5) #EST + Daylight savings
    
def main():
    debounce = False
    prev_time = time.monotonic()
    ### Booting up
    led(BLUE)

    wifi_init()

    ### Waiting for press
    led(OFF)

    while True:
        # Only trigger onPress on a rising edge
        if touch.value:
            if not debounce:
                debounce = True
                onPress()
        else:
            debounce = False
            
        #if time.monotonic() - prev_time >= 60.0:
        #    prev_time = time.monotonic()
        #    watchdog_post()
        
        time.sleep(0.2)
        
if __name__ == "__main__":
    main()