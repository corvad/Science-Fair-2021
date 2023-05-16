#Import the needed modules
from xml.etree import ElementTree
import requests
import json
import time
import datetime
import sys
#Import the configuration file
sys.path.append('/var/www/html')
from config import *

#This function checks the current weather
def weather():
    ##############################
    #Current Rain Query and Parse#
    ##############################

    #Construct the current rain data query
    curl = "https://api.openweathermap.org/data/2.5/weather?q=" + zip + ",US&appid=" + apikey + "&mode=xml"

    #Query the current rain data
    cresponse = requests.get(curl)
    
    #Parse the result to get the current precipitation and save it
    rpxml = cresponse.content
    ctree = ElementTree.fromstring(rpxml)
    crain = str(ctree.find('precipitation').get('mode'))

    #############################
    #Future Rain Query and Parse#
    #############################

    #Construct the future rain data query
    furl = "https://api.openweathermap.org/data/2.5/forecast?zip=" + zip + "&appid=" + apikey
    
    #Query the future rain chance data
    fresponse = (requests.get(furl)).json()
    
    #Parsing the data and saving it to see if it might rain in the days to come
    frain = 0
    for x in range(18):
        frain = frain + (fresponse['list'][x]['pop'])

    ###################################
    #Check the Current and Future Rain#
    ###################################

    #Conditional to check whether it is raining or if it will rain in the future
    if(crain == "no"):
        #continue
        if(frain <= .75):
            return 1
        else:
            return 0
    else:
        return 0

#Starts here
if __name__ == "__main__":
    #Calls function weather(), which checks the current rain conditions
    rain = str(weather())

    #Note: rain=1 for no rain and rain=0 for rain

    #Writes the value of rain to a file for water.py to use, and writes data to log with date and time
    weatherfile = open("/home/pi/WaterPi/weatherdata.py", "w")
    weatherfile.write("rain = " + rain)
    weatherfile.close()
    log = open("/home/pi/WaterPi/logs/weather","a")
    log.write(str(datetime.datetime.now()) + "---" + "rain=" + rain + "\n")
    log.close()