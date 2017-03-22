import sys
import os
from time import sleep
import glob
import serial
from time import time
from threading import Thread
from threading import Lock
from threading import Event
import RPi.GPIO as gpio
from transceiver import Transceiver

flow = 23
level = 24
rain = 18
max_time = 30 * 60
gpio.setmode(gpio.BCM)
gpio.setup(flow,gpio.IN)
gpio.setup(level,gpio.IN)
gpio.setup(rain,gpio.IN)

def xbee_usb_port():
    if sys.platform.startswith('linux'):
        ports = glob.glob('/dev/ttyU*')
    if len(ports) != 0:
        result = []
        for port in ports:
            try:
                ser = serial.Serial(port)
                ser.close()
                result.append(port)
            except( OSError, serial.SerialException):
                pass
        return result[0]
    else:
        return None

def check_rainguage():
    return gpio.input(rain)

def check_flowsensor():
    return gpio.input(flow)

def check_levelsensor():
    return gpio.input(level)

def get_tick():
    previous_state = 0
    previous_time = time()
    collection_duration = 2
    while (time()-previous_time) <= collection_duration:
        current_state = check_rainguage()
        if current_state  > previous_state:
            previous_state = current_state
            while current_state == previous_state:
                current_state = check_rainguage()
            return 1
    return 0

def get_total_rainfall():
    counter = 0
    rainfall = 2.769
    ticking = 0
    previous_time = time()
    while (time()-previous_time) <= max_time:
        ticking = get_tick()
        if not ticking:
            break
        else:
            rainfall += 2.769
    return rainfall

def detect_outfall(xbee,lock,event):
    while not event.isSet():
        while check_flowsensor() and check_levelsensor():
            print("outfall is occuring")
            lock.acquire()
            xbee.send_message('out\n')
            sleep(0.5)
            if xbee.receive_message() == 'oyes':
                print("received outfall confirmation")
                lock.release()
                break
            lock.release()
        
def detect_rainfall(xbee,lock,event):
    while not event.isSet():
        if get_tick():
            print("rainguage invoked")
            lock.acquire()
            create_trigger(xbee)
            lock.release()
            send_data(xbee,lock)
            print("sent the pool and rain data")
        sleep(0.25)

def create_trigger(xbee):
    message = ""
    while not message == "tyes":
        xbee.send_message('tri\n')
        message = xbee.receive_message()

def send_data(xbee,lock):
    rain_val = rain_gauge.get_total_rainfall()
    pool_val = 8
    pool_val = 'p' + str(pool_val) + '\n'
    rain_val = 'r' + str(rain_val) + '\n'
    message = ""
    lock.acquire()
    create_trigger(xbee)
    while not message == "ryes":
        xbee.send_message(rain_val)
        sleep(0.5)
        xbee.send_message(pool_val)
        sleep(0.5)
        message  = xbee.receive_message()
    lock.release()

def main():
    lock = Lock()
    event = Event()
    port = xbee_usb_port()
    if port != None:
        try:
            charlie_xbee = Transceiver(9600,port)
            thread1 = Thread(target = detect_outfall, args = (charlie_xbee,lock,event, ))
            thread2 = Thread(target = detect_rainfall, args = (charlie_xbee,lock,event,))
            thread1.start()
            thread2.start()
        except KeyboardInterrupt:
            event.set()
            print("Ending the program")
            thread1.join()
            thread2.join()
    else:
        print('Missing xbee device')

if __name__ == "__main__":
    main()
