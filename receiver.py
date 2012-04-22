import serial
import time
import math

eeprom_size = 1024
group_size = 9 # a group is a sign byte plus the normal bytes that follow it

ser = serial.Serial("/dev/tty.usbserial-A80090rN", 19200)
f = open("camera_data.txt", "w")
time.sleep(2) # need to wait a bit because it takes time to open serial port
ser.write("hello") # handshake to tell Arduino to send EEPROM contents

num_of_photos = (eeprom_size / group_size) * (group_size - 1) + (eeprom_size - (eeprom_size / group_size) * group_size - 1)
for i in range(num_of_photos):
  d = ser.readline()
  f.write(d)
ser.close()
f.close()