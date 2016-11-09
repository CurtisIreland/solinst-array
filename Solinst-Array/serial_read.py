import serial
import time
import storage.database as lite
import datetime

#    port='/dev/ttyAMA0',\
ser = serial.Serial(
    port='COM3',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

print("connected to: " + ser.portstr)

# Get the serial number of this raspberry pi
##serial = get_serial();
#serial = "pc-test"

datadir = "data/"
vals = []

time.sleep(2)
ser.write("\n")
time.sleep(2)

line = ser.readline().strip()

vals = line.split(',')

ser.close()


# Store data into local database file
# Determine the name of the database
today = datetime.datetime.today()
dbdate =  today.strftime('%Y%m%d')
db_filename = "sensordata-" + dbdate + ".sqlite"

sensordb = lite.Database(datadir + db_filename)
sensordb.addLine(vals)

sensordb.close()
