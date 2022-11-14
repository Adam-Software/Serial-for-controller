import unittest
from Serial.serialPi import SerialU


class SerialPiTestCase(unittest.TestCase):

    def testDoubleInitEquals(self):
        serial1 = SerialU()
        serial2 = SerialU()

        self.assertEqual(serial1, serial2)  # add assertion here

if __name__ == '__main__':
    unittest.main()
