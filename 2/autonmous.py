
from __future__ import division 
from anwar import PID 
from UDP import UDP_Server 
import sys 
import time 
import Adafruit_PCA9685 
from VideoStream import *

pipline =  "v4l2src device=/dev/video0 ! image/jpeg,width=1920,height=1080,framerate=30/1 ! rtpjpegpay ! udpsink host=10.1.1.14 port=5000"
camera = Gstreamer(pipline)

cony_f = PID(0.3, 0.2, 0.1, 360, 250)
cony_b = PID(0.3, 0.2, 0.1, 360, 250)
conz = PID(0.4, 0, 0, 400, 200)
print("yallaaaaaaa")
    #setpoint = input("enter height : ")
    #freshwaterDepth = input("enter depth : ")
    
toss=UDP_Server("10.1.1.15",9020)
    
    #setpoint = float(setpoint)
    #nput_value = input("enter current point : ")
    #input_value=float(input_value)
    #freshwaterDepth = float(freshwaterDepth)
errory=0.0
errorz=0.0 
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)
 
pwm.set_pwm(5, 0, 305)
pwm.set_pwm(7, 0, 305)
pwm.set_pwm(13, 0, 305)
pwm.set_pwm(15, 0, 305)
pwm.set_pwm(11, 0, 305)
pwm.set_pwm(9, 0, 305)
#pwm.set_pwm(9, 0, 305)
#pwm.set_pwm(8, 0, 305)

time.sleep(0.1)

valy_f, valy_b, valz = 0.0, 0.0, 0.0
try:
    while True:
            data=toss.recieve()
            #print(data)
            data=data.split(",")
            #print(data)
            #print(data[0])
            errory=float(data[0])
            errorz=float(data[1])

            cony_f.update(errory)
            cony_b.update(-1.0*errory)
#            conz.update(errorz)

            valy_f = cony_f.output
            valy_b = cony_b.output
#            valz = conz.output

            print("pwm in y   : " + str(valy_f))
            print("pwm in y   : " + str(valy_b))
   #         print("pwm in yaw : " + str(val2))
            if valy_f:

                pwm.set_pwm(7, 0,  valy_f)
                pwm.set_pwm(5, 0,  valy_b)
                pwm.set_pwm(13, 0, valy_f)
                pwm.set_pwm(15, 0, valy_b)
#                pwm.set_pwm(11, 0, valz)
#                pwm.set_pwm(9, 0,  valz)

                last_time = time.time()
            else :
                print("\n")

            time.sleep(0.01)

except KeyboardInterrupt:
    time.sleep(0.1)
    print("no")
    pwm.set_pwm(5, 0, 305)
    pwm.set_pwm(7, 0, 305)
    pwm.set_pwm(13, 0, 305)
    pwm.set_pwm(15, 0, 305)
    pwm.set_pwm(11, 0, 305)
    pwm.set_pwm(9, 0, 305)

sys.exit()
