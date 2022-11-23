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
if os.name != 'nt':
    if(is64bit):
        serial = ctypes.CDLL(os.path.join(path, 'serial_aaarch64.so'))
    else:
        serial = ctypes.CDLL(os.path.join(path, 'serial_armv71.so'))
 

if os.name != 'nt':
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

class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class SerialU(metaclass=MetaSingleton):
    _port = None
    _devicename = None
    _baudrate = None

    def __init__(self,
                 devicename: str = '/dev/ttyAMA0',
                 baudrate: int = 115200):
        self._devicename = devicename
        self._baudrate = baudrate
        self._initPort()

    def _initPort(self):
        if os.name == 'nt':
            return

        if self._port is None:
            self._port = serial.serialOpen(self._devicename.encode('utf-8'), self._baudrate)

    def close(self):
        if os.name == 'nt':
            return

        if self._port is not None:
            serial.serialClose(self._port)
            self._port = None

    def read(self, symbol, time, buffer):
        if os.name == 'nt':
            return

        if self._port is not None:
            return serial.readdata(self._port, symbol.encode('utf-8'), time, buffer).decode('utf-8')

        self._initPort()
        return serial.readdata(self._port, symbol.encode('utf-8'), time, buffer).decode('utf-8')

    def readByte(self, symbol, time, buffer):
        if os.name == 'nt':
            return

        if self._port is not None:
            return serial.readdata(self._port, symbol.encode('utf-8'), time, buffer)

        self._initPort()
        return serial.readdata(self._port, symbol.encode('utf-8'), time, buffer)

    def readf(self, symbol, time):
        if os.name == 'nt':
            return

        if self._port is not None:
            return serial.readfrom(self._port, symbol.encode('utf-8'), time).decode('utf-8')

        self._initPort()
        return serial.readfrom(self._port, symbol.encode('utf-8'), time).decode('utf-8')

    def write(self, byted, size):
        if os.name == 'nt':
            return

        if self._port is not None:
            buffer = (ctypes.c_ubyte * size)()
            for i in range(size):
                buffer[i]=byted[i]
            serial.send(self._port, buffer, size)
            return

        self._initPort()
        self.write(byted, size)
        return


    def print(self, byted, size):
        if os.name == 'nt':
            return

        if self._port is not None:
            serial.serialPrint(self._port, byted, size)
            return

        self._initPort()
        self.print(byted, size)
        return

    def avail(self):
        if os.name == 'nt':
            return

        if self._port is not None:
            return serial.serialDataAvail(self._port)

        self._initPort()
        return serial.serialDataAvail(self._port)

    @staticmethod
    def CalculateCrc(arr):
        st_byt = 0
        crc = 0

        while st_byt < len(arr):
            dat = arr[st_byt]
            for i in range(8):
                fb = crc ^ dat
                fb &= 1
                crc >>= 1
                dat >>= 1
                if fb == 1:
                    crc ^= 0x8c
            st_byt += 1

        return crc