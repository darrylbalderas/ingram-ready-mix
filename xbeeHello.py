import serial
import glob
import sys
import requests

def xbee_Usb_Port():
    ports = glob.glob('/dev/tty[A-Za-z]*')
    result = []
   
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except( OSError, serial.SerialException):
            pass
    print(result)
    return result[1]

system_name = sys.platform
baud_Rate = 9600
port_Name = xbee_Usb_Port()
print (port_Name)
xbee_Bravo = serial.Serial(port_Name, baud_Rate, timeout=0.5)
print (port_Name)
xbee_Bravo.write('Hello from Raspberry pi')
while True:
    try:
        xbee_Bravo.write('Hello User')
        incoming = xbee_Bravo.readline().strip()
        print('Received Data : ' + incoming)
    except KeyboardInterrupt:
        break
        pass


xbee_Bravo.close()
