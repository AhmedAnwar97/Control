from __future__ import division
from anwar import PID
from UDP import UDP_Server
import sys
import time
import Adafruit_PCA9685
from VideoStream import *
import logging
from Adafruit_BNO055 import BNO055


pipline = "v4l2src device=/dev/video0 ! image/jpeg,width=1920,height=1080,framerate=30/1 ! rtpjpegpay ! udpsink host=10.1.1.14 port=5000"
camera  = Gstreamer(pipline)

cony_f   = PID(1,0 ,0 , 360, 250)
cony_b   = PID(1,0 ,0 , 360, 250)

conz   = PID(1,0 ,0 , 400, 200)
conyaw_f = PID(0.3,0 ,0 , 340, 250)
conyaw_b = PID(0.3,0 ,0 , 340, 250)


print("yallaaaaaaa")

toss=UDP_Server("10.1.1.15",9020)

bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()

# Sensor data, desired set value, errors, and PWMs 
sensor_yaw = 0.0
set_yaw    =0.0
errory   = 0.0
errorz   = 0.0  
erroryaw = 0.0
valy_f, valy_b, valz, valyaw = 0.0, 0.0, 0.0, 0.0


sensor_yaw, roll, pitch = bno.read_euler()
print (sensor_yaw)

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

pwm.set_pwm(5, 0, 305)
pwm.set_pwm(7, 0, 305)
pwm.set_pwm(9, 0, 305)
pwm.set_pwm(8, 0, 305)
pwm.set_pwm(13, 0, 305)
pwm.set_pwm(15, 0, 305)
pwm.set_pwm(11, 0, 305)

time.sleep(0.01)

set_point = False

try:
    while True:

            data=toss.recieve()
            data=data.split(",")
            
            # Read the Euler angles for heading, roll, pitch (all in degrees).
            if not set_point:
                set_yaw, roll, pitch = bno.read_euler()
                set_point = True
            else :
                sensor_yaw, roll, pitch = bno.read_euler()
                erroryaw = sensor_yaw - set_yaw

            errory   = float(data[0])
            errorz   = float(data[1])
#            erroryaw = float(data[2])

            cony_f.update(errory)
            conz.update(errorz)
            cony_b.update(-1.0*errory)

            valy_f = cony_f.output
            valy_b = cony_b.output
            valz   = conz.output
#            valyaw   = conyaw.update(erroryaw)

            conyaw_f.update(erroryaw)
            conyaw_b.update(-1.0*erroryaw)
            valyaw_f = conyaw_f.output
            valyaw_b = conyaw_b.output

            print("pwm in y     : " + str(valy_f))
            print("pwm in z     : " + str(valz))
            print("pwm in yaw   : " + str(valyaw))
            print("error        : " + str(erroryaw))
            if erroryaw < 5 and erroryaw > -5:
                 print ("hello")
#                pwm.set_pwm(7, 0,  valy_f)
#                pwm.set_pwm(5, 0,  valy_b)
#                pwm.set_pwm(13, 0, valy_f)
#                pwm.set_pwm(15, 0, valy_b)
#                pwm.set_pwm(11, 0, valz)
#                pwm.set_pwm(9, 0,  valz)

#                last_time = time.time()
            else :
                print ("yaw error : " + str(erroryaw))
                pwm.set_pwm(7, 0,  valyaw_f)
                pwm.set_pwm(5, 0,  valyaw_b)
                pwm.set_pwm(13, 0, valyaw_f)
                pwm.set_pwm(15, 0, valyaw_b)
#                pwm.set_pwm(11, 0, valz/3)
#                pwm.set_pwm(9, 0,  valz/3)

#            time.sleep(0.01)

except KeyboardInterrupt:
    time.sleep(0.1)
    pwm.set_pwm(5, 0, 305)
    pwm.set_pwm(7, 0, 305)
    pwm.set_pwm(13, 0, 305)
    pwm.set_pwm(15, 0, 305)
    pwm.set_pwm(11, 0, 305)
    pwm.set_pwm(9, 0, 305)
    print("no")


sys.exit()
