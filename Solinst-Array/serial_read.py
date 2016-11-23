import serial
import time
import storage.database as lite
import datetime
import os
import ConfigParser

# Load configuration
config_file = "solinst.ini"
if(not os.path.exists(config_file)):
    exit(-1)

Config = ConfigParser.ConfigParser()
Config.read(config_file)

DEBUG = Config.getboolean("general", "debug")
datadir = Config.get("general", "data_dir")
serial_port = Config.get("serial_read", "serial_port")
serial_baud = Config.getint("serial_read", "serial_baud")

#    port='/dev/ttyAMA0',\
ser = serial.Serial(
    port=serial_port,\
    baudrate=serial_baud,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

print("connected to: " + ser.portstr)

# Get the serial number of this raspberry pi
##serial = get_serial();
#serial = "pc-test"

vals = []

time.sleep(2)
ser.write("\n")
time.sleep(12)

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
