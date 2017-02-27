from PyCRC.CRCCCITT import CRCCCITT
from PyCRC.CRC16 import CRC16

# outputs 21612
input = '12345'
print(CRCCCITT().calculate(input))

input = '9472'
print(CRCCCITT().calculate(input))

input = '23451'
print(CRCCCITT().calculate(input))
