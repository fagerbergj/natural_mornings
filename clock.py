import json
import datetime
import time
import RPi.GPIO as GPIO
import numpy as np
import pygame
import threading
import winsound

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

    print(results)
    return np.mean(results)


class SoundThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run (self):
          play_sound()

class BlindsThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run (self):
          open_blinds()

class WindowThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run (self):
          open_window()

def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load("rainforest_ambience-GlorySunz-1938133500.wav")
    pygame.mixer.music.play()
    print('Play sound')
    


def open_blinds():
    print('Opening blinds')
    Motor1A = 16
    Motor1B = 18
    Motor1E = 22

    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)

    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

    time.sleep(5)
    GPIO.output(Motor1E,GPIO.LOW)

def open_window():
    print('Opening window')
    Motor2A = 23
    Motor2B = 21
    Motor2E = 19

    GPIO.setup(Motor2A,GPIO.OUT)
    GPIO.setup(Motor2B,GPIO.OUT)
    GPIO.setup(Motor2E,GPIO.OUT)

    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)

    time.sleep(5)
    GPIO.output(Motor2E,GPIO.LOW)

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
        # GPIO.setmode(GPIO.BOARD)
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
            # check to see if current time = time from config
            dateTimeNow = datetime.datetime.now()
            nowTimeInMin = dateTimeNow.minute + dateTimeNow.hour * 60
            print("time " + str(nowTimeInMin) + " vs " + str(day['time']))
            activated = day['time'] == nowTimeInMin
        if activated:
            if day["playSound"]:
                # play sound
                print("Play Sound")
                #SoundThread().start()
                #play_sound()
            if day["openBlinds"]:
                # activate blinds motor
                print("Open Blinds Thread Spawn")
                BlindsThread().start()
            if day["openWindow"]:
                # activate window motor
                print("Open Window Thread Spawn")
                WindowThread().start()

        # GPIO.cleanup()
