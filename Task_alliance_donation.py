import json

from numpy import array
from random import uniform,randint

import cv2
from pytesseract import pytesseract

from Task import Task
from Task_utils import get_class, get_name

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class AllianceDonation(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.frame)
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.current_profile = MainTask.current_profile
        self.frame = MainTask.frame
        self.adb = MainTask.frame.adb
        self.ppid = MainTask.ppid
        self.pid = MainTask.pid
        self.language = MainTask.language
        self.name = MainTask.name
        self.resource_type = MainTask.resource_type
        self.sel = MainTask.sel

    def task_name(self):
        return "AllianceDonation"

    @get_name
    def collect_alliance_resources(self) -> None:
        screen = self.adb.get_curr_device_screen_img()
        source = array(screen)
        source = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
        co = self.adb.find_img(source=source, target="alliance_flag1", confidence=0.8)
        if co is None:
            co = self.adb.find_img(source=source, target="alliance_flag2", confidence=0.8)
        if co is None:
            return
        self.click(co[0] + uniform(0, 20), co[1] + uniform(0, 10))
        self.better_sleep((1.0, 1.395))
        x, y = uniform(955, 1067), uniform(122, 150)
        self.click(x, y)
        self.better_sleep((0.78, 1.095))
        x, y = uniform(1100, 1130), uniform(30, 58)
        self.click(x, y)
        self.better_sleep((1.0, 1.395))

    @get_class
    def run(self):
        # Open du menu
        if self.adb.find_img(target='menu_opened', confidence=0.8) is None:
            x, y = uniform(1200, 1250), uniform(650, 690)
            self.click(x, y)
            self.better_sleep((1.725, 1.995))
        # Open alliance menu
        x, y = uniform(1010, 1050), uniform(650, 690)
        self.click(x, y)
        self.better_sleep((1.725, 2.295))

        alliance_tech_logo = self.adb.find_img(target="alliance_tech")
        if alliance_tech_logo is not None:
            self.click(alliance_tech_logo[0] + uniform(0, 30), alliance_tech_logo[1] + uniform(0, 15))
            self.better_sleep((2, 3))
            donation_logo = self.adb.find_img(target="tech")

            if donation_logo is not None:
                self.click(donation_logo[0] + uniform(0, 10), donation_logo[1] + uniform(0, 10))
                self.better_sleep((1, 2))
                # Holding click on the donation button
                while self.adb.find_img(target="donate_button"):
                    x, y, arg = uniform(910, 1040), uniform(550, 580), randint(2500, 3475)
                    self.swipe_arg(x, y, x, y, arg)
                    self.better_sleep((0.7, 1.3))
                # Check if the resources pop-up comes
                if self.adb.find_img(target="get_more_rss") is not None:
                    self.click(uniform(1000, 1020), uniform(129, 148))
                    self.better_sleep((1, 1.425))
                self.click(uniform(1080, 1100), uniform(70, 90))
                self.better_sleep((1, 1.425))

            x, y = uniform(1100, 1130), uniform(60, 80)
            self.click(x, y)
            self.better_sleep((1.8, 2.125))
            self.collect_alliance_resources()

        x, y = uniform(1100, 1130), uniform(30, 58)
        self.click(x, y)
        self.better_sleep((1.3, 1.6))
