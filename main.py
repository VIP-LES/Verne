from sensormodules import IMUModule, GeigerCounterModule
import logging
import signal
import csv
import yaml
import os
import time
from datetime import datetime, timedelta
from shutil import copyfile

fileDir = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = "/data/config.yml"

logging.basicConfig(level=logging.INFO)

class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True

def getCSVFilesFromModules(modules, missionTime, i):
    csvs = {}
    for m in modules.keys():
        f = open('/data/%s-%d.csv' % (m, i), 'wb')
        writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        printableMissionTime = missionTime - datetime.fromtimestamp(0)
        writer.writerow([int(printableMissionTime.total_seconds() * 1000)])

        csvs[m] = (f, writer)

    return csvs

def closeCSVFiles(csvs):
    for c in csvs.values():
        c[0].close()

if __name__ == '__main__':
    killer = GracefulKiller()

    if not os.path.isfile(CONFIG_PATH):
        copyfile(os.path.join(fileDir, "sampleConfig.yml"), CONFIG_PATH)

    # Start by reading the config
    cutFileAfterHours = None
    killScriptAfterHours = None
    with open(CONFIG_PATH, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

        cutFileAfterHours = float(cfg["cutFileInterval"])
        killScriptAfterHours = float(cfg["killScriptInterval"])

    if cutFileAfterHours is None or killScriptAfterHours is None:
        raise ValueError("Could not read config file. Delete file if you want it reset.")

    # Initialize the logger
    logger = logging.getLogger("verne")

    # Load the modules
    modules = {}
    modules['imu'] = IMUModule(logger.getChild("imu"))
    modules['geiger'] = GeigerCounterModule(logger.getChild("geiger"), "/dev/ttyAMA0", 9600)

    missionTime = datetime.now()
    timeToKill = missionTime + timedelta(hours=killScriptAfterHours)
    timeToRenewFile = missionTime + timedelta(hours=cutFileAfterHours)

    currentFile = 0

    # If files exist, we want to find an int at which file-i does not exist, and increment it
    # once more to make it clear that this is from a new recording.
    while True:
        filesExist = [os.path.isfile("/data/%s-%d.csv" % (m, currentFile)) for m in modules.keys()].count(True)

        if filesExist > 0:
            currentFile += 1
        else:
            break

    currentFile += 1

    csvs = getCSVFilesFromModules(modules, missionTime, currentFile)
    currentFile += 1
    
    logger.info("Starting mission loop.")

    while True:
        currentTime = datetime.now()
        missionElapsedTime = int((currentTime - missionTime).total_seconds() * 1000)

        if currentTime > timeToKill:
            # It's time to end the recording! Goodbye!
            break

        if currentTime > timeToRenewFile:
            closeCSVFiles(csvs)

            csvs = getCSVFilesFromModules(modules, missionTime, currentFile)
            currentFile += 1

            timeToRenewFile = currentTime + timedelta(hours=cutFileAfterHours)

        for m in modules.keys():
            data = modules[m].poll(missionElapsedTime)

            if data is not None and len(data) > 0:
                writer = csvs[m][1]

                for datum in data:
                    writer.writerow([missionElapsedTime] + list(datum))

        if killer.kill_now:
            break

    closeCSVFiles(csvs)

    logger.info("The eagle has landed: stopping recording. Goodbye!")
