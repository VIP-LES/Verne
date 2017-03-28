from sensormodules import IMUModule, GeigerCounterModule
import logging
import signal
import csv
import time


# TODO: Improve the time function!
millis = lambda: int(round(time.time() * 1000))

class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


if __name__ == '__main__':
    killer = GracefulKiller()
    modules = {}
    csvs = {}

    logger = logging.getLogger("verne")

    modules['imu'] = IMUModule(logger.getChild("imu"))
    modules['geiger'] = GeigerCounterModule(logger.getChild("geiger"), "/dev/uart", 9600)

    for m in modules.keys():
        f = open('%s.csv' % m, 'wb')
        writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        csvs[m] = (f, writer)

    while True:
        for m in modules.keys():
            data = modules[m].poll()

            if len(data) > 0:
                currentTime = millis()
                writer = csvs[m][0]

                for datum in data:
                    writer.writerow([currentTime] + list(datum))

        if killer.kill_now:
            break

    for c in csvs.values():
        c[1].close()

    print("Goodbye!")
