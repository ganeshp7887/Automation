import logging
import time


class Logger:

    def __init__(self):
        pass

    def AddLog(self, data):
        self.Logger = logging.basicConfig(filename='./Log/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.Logger.info(data)