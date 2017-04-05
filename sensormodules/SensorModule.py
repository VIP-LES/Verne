import abc

class SensorModule:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def poll(self, dt):
        """
        This is our module's polling method which will be called from the main event loop.
        This method should not block under any circumstances.

        It should return a list of tuples containing data points. All of these data points will get the
        current timestamp, so the timestamp should not be included.
        """
        return