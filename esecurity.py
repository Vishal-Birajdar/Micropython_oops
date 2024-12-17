import time
#import neopixel
#from machine import Pin
#from umqtt.robust import MQTTClient
import shared
import machine
import json
#import ssl
    
    
    
class call_loop:
    def __init__(self):
        pass
    def callback(self,topic_cmd,msg):
        try:
            decoded_topic = topic_cmd.decode('utf-8').strip()
            decoded_msg = msg.decode('utf-8').strip()
            print("decoded_topic:"+decoded_topic)
            print("decoded_msg:"+decoded_msg)
            if decoded_topic.endswith("FD"):
                print("decoded_topic:"+decoded_topic)
                if decoded_msg == '12':
                    shared.buffer["FD"] = '12'
                    shared.FG_Arm = True
                    print("shared.FG_Arm ",shared.FG_Arm)
                    shared.string_json = json.dumps(shared.buffer)
                elif decoded_msg == '01':
                    shared.buffer["FD"] == '01'
                    shared.FG_Arm = False
                    print("shared.FG_Arm ",shared.FG_Arm)
                    shared.string_json = json.dumps(shared.buffer)
                else:
                    print("Invalid Input !")
            elif decoded_topic.endswith("D"):
                print("decoded_topic:"+decoded_topic)
                if decoded_msg == '00':
                    shared.buffer["D"] = decoded_msg
                    shared.arm_status = False
                    shared.string_json = json.dumps(shared.buffer)
                    shared.pix[0] = shared.RED
                    shared.pix.write()
                elif decoded_msg == '10':
                    shared.buffer["D"] = decoded_msg
                    shared.arm_status = True
                    shared.string_json = json.dumps(shared.buffer)
                    shared.pix[0] = shared.GREEN
                    shared.pix.write()
                    print("shared.arm_status is ", shared.arm_status)
                else:
                    print("Invalid input!!")
            elif decoded_topic.endswith("RR"):
                if decoded_msg == '05':
                    shared.R1State.value(0)
                    shared.R2State.value(0)
                    shared.R3State.value(0)
                    shared.R4State.value(0)
                    shared.active_sensor =[0,0,0,0]
                    shared.buffer["R1"] = '0101'
                    shared.buffer["R2"] = '0102'
                    shared.buffer["R3"] = '0103'
                    shared.buffer["R4"] = '0104'
                    shared.string_json = json.dumps(shared.buffer)
            elif decoded_topic.endswith("MR"):
                if decoded_msg == '06':
                    machine.reset()
            elif decoded_topic.endswith("R1"):
                if decoded_msg == '0101':
                    shared.buffer["R1"] = decoded_msg
                    shared.R1State.value(0)
                    shared.string_json = json.dumps(shared.buffer)
                    print("R1 state ",shared.R1State.value())
                elif decoded_msg == '1101' and shared.arm_status:
                    shared.buffer["R1"] = decoded_msg
                    shared.string_json = json.dumps(shared.buffer)
                    shared.R1State.value(1)
                else:
                    print("Invalid input")
                
            elif decoded_topic.endswith("R2"):
                if decoded_msg == '0102':
                    shared.buffer["R2"] = decoded_msg
                    shared.string_json = json.dumps(shared.buffer)
                    shared.R2State.value(0)
                elif decoded_msg == '1102' and shared.arm_status:
                    shared.buffer["R2"] = decoded_msg
                    shared.string_json = json.dumps(shared.buffer)
                    shared.R2State.value(1)
                else:
                    print("Invalid input")
            elif decoded_topic.endswith("R3"):
                if decoded_msg == '0103':
                    shared.buffer["R3"] = decoded_msg
                    shared.R3State.value(0)
                    shared.string_json = json.dumps(shared.buffer)
                elif decoded_msg == '1103' and shared.arm_status:
                    shared.buffer["R3"] = decoded_msg
                    shared.string_json = json.dumps(shared.buffer)
                    shared.R3State.value(1)
                else:
                    print("Invalid input")
            elif decoded_topic.endswith("R4"):
                if decoded_msg == '0104':
                    shared.buffer["R4"] = decoded_msg
                    shared.string_json = json.dumps(shared.buffer)
                    shared.R4State.value(0)
                elif decoded_msg == '1104' and shared.arm_status:
                    shared.buffer["R4"] = decoded_msg
                    shared.string_json = json.dumps(shared.buffer)
                    shared.R4State.value(1)
                else:
                    print("Invalid input")       
            shared.string_json = json.dumps(shared.buffer)
            shared.client.publish(shared.topic_json,shared.string_json)
        except Exception as e:
            print("Error subscribing to the topic ",e)
            shared.event('\n Error subscribing to the topic')
            machine.reset()
#-----------------------------------------------------------------------___________Main___________________------------------------------------------------------------------        
    def main(self):
        try:
            time.sleep(1)
            shared.client.check_msg()
            time.sleep(0.5)
            if shared.arm_status == True:
                shared.pix[0] = shared.GREEN
                shared.pix.write()
                
                if shared.act_sensor_cnt == 0:
                    sared.pix[2] = shared.GREEN
                    shared.pix.write()
                if shared.act_sensor_cnt == 1:
                    shared.R1State.value(1)
                    shared.pix[2] = shared.YELLOW
                    shared.pix.write()
                    shared.buffer["R1"] = "1101"
                elif shared.act_sensor_cnt == 2:
                    shared.pix[2] = shared.BLUE
                    shared.pix.write()
                    shared.R2State.value(1)
                    shared.buffer["R2"] = "1102"
                elif shared.act_sensor_cnt == 3:
                    shared.pix[2] = shared.PURPLE
                    shared.pix[1] = shared.ORANGE
                    shared.pix.write()
                    shared.R3State.value(1)
                    shared.buffer["R3"] = "1103"
                elif shared.act_sensor_cnt >= 3:
                    if shared.FG_Arm == True:
                        print("FG status ",shared.FG_Arm)
                        shared.pix[2] = shared.CYAN
                        shared.pix[1] = shared.RED
                        shared.pix.write()
                        shared.R4State.value(1)
                        shared.buffer["R4"] = "1104"
                        shared.buffer["FD"] = "12"
            else:
                shared.FG_Arm = False
                shared.R1State.value(0)
                shared.R2State.value(0)
                shared.R3State.value(0)
                shared.R4State.value(0)
                shared.buffer["R1"] = '0101'
                shared.buffer["R2"] = '0102'
                shared.buffer["R3"] = '0103'
                shared.buffer["R4"] = '0104'
                shared.buffer["FD"] = '01'
                shared.pix[1] = shared.RED
                shared.pix.write()
            shared.buffer_json[shared.config['device_info']['device_id']]=shared.buffer
            shared.string_json = json.dumps(shared.buffer_json)
            shared.client.publish(shared.topic_json,shared.string_json)
        except Exception as e:
            print("Failed Connection with error:",e)
            shared.event('\n Failed Connection with error in esecurity file ')
            time.sleep(1)
            machine.reset()	

