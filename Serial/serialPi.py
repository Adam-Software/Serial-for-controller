#!/usr/bin/python3
#-*- coding: utf-8 -*-

#https://docs.python.org/3/library/ctypes.html

import sys
import time
import ctypes 
import struct
import os

import numpy.ctypeslib as ctl
import numpy as np
from numpy.ctypeslib import ndpointer

# checking the bit depth of the operating system
is64bit = struct.calcsize('P') * 8 == 64

# path
path = os.path.dirname(os.path.realpath(__file__))

# loading the library depending on the architecture of the operating system
if(is64bit):
    serial = ctypes.CDLL(os.path.join(path, 'serial_aaarch64.so'))
else:
    serial = ctypes.CDLL(os.path.join(path, 'serial_armv71.so'))
 
# Указываем, что функция возвращает int
serial.serialOpen.restype = ctypes.c_int
serial.serialClose.restype = ctypes.c_void_p
serial.serialDataAvail.restype = ctypes.c_int
serial.send.restype = ctypes.c_void_p

# Указываем, что функция возвращает char *
serial.readfrom.restype = ctypes.c_char_p
serial.readdata.restype = ctypes.c_char_p
serial.serialPrint.restype = ctypes.c_void_p

# Указываем, что функция принимает аргумент
serial.serialOpen.argtypes = [ctypes.POINTER(ctypes.c_char),ctypes.c_int, ]
serial.serialClose.argtypes = [ctypes.c_int]
serial.serialDataAvail.argtypes = [ctypes.c_int]
serial.send.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_ubyte),ctypes.c_uint,]
serial.readfrom.argtypes = [ctypes.c_int,ctypes.c_char,ctypes.c_int,]
serial.readdata.argtypes = [ctypes.c_int,ctypes.c_char,ctypes.c_int,ctypes.c_int,]
serial.serialPrint.argtypes = [ctypes.c_int,ctypes.POINTER(ctypes.c_char) ]

class SerialU:
    def __init__(self, com, port):
        self.port = serial.serialOpen(com.encode('utf-8'), port)

    def close(self):
        serial.serialClose(self.port)        

    def read(self, symbol, time, buffer):
        return serial.readdata(self.port, symbol.encode('utf-8'), time, buffer).decode('utf-8')

    def readByte(self, symbol, time, buffer):
        return serial.readdata(self.port, symbol.encode('utf-8'), time, buffer)

    def readf(self, symbol, time):
        return serial.readfrom(self.port, symbol.encode('utf-8'), time).decode('utf-8')

    def write(self, byted, size):
        buffer = (ctypes.c_ubyte * size)()
        for i in range(size):
            buffer[i]=byted[i]
        serial.send(self.port, buffer, size)

    def print(self, byted, size):
        serial.serialPrint(self.port, byted,size)
    
    def avail(self):
        return serial.serialDataAvail(self.port)