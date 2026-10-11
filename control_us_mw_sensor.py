#
# TITLE: ultra-sonic sensor (HC-SR04P) & microwave sensor (SEN0192)
# AUTHOR: Hyunseung Yoo
# PURPOSE:
# REVISION:
# REFERENCE: Google Gemini Plus
#


import utime, time
import uasyncio as asyncio
from machine import Pin, PWM, I2C


#=========
# CLASS: SEN0192
#  Gravity: microwave sensor v2.0 module (DFRobot)
#  Doppler effect, 10.525GHz
#    Vcc = 5.0V
#    GND = 0.0V
#    OUT/D = MCU GPIO (3.3V)

class SEN0192:
    # constructor
    def __init__(self, out_pin:int):
        # user input
        self.out_pin  = out_pin
        
        # GPIO
        self.out_gpio = Pin( self.out_pin, Pin.IN, Pin.PULL_DOWN )
        time.sleep_ms(10)
        
        # control parameters
        self.event_no = 0
        self.motion_detected = False
        self.last_trigger_time = 0
        self.debounce_ms = 500			# ms
        
        
    # Interrupt Service Routine
    def irq_handler(self, pin):
        #
        current_time = utime.ticks_ms()
        
        # check debounce time
        if utime.ticks_diff(current_time, self.last_trigger_time) > self.debounce_ms:
            if pin.value() == 1:
                self.motion_detected = True
                self.event_no += 1
                self.last_trigger_time = current_time
        


#=========
# CLASS: HCSR04P
#  detection range = 2cm ~ 450cm
#  Vcc range = 2.8 ~ 5.5V
#    Vcc ~ 3.3V (GPIO output)
#    GND ~ 0.0V
#    sda ~ data (i2c)
#    scl ~ clock (i2c)

class HCSR04P:
    #
    def __init__(self, i2c_ch:int, sda_pin:int, scl_pin:int, i2c_freq:int, i2c_addr:int):
        # user input
        self.i2c_ch  = i2c_ch
        self.sda_pin = sda_pin
        self.scl_pin = scl_pin
        
        # sda
        self.sda_gpio  = Pin( self.sda_pin, Pin.IN, Pin.PULL_UP )
        time.sleep_ms(100)		# wait
        
        # scl
        self.scl_gpio  = Pin( self.scl_pin, Pin.IN, Pin.PULL_UP )
        time.sleep_ms(100)		# wait
        
        # i2c operation
        self.i2c_freq = i2c_freq
        self.i2c_addr = i2c_addr
        
        # i2c
        self.i2c = I2C(self.i2c_ch, sda=self.sda_gpio, scl=self.scl_gpio, freq=self.i2c_freq)
        time.sleep_ms(100)		# wait
        
        # available addresses
        devices = self.i2c.scan()
        output_string = 'I2C channel %i, available addr = %s' % (self.i2c_ch, [hex(each_device) for each_device in devices])
        print(output_string)
            
    #
    def distance_mm(self) -> float:
        # measurement command 0x01
        self.i2c.writeto(self.i2c_addr, bytearray([0x01]))
            
        # receive time
        utime.sleep_ms(200)
            
        # result
        data = self.i2c.readfrom(self.i2c_addr, 3)
            
        # calculation
        # data[0]: high, data[1]: low -> (big endian)
        dist_mm = (data[0] << 16) | (data[1] << 8) | data[2]
            
        #
        return round(dist_mm/1024)
        


#==========
# main

# microwave sensor
if True:
    mw_sensor = SEN0192(out_pin=15)
    mw_sensor.out_gpio.irq(trigger=mw_sensor.out_gpio.IRQ_RISING, handler=mw_sensor.irq_handler)

    try:
        while True:
            #
            if mw_sensor.motion_detected:
                print('%4i SEN0192 motion detected' % (mw_sensor.event_no))
                mw_sensor.motion_detected = False
            #    
            utime.sleep_ms(500)
            
    except KeyboardInterrupt:    
        print('done.')


# ultra-sonic sensor
if True:
    us_sensor = HCSR04P(i2c_ch=0, sda_pin=0, scl_pin=1, i2c_freq=100000, i2c_addr=0x57)
    for cnt in range(100):
        dist_mm = us_sensor.distance_mm()
        #
        output_string = 'count=%4i distance = %imm' % (cnt, dist_mm)
        print(output_string)
         #
        time.sleep(1)
