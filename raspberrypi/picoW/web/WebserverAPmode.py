import network
import time
import socket
import uasyncio as asyncio
from machine import Pin,ADC,I2C
import utime
from BME280 import *


def web_page():
  html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
            <body><h1>Hello World</h1></body></html>
         """
  return html

# if you do not see the network you may have to power cycle
# unplug your pico w for 10 seconds and plug it in again
def ap_mode(ssid, password):
    """
        Description: This is a function to activate AP mode

        Parameters:

        ssid[str]: The name of your internet connection
        password[str]: Password for your internet connection

        Returns: Nada
    """
    # Just making our internet connection
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    while ap.active() == False:
        pass
    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to:: ' + ap.ifconfig()[0])
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
    s.bind(('', 80))
    s.listen(5)

    while True:
      conn, addr = s.accept()
      print('Got a connection from %s' % str(addr))
      request = conn.recv(1024)
      print('Content = %s' % str(request))
      response = web_page()
      conn.send(response)
      conn.close()
   '''  

async def webService():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
    s.bind(('', 80))
    s.listen(5)

    while True:
      conn, addr = s.accept()
      print('Got a connection from %s' % str(addr))
      request = conn.recv(1024)
      print('Content = %s' % str(request))
      response = web_page()
      conn.send(response)
      conn.close()
      await asyncio.sleep_ms(10) 

async def main():    
    while True:
        await asyncio.gather(webService())
        #await asyncio.gather(readSoilMoisture())
        #await asyncio.gather(btHandler(),readSoilMoisture(),notify())
        await asyncio.sleep_ms(10)   

if __name__=="__main__":    
    try:
        ap_mode('grassy', 'zaqwsxcde')
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted")
    finally:        
        asyncio.new_event_loop()
        
