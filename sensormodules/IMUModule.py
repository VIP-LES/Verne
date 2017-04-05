import sys

import RTIMU
import os.path
import time
import math

from . import SensorModule

class IMUModule(SensorModule):
    def __init__(self, logger, settings_file, millisecond_polling_interval):
        sys.path.append('.')

        logger.info("Using settings file " + settings_file + ".ini")
        if not os.path.exists(settings_file + ".ini"):
            logger.warning("Settings file does not exist, will be created")
        else:
            logger.info("Using existing IMU settings file")

        self.s = RTIMU.Settings(settings_file)
        self.imu = RTIMU.RTIMU(self.s)

        logger.info("IMU Name: " + self.imu.IMUName())

        if not self.imu.IMUInit():
            raise ValueError("IMU Init Failed")
        else:
            logger.info("IMU initialized")

        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)

        self.pollInterval = millisecond_polling_interval
        self.logger = logger
        self.data = None
        self.lastPoll = None

    def poll(self, dt):
        if self.imu.IMURead():
            data = self.imu.getIMUData()
            fusionPose = data["fusionPose"]
            almostReady = ([data["accel"][0] * 9.81, data["accel"][1] * 9.81, data["accel"][2] * 9.81]+[math.degrees(v) for v in fusionPose])
            self.data = tuple(["%.2f" % d for d in almostReady])

        if (self.data is not None) and (self.lastPoll is None or ((dt - self.lastPoll) >= self.pollInterval)):
            self.lastPoll = dt
            return [self.data]
