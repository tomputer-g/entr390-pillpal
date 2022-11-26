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
# Stuff
import math
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
    timestamp_dat = datetime(ntp.datetime.tm_year, ntp.datetime.tm_mon, ntp.datetime.tm_mday, ntp.datetime.tm_hour, ntp.datetime.tm_min)
    json_data = {"Starting_timestamp": str(timestamp_dat)}
    print(json_data)
    ret = db_post(secrets["api-post"] + "/records", json_data)
    print("Press:",ret.text)
    led(GREEN)
    time.sleep(0.2)
    led(OFF)

def watchdog_post():
    led(PURPLE)
    timestamp_dat = datetime(ntp.datetime.tm_year, ntp.datetime.tm_mon, ntp.datetime.tm_mday, ntp.datetime.tm_hour, ntp.datetime.tm_min - 1)
    json_data = {"timestamp_prev": str(timestamp_dat)}
    print(json_data)
    ret = db_post(secrets["api-post"] + "/watchdog", json_data)
    print("Watchdog:",ret.text)
    led(GREEN)
    time.sleep(0.2)
    led(OFF)

def db_post(url, json_data):
    response = None
    while not response:
        try:
            response = requests.post(url, data=json_data)
        except AssertionError as error:
            print("Request failed", error)
            response = None
            #failure_count += 1
            #if failure_count >= 5:
            #    raise AssertionError(
            #        "Failed to resolve hostname, \
            #                          please check your router's DNS configuration."
            #    ) from error
            #continue
    return response

def wifi_init():
    # Connect to wifi
    global requests
    global ntp
    wifi.radio.connect(secrets["ssid"], secrets["password"])
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    ntp = adafruit_ntp.NTP(pool, tz_offset=0) #EST + Daylight savings

def main():
    debounce = False
    #prev_time = time.monotonic()
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

        if ntp.datetime.tm_sec == 0:
            watchdog_post()
            time.sleep(0.8)
        #if time.monotonic() - prev_time >= 60.0:
        #    prev_time = time.monotonic()
        #    watchdog_post()
        time.sleep(0.5)

if __name__ == "__main__":
    main()
