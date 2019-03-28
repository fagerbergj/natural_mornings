import json
import datetime
import time
import RPi.GPIO as GPIO
import numpy as np

GPIO.setmode(GPIO.BOARD)

def day_to_index(argument):
    switcher = {
        'Monday': 0,
        'Tuesday': 1,
        'Wednesday': 2,
        'Thursday': 3,
        'Friday': 4,
        'Saturday': 5,
        'Sunday': 6
    }
    return switcher.get(argument, "nothing")

def average_light_value (seconds=60):
    pin_to_circuit = 7

    results = np.empty(0)
    timeCalled = datetime.datetime.now().second + datetime.datetime.now().minute * 60
    while (datetime.datetime.now().second + datetime.datetime.now().minute * 60 < timeCalled + seconds ):
        count = 0
    
        #Output on the pin for 
        GPIO.setup(pin_to_circuit, GPIO.OUT)
        GPIO.output(pin_to_circuit, GPIO.LOW)
        time.sleep(0.1)

        #Change the pin back to input
        GPIO.setup(pin_to_circuit, GPIO.IN)
    
        #Count until the pin goes high
        while (GPIO.input(pin_to_circuit) == GPIO.LOW):
            count += 1

        np.append(results, count)

    # GPIO.cleanup()
    print(results)
    return np.mean(results)



# While true
# while(true):
    # Pull config from files
with open('config.json') as json_file: 
    # Parse config into array 
    data = json.load(json_file)
    # get current day config
    dateTimeNow = datetime.datetime.now()
    dayIndex = day_to_index(dateTimeNow.today().strftime("%A"))
    day = data["config"][dayIndex]
    # if day is enabled
    if day['isEnabled']:
        triggered = False
        # if light activated is true
        if day['lightActivated']:
            value = average_light_value()
            triggered = value >= 200
            print(value)
            # read light sensor for 1 minuet
            # average result to set triggered to true or not
        else:
            # sleep 1 minuet
            time.sleep(6)
            # check to see if current time = time from config
            dateTimeNow = datetime.datetime.now()
            nowTimeInMin = dateTimeNow.minute + dateTimeNow.hour * 60
            triggered = day['time'] == nowTimeInMin
        if triggered:
            if day["playSound"]:
                # play sound
                pass
            if day["openBlinds"]:
                # activate blinds motor
                pass
            if day["openWindow"]:
                # activate window motor
                pass
