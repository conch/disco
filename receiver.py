import serial
import time

ser = serial.Serial("/dev/tty.usbserial-A80090rN", 19200)
f = open("camera_data.txt", "w")
time.sleep(2) # need to wait a bit because it takes time to open serial port
ser.write("hello") # handshake to tell Arduino to send EEPROM contents

for i in range(1024 / 2):
  d = ser.readline()
  f.write(d)
ser.close()
f.close()