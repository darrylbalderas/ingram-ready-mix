import sys
import os
from time import sleep
import glob
import serial
from time import time
from threading import Thread
import RPi.GPIO as gpio
from transceiver import Transceiver
from multiprocessing import Process
import Queue
import random

flow = 20
level = 16
rain = 12
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

def empty_queue(q):
    while not q.empty():
        q.pop(0)

def send_outfall(out_queue,send_queue):
    message = ""
    flag = False
    send_flag = True
    while not flag:
        if len(out_queue) != 0:
            message = out_queue.pop(0)
            if message == "oyes":
                flag = True
            else:
                send_flag = True
        elif send_flag:
            if not "out" in send_queue: 
                send_queue.append("out")
                send_flag = False

def detect_outfall(out_queue,send_queue):
    while True:
        if check_flowsensor() and check_levelsensor():
            send_outfall(out_queue,send_queue)
        
def detect_rainfall(tri_queue,send_queue,):
    while True:
        if get_tick():
            create_trigger(tri_queue,send_queue)
            send_data(tri_queue, send_queue)

def create_trigger(tri_queue, send_queue):
    message = ""
    flag = False
    send_flag = True
    while not flag:
        if len(tri_queue) != 0:
            message = tri_queue.pop(0)
            if message == "tyes":
                flag = True
            else:
                send_flag = True
        elif send_flag:
            if not "tri" in send_queue:
                send_queue.append("tri")
                send_flag = False

def send_data(tri_queue,send_queue):
    rain_val = get_total_rainfall()
    pool_val = 8.0
    pool_val = 'p' + str(pool_val)
    rain_val = 'r' + str(rain_val)
    message = ""
    flag = False
    send_flag = True
    while not flag:
        if len(tri_queue) != 0:
            message = tri_queue.pop(0)
            if message == "ryes":
                flag = True
            else:
                send_flag = True
        elif send_flag:
            send_queue.append(rain_val)
            send_queue.append(pool_val)
            send_flag = False

def transmission(xbee):
    while True:
        xbee.receive_message()
        xbee.send_message()

def main():
    send_queue= []
    out_queue = []
    tri_queue = []
    data_queue = []
    port = xbee_usb_port()
    if port != None:
        try:
            charlie_xbee = Transceiver(9600,port,out_queue,tri_queue,data_queue,send_queue)
            print("starting threads")
            t = Thread(target = detect_rainfall, args = (tri_queue,send_queue,))
            t.start()
            t1 = Thread(target = transmission, args = (charlie_xbee,))
            t1.start()
            detect_outfall(out_queue,send_queue)
        except KeyboardInterrupt:
            print("Ending the program")
            t.join()
            t1.join()
    else:
        print('Missing xbee device')

if __name__ == "__main__":
    main()
