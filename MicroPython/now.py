import network
from esp import espnow

# A WLAN interface must be active to send()/recv()
w0 = network.WLAN(network.STA_IF)
w0.active(True)
w0.disconnect()   # For ESP8266

e = espnow.ESPNow()
e.init()
peer = b'e0\d4\e8\00\00\d2\8a\f7' # MAC address of peer's wifi interface
e.add_peer(peer)

while True:
    host, msg = e.irecv()     # Available on ESP32 and ESP8266
    if msg:             # msg == None if timeout in irecv()
        print(host, msg)
        if msg == b'end':
            break