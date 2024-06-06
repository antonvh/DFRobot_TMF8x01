# -*- coding:utf-8 -*-

'''
  @file demo_get_distance.py
  @brief Get measurement data by PROXIMITY and DISTANCE hybrid mode.
  @note  TMF8801 only suport one mode, PROXIMITY and DISTANCE hybrid mode.
  @n 
  @n --------------------------------------------------------------------------------|
  @n |  Type     |   suport ranging mode     |  ranging ranges |  Accuracy           |
  @n |---------------------------------------|-----------------|---------------------|
  @n |  TMF8801  | PROXIMITY and DISTANCE    |                 |  20~100mm: +/-15mm  |
  @n |           |  hybrid mode(only one)    |    20~240cm     |  100~200mm: +/-10mm |
  @n |           |                           |                 |   >=200: +/-%5      |
  @n |---------------------------------------|-----------------|---------------------|
  @n 
  @n hardware conneted table:
  @n ------------------------------------------
  @n |  TMF8801  |            MCU              |
  @n |-----------------------------------------|
  @n |    sda    |       Pin 5                 |
  @n |    scl    |       Pin 4                 |
  @n |-----------------------------------------|
  @n |    EN     |   not connected, floating   |
  @n |-----------------------------------------|
  @n |    INT    |   not connected, floating   |
  @n |-----------------------------------------|
  @n |    PIN0   |   not connected, floating   |
  @n |-----------------------------------------|
  @n |    PIN1   |    not connected, floating  |
  @n |-----------------------------------------|
  @n
  @Copyright   Antons Mindstorms
  @license     The MIT License (MIT)
  @author Antons Mindstorms
  @version  V1.0
  @date  2024
'''

from DFRobot_TMF8x01 import DFRobot_TMF8801 as tmf8801
from machine import Pin, I2C
import time

i2c1 = I2C(1, scl=Pin(4), sda=Pin(5), freq=400_000)
addr = i2c1.scan()
if addr:
    print("Found sensor at",hex(*addr))
    
tof = tmf8801(i2c1)


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
#tof.start_measurement(calib_m = tof.eMODE_CALIB, mode = tof.ePROXIMITY)

while True:
  if(tof.is_data_ready() == True):
    print("Distance = %d mm"%tof.get_distance_mm())
  #time.sleep(2)


