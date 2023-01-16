import json
import traceback

from random import uniform
import cv2
from PIL import Image
from numpy import array
from pytesseract import pytesseract

from Task import Task, get_name
from Task_utils import get_class

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class DailyQuests(Task):
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
        return "DailyQuests"


    @get_name
    def available_quests(self):
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        cropped_image = cv_image[230:480, 441:814]
        img = Image.fromarray(cropped_image)
        return img.getpixel((68, 131)) == (227, 0, 0) or img.getpixel((68, 131)) == (0, 0, 227)

    @get_name
    def enter_quests(self):
        self.click(uniform(23,69), uniform(151,190))
        self.better_sleep((1.725, 1.995))