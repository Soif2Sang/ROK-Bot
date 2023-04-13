import json
import traceback

from random import uniform
import cv2
from PIL import Image
from numpy import array
from pytesseract import pytesseract

from Task import Task, get_name
from Task_utils import get_class, get_data

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class DailyQuests(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.data = get_data()
        self.current_profile = MainTask.current_profile
        self.frame = MainTask.tile
        self.adb = MainTask.adb
        self.ppid = MainTask.ppid
        self.pid = MainTask.pid
        self.language = MainTask.language
        self.name = MainTask.name
        self.sel = MainTask.sel

    def task_name(self):
        return "DailyQuests"


    @get_name
    def available_quests(self):
        # pil_image = self.adb.get_curr_device_screen_img()
        # cv_image = array(pil_image)
        # cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        cv_image = self.adb.get_cv2_img()
        img = Image.fromarray(cv_image)
        # print(img.getpixel((75, 126)))
        # print(img.getpixel((65, 135)))
        return img.getpixel((75, 128))[0]>220 or img.getpixel((75, 128))[2]>220

    @get_name
    def daily_objectives(self):
        cv_image = self.adb.get_cv2_img()
        img = Image.fromarray(cv_image)
        return img.getpixel((62, 265))[0]>220 or img.getpixel((62, 265))[2]>220

    @get_name
    def enter_quests(self):
        self.click(uniform(23,69), uniform(151,190))
        self.better_sleep((1.725, 1.995))

    @get_name
    def claim_all(self):
        said = False
        while (co:=self.find_img("claim_quest")) is not None:
            if not said:
                self.print("Claiming the quests rewards")
                said = True
            self.click(co[0] + uniform(0,30), co[1]+ uniform(0,10))
            self.better_sleep((1.725, 1.995))

    @get_class
    def run(self):
        if self.available_quests():
            self.enter_quests()
            self.better_sleep((1.725, 1.995))
            self.claim_all()
            if self.daily_objectives():
                self.click(uniform(87,120), uniform(280,340))
                self.better_sleep((1.725, 1.995))
                self.claim_all()
                if self.daily_objectives():
                    self.print("Claiming daily objectives")
                    cos = [
                        [360,203],
                        [530,203],
                        [710,203],
                        [880,203],
                        [1050,203]
                    ]
                    for co in cos:
                        self.click(co[0]+uniform(-1,1), co[1]+uniform(-1,1))
                        self.better_sleep((3,5))
                        self.click(uniform(75,135), uniform(525,580))
                        self.better_sleep((1.725, 1.995))
            self.click(uniform(1082,1100), uniform(76,92))
            self.better_sleep((1.725, 1.995))