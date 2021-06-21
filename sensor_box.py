from pitop.pma import SoundSensor
from pitop.pma import LightSensor
from pitop.miniscreen import UpButton, DownButton, SelectButton, CancelButton
from time import sleep
import csv
import threading
from pitop.miniscreen import OLED
import datetime

print("sensor box scrip running")
sound_sensor = SoundSensor("A1")
light_sensor = LightSensor("A0")

mini_screen = OLED()
mini_screen.set_max_fps(1)
mini_screen.draw_multiline_text("welcome to sensor box script. Press o to start recording enviroment", font_size = 12)

up = UpButton()
down = DownButton()
select = SelectButton()
cancel = CancelButton()

recording = False

def readData():
    with open('sensor_'+str(datetime.datetime.now())+".csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["time", "sound_sensor","light_sensor"])
        while recording:
            writer.writerow([datetime.datetime.now(), sound_sensor.reading, light_sensor.reading])
            print("add line to csv")
            sleep(0.1)

def start_recording():
    mini_screen.draw_multiline_text("----- recording ------ Press x to stop recording.", font_size = 12)
    recording = True
    t = threading.Thread(name = 'readData', target = readData)
    t.setDaemon(True)
    t.start()

def stop_recording():
    mini_screen.draw_multiline_text("stopped recording. Press o to start recording.", font_size = 12)
    recording = False

exiting = False


while True:
    if cancel.is_pressed:
        print("cancel_pressed")
        if recording:#press cancel once (from running state)
            recording = False
            stop_recording()
            print("Cancel pressed")
        else:
            if exiting:# press cancel three times (from stopped state)
                exit()
            else:# press cancel twice (from stopped state)
                mini_screen.draw_multiline_text("are you sure you want to exit? Press x again to confirm.", font_size = 12)
                exiting = True
        sleep(1)
    if select.is_pressed:
        print("select_pressed")
        if exiting:# if we were in cancel twice state go back to cancel once state
            exiting = False
            stop_recording()
        elif not recording:# enter recording state from from cancel once state
            recording = True
            start_recording()
            print("Select pressed")
        sleep(1)
