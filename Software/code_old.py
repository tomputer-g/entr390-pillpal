
# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""HTTP POST"""
import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
"""CircuitPython Capacitive Touch"""
import time
import board
import touchio
touch = touchio.TouchIn(board.D5)

"""CircuitPython Essentials NeoPixel example"""
import neopixel
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3, auto_write=False)



#RED: has power, starting
pixels.fill(RED)
pixels.show()
# URLs to fetch from
# Get wifi details and more from a secrets.py file


#print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
#wifi.radio.start_scanning_networks()
#wifi.radio.stop_scanning_networks()

#YELLOW: connecting
pixels.fill(YELLOW)
pixels.show()
wifi.radio.connect(secrets["ssid"], secrets["password"])
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

#GREEN: connected, waiting
pixels.fill(GREEN)
pixels.show()

while True:
    while not touch.value:
        time.sleep(0.05) #wait for a touch
    print("Trying to post to Xano database")
    #BLUE: sending to database
    pixels.fill(BLUE)
    pixels.show()
    response = None
    while not response:
        try:
            response = requests.post(secrets["test-post"])
            failure_count = 0
        except AssertionError as error:
            print("Request failed, retrying...\n", error)
            failure_count += 1
            if failure_count >= attempts:
                raise AssertionError(
                    "Failed to resolve hostname, \
                                      please check your router's DNS configuration."
                ) from error
            continue
    print(str(response.text))
    print("Done Posting Cringe")
    print("-" * 40)
    #GREEN: connected, waiting
    pixels.fill(GREEN)
    pixels.show()
    while touch.value:
        time.sleep(0.05) #Wait for touch to stop
