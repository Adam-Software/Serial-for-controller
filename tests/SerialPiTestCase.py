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

from serial_for_controller.SerialPi import SerialPi


class SerialPiTestCase(unittest.TestCase):

    def testDoubleInitEquals(self):
        serial1 = SerialPi()
        serial2 = SerialPi()

        avial1 = serial1.Avail()
        avial2 = serial2.Avail()

        self.assertEqual(serial1, serial2)

        if os.name == 'nt':
            self.assertEqual(avial1, None)
            self.assertEqual(avial2, None)
            return

        self.assertEqual(avial1, 0)
        self.assertEqual(avial2, 0)


    def testWriteToSerialAfterClose(self):
        serial = SerialPi()
        avial1 = serial.Avail()

        # closing a port in one of the class instances will cause it to be closed in all instances of the class
        serial.Close()
        # but when accessing any method of the library, the port will be initialized again
        avial2 = serial.Avail()

        if os.name == 'nt':
            self.assertEqual(avial1, None)
            self.assertEqual(avial2, None)
            return

        self.assertEqual(avial1, 0)
        self.assertEqual(avial2, 0)

    def testDoubleInitWithCloseEquals(self):
        serial1 = SerialPi()
        serial2 = SerialPi()

        # closing a port in one of the class instances will cause it to be closed in all instances of the class
        serial1.Close()

        self.assertEqual(serial1._port, None)
        self.assertEqual(serial2._port, None)

    def testCalculateCrc(self):
        result = SerialPi.CalculateCrc([10, 2, 5, 0, 6, 0, 0, 0])
        self.assertEqual(result, 52)

    # running this test should be error-free
    def testRunOnWinSystem(self):
        serial1 = SerialPi()
        serial1.Close()

if __name__ == '__main__':
    unittest.main()
