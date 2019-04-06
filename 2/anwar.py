import time

class PID:
    """PID Controller
    """

    def __init__(self, Kp, Ki, Kd, out_max, out_min):
        # self.emit_Signal =  emitsignal
        # self.pilot_enable = False
        # self.enable = False
# 250 53 35
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        self.sample_time = 0.09
        self.current_time = time.time()
        self.last_time = self.current_time

        self.SetPoint = 0.0
        self.depth = 0.0
        # self.sensor_offset = 0.4
        self.pwm_zero = 305

        self.out_max = out_max
        self.out_min = out_min
        self.zero_offset = 305
        self.fwd_zero_offset = 317
        self.bwd_zero_offset = 296

        self.clear()

    def clear(self):
#        self.SetPoint = 0.0
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        # Windup Guard
        self.int_error = 0.0
        self.windup_guard = 20.0

        self.output = 0.0


    def update(self, error):
        self.error = error
#        print("Set Point: "+str(self.SetPoint))
        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = self.error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * self.error
            self.ITerm += self.error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = self.error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)
#            print("output"+str(self.output))
            # add pwm zero offset to output
            if self.output > 0:
                self.output += self.fwd_zero_offset
            else:
                self.output += self.bwd_zero_offset

            # account for min and max ranges
            if self.output > self.out_max:
                self.output = self.out_max
            elif self.output < self.out_min:
                self.output = self.out_min

            # account for dead zone
            if (self.output > self.zero_offset) and (self.output < self.fwd_zero_offset):
                self.output = self.fwd_zero_offset
            elif (self.output < self.zero_offset) and (self.output > self.bwd_zero_offset):
                self.output = self.bwd_zero_offset

        self.output = int(self.output)

    def setWindup(self, windup):
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        self.sample_time = sample_time

