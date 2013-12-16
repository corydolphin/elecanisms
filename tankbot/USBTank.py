import usb.core
import time

HELLO = 0
SET_MOTORS = 1

class USBTank:
    def __init__(self):
        self.dev = usb.core.find(idVendor = 0x6666, idProduct = 0x0003)
        if self.dev is None:
            raise ValueError('no USB device found matching idVendor = 0x6666 and idProduct = 0x0003')
        self.dev.set_configuration()
        self.rMotor = 0
        self.lMotor = 0
        self.linVel = 0
        self.angVel = 0

    def close(self):
        self.dev = None

    def hello(self):
        try:
            self.dev.ctrl_transfer(0x40, HELLO)
        except usb.core.USBError:
            print "Could not send HELLO vendor request."

    def set_motors(self, lMotor, rMotor):
        self.rMotor = rMotor
        self.lMotor = lMotor
        try:
            self.dev.ctrl_transfer(0x40, SET_MOTORS, int(self.lMotor), int(self.rMotor))
        except usb.core.USBError:
            print "Could not send SET_MOTORS vendor request."

    def set_vel(self, linVel, angVel):
        self.linVel = linVel
        self.angVel = angVel
        self.set_motors(linVel + angVel/2, linVel - angVel/2)

if __name__ == '__main__':
    dev = USBTank()
    time.sleep(1)

    for i in range(-32500,32501,5000):
        print i
        dev.set_motors(i,i)
        time.sleep(1)
        # time.sleep(0.001)
