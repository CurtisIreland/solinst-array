import serial
import time

#    port='/dev/ttyAMA0',\
ser = serial.Serial(
    port='COM7',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

print("connected to: " + ser.portstr)

try:
    vals = []
    while True:
        ser.write("\n")
        time.sleep(10)
    
        line = ser.readline().strip()
        vals = line.split(',')

except KeyboardInterrupt:
    print 'Exiting'

ser.close()