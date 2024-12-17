import network
import socket
import time
import random
from machine import Pin

led = Pin('LED',Pin.OUT)


def webpage(random_value,state):
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title>Pico web server </title>
        <meta name ="viewport" content="width=device-width,initial-scale=1">
        <head>
        <body>
        <h1>Raspberry Pi Pico Web Server </h1>
        <h2>LED Control</h2>
        <form action= "./lighton">
            <input type="submit" value"Light on"/>
        </form>
        <br>
        <form action= "./lightoff">
            <input type="submit" value"Light Off"/>
        </form>
        <p>LED state: {state}</p>
        <h2>Fetch New Value<h2>
        <form action="./value">
            <input type="submit"value"Fetch value"/>
        </form>
        <p>Fetched value: {random_value}</p>
        </body>
        </html>
        """
    return str(html)

wlan  = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('DataMann','Datamann@2022)

connection_timeout = 10
while connection_timeout > 0:
    if wlan.status() >= 3:
        break
    connection_timeout -= 1
    print('Waiting for Wi-Fi connection...')
    time.sleep(1)

# Check if connection is successful
if wlan.status() != 3:
    raise RuntimeError('Failed to establish a network connection')
else:
    print('Connection successful!')
    network_info = wlan.ifconfig()
    print('IP address:', network_info[0])

#Set up socket and start listening
    
addr = socket.getaddrinfo('0.0.0.0',80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(addr)
s.listen()
print('Listening on',addr)

state = "OFF"
random_value = 0

while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from', addr)
        
        # Receive and parse the request
        request = conn.recv(1024)
        request = str(request)
        print('Request content = %s' % request)

        try:
            request = request.split()[1]
            print('Request:', request)
        except IndexError:
            pass
        
        # Process the request and update variables
        if request == '/lighton?':
            print("LED on")
            led.value(1)
            state = "ON"
        elif request == '/lightoff?':
            led.value(0)
            state = 'OFF'
        elif request == '/value?':
            random_value = random.randint(0, 20)

        # Generate HTML response
        response = webpage(random_value, state)  

        # Send the HTTP response and close the connection
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()

    except OSError as e:
        conn.close()
        print('Connection closed')
