from __future__ import division
from anwar import PID
from UDP import *
import sys
import time
#import Adafruit_PCA9685
#from VideoStream import *
import logging
#from Adafruit_BNO055 import BNO055
#import ms5837


"""
pipline = "v4l2src device=/dev/video0 ! image/jpeg,width=1920,height=1080,framerate=30/1 ! rtpjpegpay ! udpsink host=10.1.1.14 port=5000"
camera  = Gstreamer(pipline)
"""
cony_f   = PID(1,0 ,0 , 360, 250)
cony_b   = PID(1,0 ,0 , 360, 250)

conz   = PID(1,0 ,0 , 400, 200)
conyaw_f = PID(0.5,0.1 ,0 , 340, 250)
conyaw_b = PID(0.3,0.1 ,0 , 340, 250)
"""
sensor = ms5837.MS5837_30BA()
# We must initialize the sensor before reading it
if not sensor.init():
        exit(1)

# We have to read values from sensor to update pressure and temperature
if not sensor.read():
    exit(1)

sensor.setFluidDensity(1000) # kg/m^3

"""
print("yallaaaaaaa")

toss=UDP_Server("192.168.43.232",9919)
helali=UDP_Client("192.168.43.190",9920)
"""
bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
"""
# Sensor data, desired set value, errors, and PWMs 
sensor_yaw = 0.0
set_yaw    =0.0
errory   = 0.0
errorz   = 0.0  
erroryaw = 0.0
last_depth = 0.0
valy_f, valy_b, valz, valyaw = 0.0, 0.0, 0.0, 0.0

"""
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
"""
time.sleep(0.01)

set_point = False
ack = False
set_pointz = False
read = 0.0

try:
    while True:

            data=toss.recieve()
            #data=data.split(",")
            #errory   = float(data[0])
            #errorz   = float(data[1])
            #erroryaw = float(data[2])

            #cony_f.update(errory)
            #cony_b.update(-1.0*errory)

            #valy_f = cony_f.output
            #valy_b = cony_b.output

            conyaw_f.update(erroryaw)
            conyaw_b.update(-1.0*erroryaw)
            valyaw_f = conyaw_f.output
            valyaw_b = conyaw_b.output

            if not set_point:
                set_p = float(data)
                set_point = True
            else:
                read = float(data)
                print ("data recieved : " + str(read))
                erroryaw = set_p - read

            # Read the Euler angles for heading, roll, pitch (all in degrees).
            if erroryaw > 10 or erroryaw < -10:
                
                #set_point = False
                if not ack:
                    helali.send("halt")
                    print ("halt")
                    ack = True
                #pwm.set_pwm(11, 0, valz/3)
                #pwm.set_pwm(9, 0,  valz/3)
                if erroryaw > 50:
                    print ("right")
                    print ("valyaw_b : " + str(valyaw_b))
                    print ("valyaw_f : " + str(valyaw_f))
                    #pwm.set_pwm(3, 0, valyaw_b)
                    #pwm.set_pwm(5, 0, valyaw_f)
                else:
                    print ("left")
                    print ("valyaw_b : " + str(valyaw_b))
                    print ("valyaw_f : " + str(valyaw_f))
                    #pwm.set_pwm(3, 0, valyaw_f)
                    #pwm.set_pwm(5, 0, valyaw_b)

            else:
                if not set_point:
                    set_yaw = sensor_yaw
                    set_point = True
                if ack:
                    helali.send("ack")
                    print ("ack")
                    #set_yaw, roll, pitch = bno.read_euler()
                    #set_point = True
                    ack = False
                """
                if errorz > errory:
                    #conz.update(errorz)
                    #valz   = conz.output/100
                    #pwm.set_pwm(11, 0, valz)
                    #pwm.set_pwm(9, 0,  valz)
                else:
                    if not set_pointz:
                        #freshwaterDepthS = sensor.depth() # default is freshwater
                        #freshwaterDepthS = float(freshwaterDepth)
                        #set_pointz = True
                    #current_z = sensor.depth() # default is freshwater
                    #current_z = float(current_z)
                    #errorz = freshwaterDepthS - current_z
                    #conz.update(errorz)
                    #valz   = conz.output
                    #pwm.set_pwm(11, 0, valz)
                    #pwm.set_pwm(9, 0,  valz)
                """
                """
                pwm.set_pwm(7, 0,  valy_f)
                pwm.set_pwm(5, 0,  valy_b)
                pwm.set_pwm(13, 0, valy_f)
                pwm.set_pwm(15, 0, valy_b)
                pwm.set_pwm(11, 0, valz)
                pwm.set_pwm(9, 0,  valz)
          """

except KeyboardInterrupt:
    time.sleep(0.1)
    """
    pwm.set_pwm(5, 0, 305)
    pwm.set_pwm(7, 0, 305)
    pwm.set_pwm(13, 0, 305)
    pwm.set_pwm(15, 0, 305)
    pwm.set_pwm(11, 0, 305)
    pwm.set_pwm(9, 0, 305)
    """
    print("no")


sys.exit()




"""
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
"""