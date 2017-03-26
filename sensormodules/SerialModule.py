from . import SensorModule
import serial

class SerialModule(SensorModule):
    def __init__(self, logger, device, baudRate):
        self.sd = serial.Serial(device, baudRate, timeout=None)

        self.logger = logger

    def poll(self):
        # It's important to realize that this method may produce incomplete data if called
        # in the middle of a line and it's up to the main loop to handle that.
        if self.sd.in_waiting > 0:
            data = self.sd.read(self.sd.in_waiting)
            return [data]