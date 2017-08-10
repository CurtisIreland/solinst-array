import os
import re
import datetime
import json
import storage.database as lite
import ConfigParser

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def file_list(datadir):
    filelist = []
    for files in os.listdir(datadir):
        matches = re.search("sensordata-[0-9]+\.sqlite", files)
        if (matches):
            filelist.append(files)
            
    return(filelist)

def login_open_sheet(oauth_key_file, spreadsheet):
    """Connect to Google Docs spreadsheet and return the first worksheet."""
    try:
        scope =  ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
        gc = gspread.authorize(credentials)
        worksheet = gc.open(spreadsheet).sheet1
        return worksheet
    except Exception as ex:
        print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)


# if DEBUG: print("Rename old database file: " + newfile)

#Load config file
config_file = "/usr/local/solinst/solinst.ini"
if(not os.path.exists(config_file)):
    print("ERROR: Cannot find configuration file.")
    exit(-1)

Config = ConfigParser.ConfigParser()
Config.read(config_file)

DEBUG = Config.getboolean("general", "debug")
datadir = Config.get("general", "data_dir")
array_id = Config.get("general", "array_id")
GDOCS_OAUTH_JSON = Config.get("web_submit", "auth_file")
GDOCS_SPREADSHEET_NAME = Config.get("web_submit", "data_file")

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
        if DEBUG: print('Logging sensor measurements to {0}'.format(GDOCS_SPREADSHEET_NAME))

        worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME)
        worksheet.append_row((array_id, str(data[0]), str(data[1]), str(data[2]), str(data[3]), str(data[4]), str(data[5]), str(data[6]), str(data[7]), datetime.datetime.now()))        

        sensordb.sentData(str(data[0]))
        if DEBUG: print("Sent data: " + str(data[0]))
    sensordb.close()
    if DEBUG: print("Close database: " + files)
