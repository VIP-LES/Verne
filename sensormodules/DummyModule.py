from . import SensorModule

class DummyModule(SensorModule):
    def __init__(self, logger, reportEveryNSeconds, returnObj):
        self.pollInterval = reportEveryNSeconds * 1000
        self.logger = logger
        self.lastPoll = None
        self.data = [returnObj]

    def poll(self, dt):
        if (self.data is not None) and (self.lastPoll is None or ((dt - self.lastPoll) >= self.pollInterval)):
            self.lastPoll = dt
            return [tuple(self.data)]
