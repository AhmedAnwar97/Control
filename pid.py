# -*- coding: utf-8 -*-

"""
    Based on Arduino PID Library (Version 1.0.1) by Brett Beauregard <br3ttb@gmail.com> brettbeauregard.com
"""

from __future__ import division
import sys
import time
#import ms5837
#import Adafruit_PCA9685

#kp = 130 , ki = 80 , kp = 0.1

kp = 130.0
ki = 80.0
kd = 0.1
direct = True
sample_time = 0.01  # seconds
output_value = 0.0
last_input = 0.0
out_max = 400
out_min = 230
zero_offset = 305
freshwaterDepth = 0.0
setpoint = 0.0
i_term = 0.0
windup_guard = 20.0
sensor_offset = 0.0

#sensor = ms5837.MS5837_30BA()
# We must initialize the sensor before reading it
#if not sensor.init():

#    exit(1)

#pwm = Adafruit_PCA9685.PCA9685()
#pwm.set_pwm_freq(50)

last_time = time.time() - sample_time

#sensor.setFluidDensity(1000) # kg/m^3

def compute(kp,ki,kd,direct,setpoint,freshwaterDepth,
            sample_time,last_time,windup_guard,i_term,
            output_value,last_input,out_min,out_max):
    
    
    now = time.time()
    time_change = now - last_time
    
    input_value = freshwaterDepth
    error = setpoint - input_value
    
    i_term += ki * error * sample_time
    if i_term > windup_guard:
         i_term = out_max
    elif i_term < -windup_guard:
         i_term = out_min

    delta_input = input_value - last_input
    output = (kp * error) + i_term + (kd * (delta_input / sample_time))
    print(output)
    output += zero_offset
    if output > out_max:
        output = out_max
    elif output < out_min:
        output = out_min

    output_value = output

    last_input = input_value
    last_time = now
    return output_value

if __name__ == '__main__':
    #if sensor.read():
    #    print("yalla")
    #print(sensor.depth())
    setpoint = input("enter height : ")
    #freshwaterDepth = input("enter depth : ")

    setpoint = float(setpoint)
    #freshwaterDepth = float(freshwaterDepth)
    #pwm.set_pwm(8, 0, 305)
    #pwm.set_pwm(10, 0, 305)
    time.sleep(1)
    #if sensor.read():
    #    sensor_offset=sensor.depth()
    try:
        while True:
            #if not sensor.read():
            #    print("no")
            #freshwaterDepth = sensor.depth() # default is freshwater
            #freshwaterDepth = float(freshwaterDepth)-sensor_offset
            #print("Depth: %.3f m (freshwater)" % (freshwaterDepth))

            val = compute(kp,ki,kd,direct,setpoint,freshwaterDepth,
                        sample_time,last_time,windup_guard,i_term,
                        output_value,last_input,out_min,out_max)
            print("pwm: " + str(val))

            if val:
                val = int(val)
                '''
                pwm.set_pwm(8, 0, val)
                pwm.set_pwm(10, 0, val)
                '''
                last_time = time.time()
            else :
                print("\n")

            time.sleep(0.01)

    except KeyboardInterrupt:
        time.sleep(0.1)
        print("no")
        '''
        pwm.set_pwm(8, 0, 305)
        pwm.set_pwm(10, 0, 305)
        '''

    sys.exit()
