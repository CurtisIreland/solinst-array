import serial, time

ser = serial.Serial(
    port='/dev/ttyAMA0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)

vals = []
while True:
    ser.write("a")
    print("-")
    time.sleep(10)

    line = ser.readline().strip()
    print(line)

    vals = line.split(',')
    print(vals)

ser.close()