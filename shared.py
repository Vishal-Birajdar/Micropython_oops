#from machine import Pin
import json
import neopixel
import time
import machine
rtc = machine.RTC()
t = rtc.datetime()

client = None
arm_status = True
FG_Arm = False
act_sensor_cnt = 0

R1State = machine.Pin(2,machine.Pin.OUT)
R2State = machine.Pin(3,machine.Pin.OUT)
R3State = machine.Pin(4,machine.Pin.OUT)
R4State = machine.Pin(5,machine.Pin.OUT)
active_sensor=[0,0,0,0]

f = open('config.json',"r")
config = json.load(f)

buffer = {"D":'10',"FD":"01","S1":'01',"S2":'02',"S3":'03',"S4":'04',"R1":'0101',"R2":'0102',"R3":'0103',"R4":'0104',"HB":'1'}
string_json = json.dumps(buffer)
buffer_json ={}

topic_json = config['device_info']['c_code']+'/'+config['device_info']['a_code']+'/'+config['device_info']['s_code']+'/'+config['device_info']['s_topic']+'/'+config['device_info']['device_id']
topic_cmd = config['device_info']['c_code']+"/"+config['device_info']['a_code']+"/"+config['device_info']['s_code']+"/CC/"+config['device_info']['device_id']
topic_hb = config['device_info']['c_code']+"/"+config['device_info']['a_code']+"/"+config['device_info']['s_code']+"/HB/"

pixPin = 22
Pixsize = 5
pix = neopixel.NeoPixel(machine.Pin(pixPin),Pixsize)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
ORANGE = (255,165,0)
#------------------------------------------__________________------------------------------------------

file_name = ""

def update_filename():
    global file_name
    # Get the current local time
    t = time.localtime()
    # Create a filename based on the current date
    file_name = '{:04d}_{:02d}_{:02d}.txt'.format(t[0], t[1], t[2])

#file_name = '{:04d}_{:02d}_{:02d}_{:02d}_{:02d}_{:02d}.txt'.format(t[0], t[1], t[2], t[4], t[5], t[6])

def event(msg):
    if file_name == "" or file_name != '{:04d}_{:02d}_{:02d}.txt'.format(time.localtime()[0], time.localtime()[1], time.localtime()[2]):
        update_filename()
    ts = time.localtime()
    ts = time.localtime()
    #ts_str = '{:04d}_{:02d}_{:02d}.txt'.format(time.localtime()[0], time.localtime()[1], time.localtime()[2])
    #ts_str = "[%04d-%02d-%02d-%02d:%02d:%02d]" % (ts.tm_year, ts.tm_mon, ts.tm_mday, ts.tm_hour, ts.tm_min, ts.tm_sec)
    #ts_str = "[%04d-%02d-%02d %02d:%02d:%02d]" % (ts.tm_year, ts.tm_mon, ts.tm_mday, ts.tm_hour, ts.tm_min, ts.tm_sec)
    log_entry = f"{ts} {msg}\n"
    
    with open(file_name, 'a') as file:
        file.write(log_entry)
        
    return log_entry       
   
#-------------------------------------------------________________________--------------------------------------------------- 


