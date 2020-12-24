# pylight.py
app = "PyLight"
version = "v1.0"
#
import requests
import json
import sys
import os
from datetime import datetime # - for logging timestamps
#
# Get information from environment_settings.py
from environment_settings import log_settings
from environment_settings import debug_settings
from environment_settings import database_settings
from environment_settings import location
from environment_settings import hue
#
# debug function
def write_to_debug_file(message,debug=debug_settings.get("debug"),path_debugfile=os.getcwd() + debug_settings.get("path_debugfile")):
    # def to write debug info to the debug file
    if debug == True:
        debugfile = open(path_debugfile, 'a+')
        logtime = str(datetime.now())
        debugfile.write(logtime + "; app: " + app + ", Message: " + message + '\n')
        debugfile.close()
        # un-comment line below to print debug-logs in CLI
        #print(logtime + "; apiflex-app: " + apiflex_app + ", Message: " + message)
#
# log function
def write_to_log_file(loginput,path_logfile=os.getcwd() + log_settings.get("path_logfile")):
    # def to write logs to the logfile
    logfile = open(path_logfile, 'a+')
    logtime = str(datetime.now())
    logprefix = logtime + "; app: " + app + ", "
    logsuffix = ", end"
    logfile.write(logprefix + loginput + logsuffix + '\n')
    logfile.close()
    write_to_debug_file("log added to file " + path_logfile + " at " + logtime)
#
# sunrise-sunset function
def get_sunrise_sunset_api():
    url = "https://api.sunrise-sunset.org/json"
        data = dict()
        data["lat"] = location.get("lat")
        data["lng"] = location.get("lng")
        data["date"] = "today"
        write_to_debug_file("Data to use in API call: " + str(data))
        write_to_debug_file("Starting API call to " + url)
        resp = requests.get(url,data=data)
        if resp.ok == True:
           print(resp.text)
        else:
           write_to_log_file("ERROR: API call to " + url + "was not successful. HTTP Response code: " + str(resp.status_code) + ": " + resp.reason)
           sys.exit()
#
# main program
if __name__ == "__main__":
    # get sunrise and sunset times from https://sunrise-sunset.org/api
    get_sunrise_sunset_api()

