#! /usr/bin/env python3

from time import sleep
# sleep(120)

import csv
import threading
from pitop.pma import SoundSensor
from pitop.pma import LightSensor
from pitop.miniscreen import UpButton, DownButton, SelectButton, CancelButton
from pitop.miniscreen import OLED
import datetime
import logging
import sys, errno

logging.basicConfig(handlers=[logging.StreamHandler(stream=sys.stdout)]
                    , format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%F %A %T", level=logging.DEBUG)
# logging.FileHandler(filename="sensor_box.log", encoding='utf-8',mode = "a+")
logging.debug("sensor box scrip running")
print("before initialization")
try:

    logging.debug(f"try to initialize OLED and Sensors")

    mini_screen = OLED()
    mini_screen.set_max_fps(1)
    mini_screen.draw_multiline_text("welcome to sensor box script. Press o to start recording enviroment", font_size=12)

except Exception as e:
    logging.exception("kaputt")
sys.exit(errno.EAGAIN)

sound_sensor = SoundSensor("A1")
light_sensor = LightSensor("A0")
select = SelectButton()
cancel = CancelButton()

logging.debug("starting idle phase")
recording = False


def readData():
    logging.debug("start recording")
    global recording
    with open('sensor_' + str(datetime.datetime.now()) + ".csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["time", "sound_sensor", "light_sensor"])
        while recording:
            writer.writerow([datetime.datetime.now(), sound_sensor.reading, light_sensor.reading])
            # print("add line to csv")
            sleep(0.1)


def start_recording():
    mini_screen.draw_multiline_text("----- recording ------ Press x to stop recording.", font_size=12)
    global recording
    recording = True
    t = threading.Thread(name='readData', target=readData)
    t.setDaemon(True)
    t.start()


def stop_recording():
    logging.debug("stop recording")
    mini_screen.draw_multiline_text("stopped recording. Press o to start recording.", font_size=12)
    global recording
    recording = False


cancel_pressed = False
select_pressed = False


def select_down():
    global select_pressed
    if select_pressed != select.is_pressed:  # state has changed
        select_pressed = select.is_pressed
        if select.is_pressed:
            return True
        else:
            return False


def cancel_down():
    global cancel_pressed
    if cancel_pressed != cancel.is_pressed:  # state has changed
        cancel_pressed = cancel.is_pressed
        if cancel.is_pressed:
            return True
        else:
            return False


state = 0
while True:

    if state == 0:  # idle (not recording) state
        if select_down():
            state = 1
            start_recording()
        elif cancel_down():
            state = 2
            mini_screen.draw_multiline_text("Are you sure you want to exit? Press x again to confirm.", font_size=12)
    if state == 1:  # recording state
        if select_down():
            pass
        elif cancel_down():
            state = 0
            stop_recording()
    if state == 2:  # are you sure you want to exit state
        if select_down():
            state = 0
            stop_recording()
        elif cancel_down():
            exit()