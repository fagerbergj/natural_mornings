import json
import datetime
import time
import RPi.GPIO as GPIO
import numpy as np

GPIO.setmode(GPIO.BOARD)

def average_light_value (seconds=60):
    pin_to_circuit = 7

    results = np.empty(0)
    timeCalled = datetime.datetime.now().hour * 360 + datetime.datetime.now().second + datetime.datetime.now().minute * 60
    while (datetime.datetime.now().hour * 360 + datetime.datetime.now().second + datetime.datetime.now().minute * 60 < timeCalled + seconds ):
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

        results = np.append(results, count)

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
    dayEnum = dateTimeNow.today().strftime("%A").upper()
    day = data["config"][dayEnum]
    # if day is enabled
    if day['isEnabled']:
        activated = False
        # if light activated is true
        if day['lightActivated']:
            value = average_light_value(5)
            # if there is enough light and it is not night time (5am to 5pm)
            print(dateTimeNow.hour)
            activated = value < 200 and dateTimeNow.hour > 5 and dateTimeNow.hour < 17
            print(value)
            # read light sensor for 1 minuet
            # average result to set activated to true or not
        else:
            # sleep 1 minute
            time.sleep(6)
            # check to see if current time = time from config
            dateTimeNow = datetime.datetime.now()
            nowTimeInMin = dateTimeNow.minute + dateTimeNow.hour * 60
            activated = day['time'] == nowTimeInMin
        if activated:

            Motor1A = 16
            Motor1B = 18
            Motor1E = 22

            Motor2A = 23
            Motor2B = 21
            Motor2E = 19

            GPIO.setup(Motor1A,GPIO.OUT)
            GPIO.setup(Motor1B,GPIO.OUT)
            GPIO.setup(Motor1E,GPIO.OUT)

            GPIO.setup(Motor2A,GPIO.OUT)
            GPIO.setup(Motor2B,GPIO.OUT)
            GPIO.setup(Motor2E,GPIO.OUT)
            
            if day["playSound"]:
                # play sound
                print('Play sound')
            if day["openBlinds"]:
                # activate blinds motor
                print('Opening blinds')
                GPIO.output(Motor1A,GPIO.HIGH)
                GPIO.output(Motor1B,GPIO.LOW)
                GPIO.output(Motor1E,GPIO.HIGH)

                sleep(5)
                GPIO.output(Motor1E,GPIO.LOW)
            if day["openWindow"]:
                # activate window motor
                print('Opening window')
                GPIO.output(Motor2A,GPIO.HIGH)
                GPIO.output(Motor2B,GPIO.LOW)
                GPIO.output(Motor2E,GPIO.HIGH)

                sleep(5)
                GPIO.output(Motor2E,GPIO.LOW)
