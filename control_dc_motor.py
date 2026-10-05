#
# TITLE: control DC motors
# AUTHOR: Hyunseung Yoo
# PURPOSE:
# REVISION:
# REFERENCE: Google Gemini Plus
#


import time
from machine import Pin, PWM


#==========
# CLASS L9110S (dc motor driver)
class L9110S:
    #
    def __init__(self, IN1_pin, IN2_pin):
        # user input
        self.IN1_pin = IN1_pin
        self.IN2_pin = IN2_pin
        
        # PWM signal
        self.dc_motor_IN1_pwm = PWM( Pin( self.IN1_pin ) )
        self.dc_motor_IN2_pwm = PWM( Pin( self.IN2_pin ) )
        
    
    def set_pwm_freq(self, pwm_freq):
        # PWM frequency range = 1kHz ~ 20kHz
        self.pwm_freq = pwm_freq
        self.dc_motor_IN1_pwm.freq( self.pwm_freq )
        self.dc_motor_IN2_pwm.freq( self.pwm_freq )


    def set_speed(self, pwm_speed):
        # PWM speed: -100 (CCW) ~ 0 (stop) ~ +100 (CW)
        self.pwm_speed = pwm_speed
        self.duty = int( abs( self.pwm_speed ) / 100 * 65535 )
        
        #
        if self.pwm_speed > 0:
            self.dc_motor_IN1_pwm.duty_u16(self.duty)
            self.dc_motor_IN2_pwm.duty_u16(0)
        #            
        elif self.pwm_speed < 0:
            self.dc_motor_IN1_pwm.duty_u16(0)
            self.dc_motor_IN2_pwm.duty_u16(self.duty)
        #
        else:
            self.dc_motor_IN1_pwm.duty_u16(0)
            self.dc_motor_IN2_pwm.duty_u16(0)
    

#==========
# main

dc_motor_fw_right = L9110S(IN1_pin=16, IN2_pin=17)
dc_motor_fw_right.set_pwm_freq(pwm_freq=1000)
dc_motor_fw_right.set_speed(pwm_speed=100)
time.sleep(3)
dc_motor_fw_right.set_speed(pwm_speed=0)
