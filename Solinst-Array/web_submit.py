import httplib as http
import urllib
import os
import re
import datetime
import storage.database as lite
import ConfigParser

def file_list(datadir):
    filelist = []
    for files in os.listdir(datadir):
        matches = re.search("sensordata-[0-9]+\.sqlite", files)
        if (matches):
            filelist.append(files)
            
    return(filelist)

#Load config file
config_file = "solinst.ini"
if(not os.path.exists(config_file)):
    exit(-1)

Config = ConfigParser.ConfigParser()
Config.read(config_file)

DEBUG = Config.getboolean("general", "debug")
datadir = Config.get("general", "data_dir")
data_public = Config.get("web_submit", "data_public")
data_private = Config.get("web_submit", "data_private")

# Determine the name of the current database
today = datetime.datetime.today()
dbdate =  today.strftime('%Y%m%d')
db_filename = "sensordata-" + dbdate + ".sqlite"

if DEBUG: print("Today's database file: " + db_filename)

# Get list of database files
filelist = file_list(datadir)
for files in filelist:
    sensordb = lite.Database(datadir + files)

    datalist = sensordb.getUnsent()
    if(len(datalist) == 0):
        sensordb.close()
        # Rename file
        if(files != db_filename): 
            newfile = files[:-7] + "_done" + files[-7:]
            os.rename(datadir + files, datadir + newfile)
            if DEBUG: print("Rename old database file: " + newfile)
        continue

    for data in datalist:
        request = {
            'collect_date' : data[0],
            'dht_temp' : data[1],
            'dht_humid' : data[2],
            'soil_temp' : data[3],
            'soil_humid' : data[4],
            'sol_temp' : data[5],
            'sol_depth' : data[6]
        }
    
        conn = http.HTTPConnection("data.sparkfun.com")
        conn_line = "/input/" + data_public + "?private_key=" + data_private + "&" + urllib.urlencode(request)
        if DEBUG: print("Data URI: " + conn_line)
        
        conn.request("GET", conn_line)
        r1 = conn.getresponse()
#        print r1.read()
        conn.close()

        if DEBUG: print("Return code: " + r1.status)
        if(r1.status != 200):
            continue
        
#        conn.connect()
            
        sensordb.sentData(str(data[0]))
        if DEBUG: print("Sent data: " + str(data[0]))
    sensordb.close()
    if DEBUG: print("Close database: " + files)