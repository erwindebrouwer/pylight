# pylight.py
app = "PyLight"
version = "v1.1"
#
# import modules
import requests
import json
import sys
import os
from datetime import datetime # - for logging timestamps
#
# Disable requests-module insecure request warning!
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
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
        #print(logtime + "; app: " + app + ", Message: " + message)
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
    data["formatted"] = 0
    write_to_debug_file("Data to use in API call: " + str(data))
    write_to_debug_file("Starting API call to " + url)
    resp = requests.get(url,data)
    if resp.ok == True:
        write_to_log_file("OK: API call to " + url + " was successful. HTTP Response code: " + str(resp.status_code) + ": " + resp.reason)
        write_to_debug_file("OK: API call to " + url + " was successful. HTTP Response code: " + str(resp.status_code) + ": " + resp.reason)
        return resp
    else:
        write_to_log_file("ERROR: API call to " + url + " was not successful. HTTP Response code: " + str(resp.status_code) + ": " + resp.reason)
        write_to_debug_file("ERROR: API call to " + url + " was not successful. HTTP Response code: " + str(resp.status_code) + ": " + resp.reason)
        sys.exit()
#
# parsing results function
def parse_results(api_response):
    parsed_datetimes = dict()
    parsed_datetimes["sunrise"] = datetime.strptime(json.loads(api_response.text)["results"]["sunrise"],"%Y-%m-%dT%H:%M:%S%z")
    write_to_debug_file("Sunrise date and time parsed to " + str(parsed_datetimes["sunrise"]))
    parsed_datetimes["sunset"] = datetime.strptime(json.loads(api_response.text)["results"]["sunset"],"%Y-%m-%dT%H:%M:%S%z")
    write_to_debug_file("Sunset date and time parsed to " + str(parsed_datetimes["sunset"]))
    return parsed_datetimes
#
# scheduling commands in HUE controller to switch_on and switch_off light(s)
def schedule_commands(parsed_datetimes):
    # set datetime suitable for use
    print("suitable times?")
    print(str(parsed_datetimes["sunrise"]))
    sunrise_time = str(parsed_datetimes["sunrise"])
    sunrise_time = sunrise_time[0:-6].replace(" ","T")
    print(sunrise_time)
    print(str(parsed_datetimes["sunset"]))
    sunset_time = str(parsed_datetimes["sunset"])
    sunset_time = sunset_time[0:-6].replace(" ","T")
    print(sunset_time)
    #
    # GET hue options from environment_settings
    hue_bridge_ip = str(hue.get("ip"))
    hue_bridge_port = str(hue.get("port"))
    hue_bridge_key = str(hue.get("key"))
    hue_bridge_lights = hue.get("lights")
    hue_bridge_brightness = str(hue.get("brightness"))
    write_to_debug_file("Got all HUE options from environment_settings file")
    write_to_debug_file("Lights to turn OFF and ON are: " + str(hue_bridge_lights) + " with a total amount of " + str(len(hue_bridge_lights)))
    # GET all lights to lookup id's
    url_get_lights = "https://"+hue_bridge_ip+":"+hue_bridge_port+"/api/"+hue_bridge_key+"/lights"
    get_lights_response = requests.get(url_get_lights, verify=False)
    get_lights_response_dict = json.loads(get_lights_response.text)
    write_to_debug_file("Finished downloading all device ID's and names from HUE controller with a total amount of " + str(len(get_lights_response_dict)))
    # resolve light names to ID's
    hue_bridge_lights_id = list()
    for name in hue_bridge_lights:
        for item in get_lights_response_dict:
            if name in get_lights_response_dict[item]["name"]:
                hue_bridge_lights_id.append(item)
    # schedule commands in Hue controller
    for light_id in hue_bridge_lights_id:
        url_post_command = "https://"+hue_bridge_ip+":"+hue_bridge_port+"/api/"+hue_bridge_key+"/schedules"
        # sunrise - switch OFF
        body_text_sunrise = '{"command":{"address":"/api/'+hue_bridge_key+'/lights/'+light_id+'/state","body":{"on":false,"bri":'+hue_bridge_brightness+'},"method":"PUT"},"time":"'+sunrise_time+'"}'
        response_sunrise = requests.post(url_post_command,data=body_text_sunrise,verify=False)
        print(response_sunrise.text)
        # sunset - switch ON
        body_text_sunset = '{"command":{"address":"/api/'+hue_bridge_key+'/lights/'+light_id+'/state","body":{"on":true,"bri":'+hue_bridge_brightness+'},"method":"PUT"},"time":"'+sunset_time+'"}'
        response_sunset = requests.post(url_post_command,data=body_text_sunset,verify=False)
        print(response_sunset.text)
#
#
# main program
if __name__ == "__main__":
    # get sunrise and sunset times from https://sunrise-sunset.org/api
    api_response = get_sunrise_sunset_api()
    parsed_datetimes = parse_results(api_response)
    schedule_commands(parsed_datetimes)
    #
    # printing some things
    print("Sunrise is at " + str(parsed_datetimes["sunrise"].hour) + ":" + str(parsed_datetimes["sunrise"].minute) + " today.")
    print("Sunset is at " + str(parsed_datetimes["sunset"].hour) + ":" + str(parsed_datetimes["sunset"].minute) + " today.")
#
# end of script