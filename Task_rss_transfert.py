import json
from time import sleep

import numpy as np
from PIL import Image
from numpy import array
from random import uniform, choice, randint

import cv2
from pytesseract import pytesseract

from Task import Task
from Task_utils import get_name, get_class, current_time
pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class RssTransfert(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        with open('../../../../../Downloads/user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.current_profile = MainTask.current_profile
        self.frame = MainTask.tile
        self.adb = MainTask.adb
        self.ppid = MainTask.ppid
        self.pid = MainTask.pid
        self.language = MainTask.language
        self.name = MainTask.name
        self.sel = MainTask.sel

    def task_name(self):
        return "RssTransfert"

    @get_name
    def get_capacity(self):
        """
                :return: True if there's a empty queue
                :return: False if queues are occupied
                """
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = array(pil_image)
        cropped_image3 = cv_image[558:590, 285:435]
        cv_image = cv2.cvtColor(cropped_image3, cv2.COLOR_BGR2HSV)
        native_text = pytesseract.image_to_string(cv_image,
                                                  config=r'--oem 1 --psm 13 -c tessedit_char_whitelist=0123456789/,')
        return int(native_text.split("/")[1].replace(",",""))

    # @get_name
    # def get_capacity(self):
    #     """
    #             :return: True if there's a empty queue
    #             :return: False if queues are occupied
    #             """
    #     pil_image = self.adb.get_curr_device_screen_img()
    #     cv_image = array(pil_image)
    #     cropped_image3 = cv_image[558:590, 285:435]
    #     cv_image = cv2.cvtColor(cropped_image3, cv2.COLOR_BGR2HSV)
    #     native_text = pytesseract.image_to_string(cv_image,
    #                                               config=r'--oem 1 --psm 13 -c tessedit_char_whitelist=0123456789/,')
    #     return int(native_text.split("/")[1].replace(",",""))


    @get_name
    def setup_ui(self,deadstop = 0):
        if deadstop ==3:
            raise ValueError()
        x,y = uniform(596,630), uniform(284,329)
        self.click(x,y)
        self.better_sleep((1,2))
        co = self.adb.find_img(target="assist_button")
        if co is None:
            self.close_windows()
            return self.setup_ui(deadstop = deadstop+1)
        self.click(co[0]+ uniform(0,40),co[1] + uniform(0,20))
        self.better_sleep((1,2))

    @get_name
    def check_captcha(self,chest=True):
        if not chest:
            super().check_captcha(chest)
            sleep(1)
        super().check_captcha(chest)

    @get_name
    def send_rss(self, type):
        types = {'food':uniform(210,230),
                 'wood':uniform(300,320),
                 'stone': uniform(390, 410),
                 'gold':uniform(470,490)}
        start = (uniform(589,597),types[type])
        end = (uniform(1045,1100), types[type]+uniform(-10,10))
        self.swipe(start[0],start[1],end[0],end[1])
        self.better_sleep((0.7,1.4))
        self.click(uniform(700,850),uniform(556,606))
        self.better_sleep((0.7, 1.4))

    @get_class
    def run(self,type,quantity):
        self.check_captcha()
        transfert_wanted = quantity
        self.setup_ui()
        self.better_sleep((0.7, 1.4))
        transportation_capacity = self.get_capacity()
        rss_sent = 0
        loop = int(transfert_wanted/transportation_capacity)
        if transportation_capacity * loop < transfert_wanted:
            loop+=1
        for i in range(loop):
            rss_sent += transportation_capacity
            self.send_rss(type)
            self.check_captcha(chest=True)
            if i!=loop-1:
                self.setup_ui()