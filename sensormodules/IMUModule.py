import sys

import RTIMU
import os.path
import time
import math

from . import SensorModule

class IMUModule(SensorModule):
    SETTINGS_FILE = "RTIMULib"
    MILLISECOND_POLLING_INTERVAL = 500

    def __init__(self, logger):
        sys.path.append('.')

        logger.info("Using settings file " + IMUModule.SETTINGS_FILE + ".ini")
        if not os.path.exists(IMUModule.SETTINGS_FILE + ".ini"):
            logger.warning("Settings file does not exist, will be created")

        s = RTIMU.Settings(IMUModule.SETTINGS_FILE)
        imu = RTIMU.RTIMU(s)

        logger.info("IMU Name: " + imu.IMUName())

        if not imu.IMUInit():
            raise ValueError("IMU Init Failed")

        imu.setSlerpPower(0.02)
        imu.setGyroEnable(True)
        imu.setAccelEnable(True)
        imu.setCompassEnable(True)

        self.imu = imu
        self.pollInterval = imu.IMUGetPollInterval()
        self.logger = logger

    def poll(self, dt):
        if self.imu.IMURead():
            data = self.imu.getIMUData()
            fusionPose = data["fusionPose"]
            #self.data = [(math.degrees(fusionPose[0]), math.degrees(fusionPose[1]), math.degrees(fusionPose[2]))]
            self.data = tuple([math.degrees(v) for v in fusionPose])

        if (self.data is not None) and (self.lastPoll is None or ((dt - self.lastPoll).total_seconds() * 1000 >= self.pollInterval)):
            self.lastPoll = dt
            return [self.data]