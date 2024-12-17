import network
import json
from umqtt.robust import MQTTClient
import machine
from esecurity import call_loop
import ssl
import time
import shared
from ota import OTAUpdater


s1_pin= machine.Pin(6,machine.Pin.IN,machine.Pin.PULL_UP)
s2_pin= machine.Pin(7,machine.Pin.IN,machine.Pin.PULL_UP)
s3_pin= machine.Pin(8,machine.Pin.IN,machine.Pin.PULL_UP)
s4_pin= machine.Pin(9,machine.Pin.IN,machine.Pin.PULL_UP)
sensor_pin=[s1_pin,s2_pin,s3_pin,s4_pin]

f = open('config.json',"r")
config = json.load(f)

interval = 1000
previousMillis = time.ticks_ms()
wlan = 0
max_attempts=30
retry_delay=6
check_interval=0.5
x = call_loop()

#-------------------------------------___________POWER_ON____________---------------------------------------------------------------
shared.pix[4] = shared.RED
shared.pix.write()
time.sleep(10)
shared.pix[4] = shared.GREEN
shared.pix.write()

shared.event("\tlog Data\n")
#---------------------------------------------_________________CONNECTION__________________--------------------------------------------

class Connection:
    
    def __init__(self):
        pass
    def wifi_connect(self,max_attempts=30, retry_delay=6, check_interval=0.5):
        global wlan
        wlan = network.WLAN(network.STA_IF)
        wlan.disconnect()
        wlan.active(True)
        
        print('Connecting to network....')
        
        for attempt in range(max_attempts):
            wlan.connect(config['wifi']['ssid'],config['wifi']['password'])
            
            # Wait for connection to establish, checking periodically
            elapsed_time = 0
            while elapsed_time < retry_delay:
                if wlan.isconnected():
                    print("Connected")
                    print("IP", wlan.ifconfig())
                    return True
                time.sleep(check_interval)
                elapsed_time += check_interval
                
            
            print(f"\n Attempt {attempt + 1}/{max_attempts} failed, retrying...")
    
        else:
            print("wifi connection failed !")
            shared.event("wifi connection failed !\n")
            machine.reset()

#---------------------------------------------____________READ_CERTIFICATE_______________--------------------------------------------
    def read_certificate(self,file_path):
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            if not data:
                print(f"Error: {file_path} is empty.")
                return None
            print(f"{file_path} read successfully.")
            return data
        except OSError as e:
            print(f"Error reading {file_path}: {e}")
            return None
#------------------------------------------------------------_______________MQTT_CONNECTION________________--------------------------------------------------------
 
 
#-----------------------------------------------------------______________________________--------------------------------------------------------
    def mqtt_connect(self):
        print("Attempting to connect to MQTT broker...")
        try:
            shared.client = MQTTClient(config['device_info']['device_id'],config['mqtt']['broker'],user=config['mqtt']['user'],password=config['mqtt']['password'],keepalive=60,ssl=True)
            shared.client.set_callback(x.callback)
            shared.client.set_last_will(shared.topic_hb,'-1',False,qos=0)
            shared.client.connect()
            print('Connected to %s MQTT Broker' % config['mqtt']['broker'])
            shared.client.publish(shared.topic_hb,'1')
            shared.client.subscribe(shared.topic_cmd+"/D")
            shared.client.subscribe(shared.topic_cmd+"/FD")
            shared.client.subscribe(shared.topic_cmd+"/R1")
            shared.client.subscribe(shared.topic_cmd+"/R2")
            shared.client.subscribe(shared.topic_cmd+"/R3")
            shared.client.subscribe(shared.topic_cmd+"/R4")
            shared.client.subscribe(shared.topic_cmd+"/RR")
            shared.client.subscribe(shared.topic_cmd+"/MR")
            shared.pix[3] = shared.GREEN
            shared.pix.write()
            return shared.client  
        except Exception as e:
            print('Failed to connect to MQTT broker. Reconnecting...',e)
            shared.event('\n Failed to connect to MQTT broker. Reconnecting...')
            shared.client = None
            return shared.client
            machine.reset()
#----------------------------------------------------__________VERSION_UPDATE_______________--------------------------------------------
  
p1 = Connection()       
p1.wifi_connect()
def check_updates():
    try:
        firmware_url = "https://github.com/Vishal-Birajdar/Micropython-/"
        files = ["shared.py", "esecurity.py", "config.json"]
        ota_updater = OTAUpdater(config['wifi']['ssid'],config['wifi']['password'] , firmware_url, files)
        ota_updater.download_and_install_update_if_available()
    except:
        shared.event("Error in updating device \n")
        machine.reset()
        

#--------------------------------------------------------_______________________________--------------------------------------------------------
key_data = p1.read_certificate('privkey4.pem')
cert_data = p1.read_certificate('cert4.pem')
ca_data = p1.read_certificate('chain4.pem')
ssl_params = {
    "certfile": cert_data,
    "keyfile": key_data,
    "cadata": ca_data,
    "server_hostname": config['mqtt']['broker'],
    "cert_reqs": ssl.CERT_REQUIRED
}
check_updates()
p1.mqtt_connect()

#-----------------------------------------------------------__________CONNECTION_CHECKING________________---------------------------------------------

while True:
    try:
        currentMillis = time.ticks_ms()
        for i, s_pin in enumerate(sensor_pin):
            shared.buffer["S"+str(i+1)] = str(s_pin.value())+str(i+1)
            if s_pin.value()==1:shared.active_sensor[i]=1
        shared.act_sensor_cnt=shared.active_sensor.count(1)
        print("active sensor",shared.act_sensor_cnt)
        print("sensor buffer",shared.active_sensor)
        time.sleep(0.1)
        x.main()
        if time.ticks_diff(currentMillis,previousMillis)>=interval:
            previousMillis = currentMillis
            if not wlan.isconnected():
                shared.pix[1] = shared.YELLOW
                shared.pix.write()
                #time.sleep(.4)
                wlan.disconnect()
                for attempt in range(max_attempts):
                    wlan.connect(config['wifi']['ssid'],config['wifi']['password'])
                    gap_time = 0
                    while gap_time < retry_delay:
                        if wlan.isconnected():
                            print("Connected")
                            print("IP", wlan.ifconfig())
                            shared.client.reconnect()
                            print('client reconnected')
                            shared.pix[1] = shared.WHITE
                            shared.pix.write()
                            #shared.event("wifi and client Reconnected\n")
                        time.sleep(check_interval)
                        gap_time += check_interval
                    print("Retrying wifi..")           
    except Exception as e:
        print("Error with ",e)
        shared.event("\n Error in the main flie in loop")
        machine.reset()


