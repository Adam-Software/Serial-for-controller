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

        avial1 = serial1.avail()
        avial2 = serial2.avail()

        self.assertEqual(serial1, serial2)
        self.assertEqual(avial1, 0)
        self.assertEqual(avial2, 0)


    def testWriteToSerialAfterClose(self):
        serial = SerialU()
        avial1 = serial.avail()

        # closing a port in one of the class instances will cause it to be closed in all instances of the class
        serial.close()
        # but when accessing any method of the library, the port will be initialized again
        avial2 = serial.avail()


        self.assertEqual(avial1, 0)
        self.assertEqual(avial2, 0)

    def testDoubleInitWithCloseEquals(self):
        serial1 = SerialU()
        serial2 = SerialU()

        # closing a port in one of the class instances will cause it to be closed in all instances of the class
        serial1.close()

        self.assertEqual(serial1._port, None)
        self.assertEqual(serial2._port, None)

    def testCalculateCrc(self):
        result = SerialU.CalculateCrc([0, 0, 0, 0, 0, 0, 0, 0])
        print(result)


if __name__ == '__main__':
    unittest.main()
