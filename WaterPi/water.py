#Import the needed modules and sensors
import time
import datetime
import sys
import board
import busio
import RPi.GPIO as GPIO
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1115(i2c)
chan1 = AnalogIn(ads, ADS.P0)
#Import the weatherdata saved by weather.py
#The variable it will look for later on is called rain
#Note: rain=1 for no rain and rain=0 for rain
sys.path.append('/home/pi/WaterPi/weatherdata.py')
from weatherdata import *

#This function tests the mositure of the soil to see if it is below a certain value (17600)
def moisture():
    if chan1.value <= 17600:
        return 0
    else:
        return 1

#This function tests the mositure of the soil to see if it is above a certain value (19000)
def start():
    if chan1.value >= 19000:
        return 1
    else:
        return 0

#This function waters the plant
def water():
    #Writes that it started watering to log, with time, date, mositure level, and it records the total from a call to the mositure() function
    log.write(str(datetime.datetime.now()) + "-Start-Watering-" + "moisture=" + str(chan1.value) + "--tot=" + str(moisture()) + "\n")

    ###############
    #Watering Loop#
    ###############

    #This loop will water the plant until the mositure goes below a certain point (17600)
    while moisture() == 1:
        print("Watering")
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(27, GPIO.OUT)
        GPIO.output(27, GPIO.HIGH)
        GPIO.output(27, GPIO.LOW)
        time.sleep(.75)
    GPIO.output(27, GPIO.HIGH)
    GPIO.cleanup()
    return 1

#Starts here
if __name__ == "__main__":
    #Execute the code under try:
    try:
        #Opens log
        log = open("/home/pi/WaterPi/logs/moisture","a")

        #Checks if there is rain currently or in the furure and checks the mositure if it is above a certain point (19000)
        if (rain == 1 and start() == 1):

            ##################
            #Decides to Water#
            ##################

            #Writes that the plant needs watering to the log, with time, date, mositure level, the total from a call to the mositure() function, and the value of rain 
            log.write(str(datetime.datetime.now()) + "-Needs-Watering-" + "moisture="  + str(chan1.value) + "--tot=" + str(moisture()) + "--rain=" + str(rain) + "\n")

            #Calls the water() function to water
            water()

            
        else:
            #Condition for watering failed, no water
            print("No Water")

            #Writes that the plant does not need water to the log, with time, date, mositure level, the total from a call to the mositure() function, and the value of rain
            log.write(str(datetime.datetime.now()) + "-No-Watering-" + "moisture="  + str(chan1.value) + "--tot=" + str(moisture()) + "--rain=" + str(rain) + "\n")

        #Writes that it finished running to the log, with time, date, mositure level, the total from a call to the mositure() function, and the value of rain
        log.write(str(datetime.datetime.now()) + "-Done-Watering-" + "moisture="  + str(chan1.value) + "--tot=" + str(moisture()) + "--rain=" + str(rain) + "\n")

        #Closes log
        log.close()

    #For stopping while debugging
    except KeyboardInterrupt:
        print("Exiting")
        GPIO.cleanup()