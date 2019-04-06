# -*- coding: utf-8 -*-

"""
    Based on Arduino PID Library (Version 1.0.1) by Brett Beauregard <br3ttb@gmail.com> brettbeauregard.com
"""

from __future__ import division
import sys
import time
import ms5837
import Adafruit_PCA9685

kp = 29.0
ki = 0
kd = 0
direct = True
sample_time = 0.01  # seconds
output_value = 0.0
last_input = 0.0
out_max = 450
out_min = 250
zero_offset = 305
freshwaterDepth = 0.0
setpoint = 0.0
i_term = 0.0
windup_guard = 20.0

sensor = ms5837.MS5837_30BA()
# We must initialize the sensor before reading it
if not sensor.init():
        exit(1)

# We have to read values from sensor to update pressure and temperature
if not sensor.read():
    exit(1)

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

last_time = time.time() - sample_time

sensor.setFluidDensity(1000) # kg/m^3

def compute(kp,ki,kd,direct,setpoint,
            sample_time,last_time,windup_guard,
            output_value,last_input,out_min,out_max):
    
    
    now = time.time()
    time_change = now - last_time
    
    input_value = freshwaterDepth
    error = setpoint - input_value
    
    i_term += ki * error * sample_time
    if i_term > windup_guard:
         i_term = out_max
    elif i_term < windup_guard:
         i_term = out_min

    delta_input = input_value - last_input
    output = (kp * error) + i_term + (kd * (delta_input / sample_time))

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
    setpoint = input("enter height : ")
    #freshwaterDepth = input("enter depth : ")

    setpoint = float(setpoint)
    #freshwaterDepth = float(freshwaterDepth)

    try:
        while True:
            freshwaterDepth = sensor.depth() # default is freshwater
            freshwaterDepth = float(freshwaterDepth)
            print("Depth: %.3f m (freshwater)" % (freshwaterDepth))

            val = compute(kp,ki,kd,direct,setpoint,
                        sample_time,last_time,windup_guard,
                        output_value,last_input,out_min,out_max)
            print("pwm: " + str(val))
            
            if val:
                pwm.set_pwm(8, 0, output_value)
                pwm.set_pwm(10, 0, output_value)
                last_time = time.time()
            else :
                print("\n")
            
            time.sleep(0.01)

    except KeyboardInterrupt:
        print('exit')

    sys.exit()