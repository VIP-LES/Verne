import sensormodules
import logging
import signal
import csv
import yaml
import os
import sys
import time
from datetime import datetime, timedelta
from shutil import copyfile

fileDir = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = "/data/config.yml"

def getSmallestCSVFileNumberGreaterThan(currentFile, modules):
    # If files exist, we want to find an int at which file-i does not exist, and increment it
    # once more to make it clear that this is from a new recording.
    currentFile += 1

    while True:
        filesExist = [m for m in modules.keys() if os.path.isfile("/data/%s-%d.csv" % (m, currentFile))]

        if len(filesExist) > 0:
            currentFile += 1
        else:
            break

    return currentFile

def getCSVFilesFromModules(modules, missionTime, i):
    csvs = {}
    for m in modules.keys():
        f = open('/data/%s-%d.csv' % (m, i), 'wb')
        writer = csv.writer(f, delimiter=', ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        printableMissionTime = missionTime - datetime.fromtimestamp(0)
        writer.writerow([int(printableMissionTime.total_seconds() * 1000)])

        csvs[m] = (f, writer)

    return csvs

def closeCSVFiles(csvs):
    for c in csvs.values():
        c[0].close()

if __name__ == '__main__':
    # Initialize the logger
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("verne")

    if not os.path.isfile(CONFIG_PATH):
        copyfile(os.path.join(fileDir, "sampleConfig.yml"), CONFIG_PATH)

    # Start by reading the config
    cutFileAfterHours = None
    killScriptAfterHours = None
    modulesToInitialize = []

    with open(CONFIG_PATH, 'r') as ymlfile:
        def death(error):
            logger.error(error)
            ymlfile.close()
            sys.exit(1)

        cfg = yaml.load(ymlfile)

        cutFileAfterHours = float(cfg["cutFileInterval"])
        killScriptAfterHours = float(cfg["killScriptInterval"])

        modulesConfig = cfg["modules"]
        if modulesConfig is None:
            death("Config file does not have a list of modules.")

        if not hasattr(modulesConfig, '__iter__'):
            death("Config key 'modules' needs to be a list of modules and not a single entry.")

        for moduleConfig in modulesConfig:
            moduleName = moduleConfig["name"]
            if moduleName is None:
                death("Config file has module defined without a valid name.")

            moduleClassName = moduleConfig["type"]
            if moduleClassName is None:
                death("Config file has module defined without a valid type.")

            moduleClass = None
            try:
                moduleClass = getattr(sensormodules, moduleClassName)
            except:
                death("Config file references invalid module type %s" % moduleConfig["type"])

            if moduleClass is None:
                death("Config file references invalid module type %s" % moduleConfig["type"])

            moduleInitParams = []
            if moduleConfig["parameters"] is not None:
                for param in moduleConfig["parameters"]:
                    moduleInitParams.append(param)

            modulesToInitialize.append((moduleClass, moduleName, moduleInitParams))

        if cutFileAfterHours is None or cutFileAfterHours <= 0 or killScriptAfterHours is None or killScriptAfterHours <= 0:
            death("The config file did not contain valid values for required keys cutFileAfterHours and killScriptAfterHours. Delete the file if you want it reset.")

        if len(modulesToInitialize) == 0:
            death("File does not define any modules, making code useless. Delete the config file if you want to have it reset to the default module config.")

    # Load the modules
    modules = {}

    for moduleClass, moduleName, moduleInitParams in modulesToInitialize:
        moduleLogger = logger.getChild(moduleName)
        modules[moduleName] = moduleClass(*([moduleLogger] + moduleInitParams))
        logger.info("Loaded module %s of type %s" % (moduleName, moduleClass.__name__))

    missionTime = datetime.now()
    timeToKill = missionTime + timedelta(hours=killScriptAfterHours)
    timeToRenewFile = missionTime + timedelta(hours=cutFileAfterHours)

    currentFile = getSmallestCSVFileNumberGreaterThan(0, modules)
    currentFile += 1 # So that we get a gap from the last time this script was run

    logger.info("Creating initial CSV files. File number: %d" % currentFile)
    csvs = getCSVFilesFromModules(modules, missionTime, currentFile)

    logger.info("Liftoff: starting recording.")

    try:
        while True:
            currentTime = datetime.now()
            missionElapsedTime = int((currentTime - missionTime).total_seconds() * 1000)

            if currentTime > timeToKill:
                # It's time to end the recording! Goodbye!
                break

            if currentTime > timeToRenewFile:
                closeCSVFiles(csvs)

                currentFile = getSmallestCSVFileNumberGreaterThan(currentFile, modules)
                csvs = getCSVFilesFromModules(modules, missionTime, currentFile)

                timeToRenewFile = currentTime + timedelta(hours=cutFileAfterHours)
                logger.info("File cutoff time reached. New file number: %d" % currentFile)

            for m in modules.keys():
                data = modules[m].poll(missionElapsedTime)

                if data is not None and len(data) > 0:
                    writer = csvs[m][1]

                    for datum in data:
                        writer.writerow([missionElapsedTime] + list(datum))
    finally:
        closeCSVFiles(csvs)
        logger.info("The eagle has landed: stopping recording. Goodbye!")
        sys.exit(0)