from random import uniform

import cv2
from pytesseract import pytesseract

from taskscod.COD_Task import Task
from utils.functions import get_class

pytesseract.tesseract_cmd = r".\\tesseract\\tesseract.exe"


class ClaimCampaign(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.data = MainTask.data
        self.current_profile = MainTask.current_profile
        self.frame = MainTask.tile
        self.adb = MainTask.adb
        self.ppid = MainTask.ppid
        self.pid = MainTask.pid
        self.language = MainTask.language
        self.name = MainTask.name
        self.sel = MainTask.sel

    def task_name(self):
        return "ClaimCampaign"

    @get_class
    def run(self):
        # Open du menu
        if self.find_img(target="cod_toolbar", confidence=0.8) is None:
            x, y = uniform(1200, 1250), uniform(650, 690)
            self.click(x, y)
            self.better_sleep((1.725, 1.995))
        self.click(860 + uniform(-5, 5), 670 + uniform(-5, 5))
        self.better_sleep((2.725, 3.995))
        self.click(640 + uniform(-5, 5), 640 + uniform(-5, 5))
        self.better_sleep((1.725, 1.995))
        if co := self.find_img(target="cod_claim", confidence=0.8):
            self.click(co[0] + uniform(0, 10), co[1] + uniform(0, 10))
            self.better_sleep((1.725, 1.995))
        self.close_windows()
