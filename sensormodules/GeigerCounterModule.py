from . import SensorModule
from . import SerialModule


class GeigerCounterModule(SensorModule):
    def __init__(self, logger, device, baudRate):
        self.sm = SerialModule(logger, device, baudRate)
        self.logger = logger

    def poll(self, dt):
        # The geiger counter's number of ticks is equal to the number of
        # characters on the serial output.
        
        data = self.sm.poll(dt)

        retval = []

        for c in data:
            retval.append(c)

        return retval