import sys
import os
import unittest

# import module from dirrectory
# if need test package comment 3 lines below

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from Serial.serialPi import SerialU


class SerialPiTestCase(unittest.TestCase):

    def testDoubleInitEquals(self):
        serial1 = SerialU()
        serial2 = SerialU()

        self.assertEqual(serial1, serial2)

    def testWriteToSerialAfterClose(self):
        serial = SerialU()
        avial = serial.avail()

        self.assertEqual(avial, True)


if __name__ == '__main__':
    unittest.main()
