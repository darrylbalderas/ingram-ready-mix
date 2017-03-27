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


# class Job(object):
#     def __init__(self, priority, message):
#         self.priority = priority
#         self.description = message
#     def __cmp__(self, other):
#         return cmp(self.priority, other.priority)

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

def send_outfall(out_queue,send_queue):
    message = ""
    while message != "oyes":
        if len(out_queue) != 0:#not out_queue.empty():
            message = out_queue.pop(0)
            # message = out_queue.get()
            # out_queue.task_done()
            # print("in send outfall")
            # print(message)
        else:
            send_queue.append("out")
            # send_queue.put("out")
            sleep(0.5)

def detect_outfall(out_queue,send_queue):
    while True:
        if check_flowsensor() and check_levelsensor():
            print("outfall is occuring")
            send_outfall(out_queue,send_queue)
            print("got outfall confirmation")
            sleep(200)
        

def detect_rainfall(tri_queue,send_queue,):
    while True:
        if get_tick():
            print("rainguage invoked")
            create_trigger(tri_queue,send_queue)
            send_data(tri_queue, send_queue)
            print("sent the pool and rain data")


def create_trigger(tri_queue, send_queue):
    message = ""
    while message != "tyes":
        if len(tri_queue) != 0: #not tri_queue.empty():
            message = tri_queue.pop(0)
            # message = tri_queue.get()
            # tri_queue.task_done()
        else:
            send_queue.append("tri")
            # send_queue.put("tri")
            sleep(0.5)

def send_data(tri_queue,send_queue):
    rain_val = get_total_rainfall()
    pool_val = 8.0
    pool_val = 'p' + str(pool_val)
    rain_val = 'r' + str(rain_val)
    message = ""
    while message != "ryes":
        if len(tri_queue) != 0:#not tri_queue.empty():
            message = tri_queue.pop(0)
            # message = tri_queue.get()
            # tri_queue.task_done()
        else:
            # send_queue.put(rain_val)
            # send_queue.put(pool_val)
            send_queue.append(rain_val)
            send_queue.append(pool_val)
            sleep(0.5)

def transmission(xbee):
    while True:
        xbee.receive_message()
        xbee.send_message()

def main():
    # send_queue= Queue.Queue()
    # out_queue = Queue.Queue()
    # tri_queue = Queue.Queue()
    # data_queue = Queue.Queue()
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
