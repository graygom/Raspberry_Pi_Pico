#
# TITLE: control SG90 servo
# AUTHOR: Hyunseung Yoo
# PURPOSE:
# REVISION:
# REFERENCE: Google Gemini Plus
#


import time
from machine import Pin, PWM, I2C


#=========
# CLASS: SG90
class SG90:
    #
    def __init__(self, pwm_pin):
        #
        self.pwm_pin = pwm_pin
        
        # PWM output pin
        self.sg90_servo = PWM( Pin(self.pwm_pin) )
        
        # PWM frequency = 50Hz, period = 20ms
        self.sg90_servo.freq(50)

    # SG90 servo angle
    def set_angle(self, angle):
        # pulse width
        self.pulse_width = 500 + (angle/180.0) * 2000				# 500us ~ 2500us
        self.duty = int( (self.pulse_width / 20000.0) *65535 )		# duty_u16 (0~65535), 20ms=20000us)
        #
        self.sg90_servo.duty_u16(self.duty)


#=========
# CLASS: HCSR04P
class HCSR04P:
    #
    def __init__(self):
        #
        self.i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)
        #
        devices = self.i2c.scan()
        #
        if devices:
            for each_index, each_dev in enumerate(devices):
                output_string = ' %i address %s' % (each_index, hex(each_dev))
                print(output_string)



#==========
# main

sg90_180_1 = SG90(pwm_pin=15)
sg90_360_1 = SG90(pwm_pin=16)
sg90_360_2 = SG90(pwm_pin=17)

us_sensor = HCSR04P()

# 
for each_index, each_angle in enumerate(range(10, 170)):
    #
    sg90_180_1.set_angle(angle=each_angle)
    #
    if each_index == 0:   
        time.sleep_ms(200)
    else:
        time.sleep_ms(30)
# cut
sg90_180_1.sg90_servo.deinit()


# CW
sg90_360_1.set_angle(angle=0)
time.sleep(1)
# CCW
sg90_360_1.set_angle(angle=180)
time.sleep(1)
# stop
sg90_360_1.set_angle(angle=90)
# cut
sg90_360_1.sg90_servo.deinit()


# CW
sg90_360_2.set_angle(angle=0)
time.sleep(1)
# CCW
sg90_360_2.set_angle(angle=180)
time.sleep(1)
# stop
sg90_360_2.set_angle(angle=90)
# cut
sg90_360_2.sg90_servo.deinit()
