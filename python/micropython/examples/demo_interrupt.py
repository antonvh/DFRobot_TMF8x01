# -*- coding:utf-8 -*-

'''
  @file demo_interrupt.py
  @brief If you enable INT pin, MCU will capture a interrupt signal when the measure is completed.
  @n You can attach the INT pin of TMF8x01 to MCU external interrupt pin.
  @n 
  @n Ranging mode configuration table: 
  @n --------------------------------------------------------------------------------|
  @n |  Type     |   suport ranging mode     |  ranging ranges |  Accuracy           |
  @n |---------------------------------------|-----------------|---------------------|
  @n |  TMF8801  | PROXIMITY and DISTANCE    |                 |  20~100mm: +/-15mm  |
  @n |           |  hybrid mode(only one)    |    20~240cm     |  100~200mm: +/-10mm |
  @n |           |                           |                 |   >=200: +/-%5      |
  @n |---------------------------------------|-----------------|---------------------|
  @n 
  @n hardware conneted table:
  @n -------------------------------------------------------
  @n |  TMF8x01  |            MCU                           |
  @n |------------------------------------------------------|
  @n |    scl    |       ESP32 Pin 2                      |
  @n |------------------------------------------------------|
  @n |    sda    |       ESP32 Pin 26                      |
  @n |------------------------------------------------------|
  @n |    EN     |   not connected, floating                |
  @n |------------------------------------------------------|
  @n |    INT    |   ESP32 Pin 27   |
  @n |------------------------------------------------------|
  @n |    PIN0   |   not connected, floating                |
  @n |------------------------------------------------------|
  @n |    PIN1   |    not connected, floating               |
  @n |------------------------------------------------------|
  @n
  @n
  @Copyright   Copyright (c) 2024 Anton Vanhoucke
  @license     The MIT License (MIT)
  @version  V1.0
  @date  2021-04-06
  @url https://github.com/DFRobot/DFRobot_TMF8x01
'''

from DFRobot_TMF8x01 import DFRobot_TMF8801 as tmf8801
from machine import Pin, I2C
import time

i2c1 = I2C(1, scl=Pin(2), sda=Pin(26), freq=400_000)
interrupt_pin = Pin(27)
addr = i2c1.scan()
if addr:
    print("Found sensor at",hex(*addr))
    
tof = tmf8801(i2c1)

irqFlag = False

def notify(pin):
  global irqFlag
  irqFlag = True
  
interrupt_pin.irq(handler=notify, trigger=Pin.IRQ_FALLING)

print("Initialization ranging sensor TMF8x01......", end = " ")
while(tof.begin() != 0):
  print("Initialization failed")
  time.sleep(1)
print("Initialization done.")

print("Software Version: ", end=" ")
print(tof.get_software_version())
print("Unique ID: %X"%tof.get_unique_id())
print("Model: ", end=" ")
print(tof.get_sensor_model())

'''Enable INT pin to check measurement data. Sending a low signal to host if measurement distance completed.'''
tof.enable_int_pin()


'''
@brief Config measurement params to enable measurement. Need to call stop_measurement to stop ranging action.
@param calib_m: Is an enumerated variable of , which is to config measurement cailibration mode.
@n     eMODE_NO_CALIB  :          Measuring without any calibration data.
@n     eMODE_CALIB    :          Measuring with calibration data.
@n     eMODE_CALIB_AND_ALGOSTATE : Measuring with calibration and algorithm state.
@param mode : the ranging mode of TMF8701 sensor.
@n     ePROXIMITY: Raing in PROXIMITY mode,ranging range 0~10cm
@n     eDISTANCE: Raing in distance mode,ranging range 10~60cm
@n     eCOMBINE:  Raing in PROXIMITY and DISTANCE hybrid mode,ranging range 0~60cm
@return status:
@n      false:  enable measurement failed.
@n      true:  enable measurement sucess.
'''
tof.start_measurement(calib_m = tof.eMODE_CALIB)
#tof.start_measurement(calib_m = tof.eMODE_CALIB, mode = tof.ePROXIMITY);

while True:
  #print(irqFlag)
  if irqFlag == True:
    irqFlag = False
    if(tof.is_data_ready() == True):
        print("Distance = %d mm"%tof.get_distance_mm())
  #time.sleep(0.5)


