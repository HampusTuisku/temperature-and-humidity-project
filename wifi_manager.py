import network
from time import sleep
import wifi_setup_conf


def connect_wifi():
    """ 
    This function connects the Pico W to the WiFi network using the credentials provided in the wifi_conf.py file.
    
    Returns:
        _true_ if the connection is successful, _false_ otherwise.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    try:
        wlan.connect(wifi_setup_conf.ssid, wifi_setup_conf.password)
        while not wlan.isconnected():
            print('Connecting..')
            sleep(1)
        print("Connected successfully!")
        print("Network config:", wlan.ifconfig())
        print("Running...")
        return True
    except Exception as e:
        print(f"An exception occurred: {e}")
        print("Failed to connect to WiFi.")
        return False
