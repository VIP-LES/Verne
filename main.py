from sensormodules import IMUModule, GeigerCounterModule
import logging
import signal
import csv
import time
from datetime import datetime

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

    missionTime = datetime.now()

    for m in modules.keys():
        f = open('/data/%s.csv' % m, 'wb')
        writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        writer.writerow([missionTime])

        csvs[m] = (f, writer)

    while True:
        missionElapsedTime = int((datetime.now() - missionTime).total_seconds() * 1000)

        for m in modules.keys():
            data = modules[m].poll(missionElapsedTime)

            if len(data) > 0:
                writer = csvs[m][0]

                for datum in data:
                    writer.writerow([missionElapsedTime] + list(datum))

        if killer.kill_now:
            break

    for c in csvs.values():
        c[1].close()

    print("The eagle has landed.")
