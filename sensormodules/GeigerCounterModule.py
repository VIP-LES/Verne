from . import SensorModule
from . import SerialModule


class GeigerCounterModule(SensorModule):
    def __init__(self, logger, device, baudRate):
        self.sm = SerialModule(logger, device, baudRate)
        self.logger = logger

    def poll(self):
        # The geiger counter's number of ticks is equal to the number of
        # characters on the serial output.
        
        data = self.sm.poll()

        retval = []

        for _ in xrange(data):
            retval.append(True)

        return retval