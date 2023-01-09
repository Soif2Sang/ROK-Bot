import cv2
import numpy as np
from bot_adb import *
from tasks_lib import *
from random import randint, uniform, shuffle
from time import sleep, time
import pytesseract
import json
import pygetwindow
import verification
import win32gui, win32ui, win32con, win32api
from datetime import datetime

with open('rkp_list.json') as config_file: data = json.load(config_file)
import pandas as pd


class Up:
    def __init__(self, adb):
        self.adb = adb
        self.sel = None

    def set_sel(self, sel):
        self.sel = sel[0]

    def click_default_hut(self):
        x, y = uniform(700, 769), uniform(214, 265)
        self.adb.click(x, y)

        sleep(1)
        x, y = uniform(790, 864), uniform(370, 417)
        self.adb.click(x, y)
        sleep(1)

    def find_image(self, image, confidence=0.8):
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = np.array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img_to_find = cv2.imread(f'resources\\{image}.png')
        result = cv2.matchTemplate(cv_image, img_to_find, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > confidence:
            return max_loc[0] + uniform(0, 40), max_loc[1] + uniform(0, 20)
        else:
            return

    def find_build(self):
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = np.array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img_to_find = cv2.imread('resources\\build.png')
        result = cv2.matchTemplate(cv_image, img_to_find, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.9:
            return max_loc[0] + uniform(0, 40), max_loc[1] + uniform(0, 20)
        else:
            return

    def find_build_upgrade(self):
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = np.array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img_to_find = cv2.imread('resources\\upgrade.png')
        result = cv2.matchTemplate(cv_image, img_to_find, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.7:
            return max_loc[0] + uniform(0, 40), max_loc[1] + uniform(0, 20)
        else:
            return

    def click_help(self):
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = np.array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img_to_find = cv2.imread('resources\\help.png')
        result = cv2.matchTemplate(cv_image, img_to_find, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.7:
            print(max_loc)
            return self.adb.click(max_loc[0] + uniform(0, 5), max_loc[1] + uniform(0, 5))
        else:
            return

    def enter_city(self):
        x = uniform(24, 91)
        y = uniform(625, 680)
        self.adb.click(x, y)
        sleep(1)
        x = uniform(24, 91)
        y = uniform(625, 680)
        self.adb.click(x, y)

    def is_in_builder(self):
        co = self.find_image('builder',0.8)
        return co!=None

    def new_build(self):
        if bot.is_in_builder():
            pil_image = bot.adb.get_curr_device_screen_img()
            cv_image = array(pil_image)
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv_image)
            print(img.getpixel((8, 355)))
            if img.getpixel((8, 355))[2] > 225 and img.getpixel((8, 355))[1] < 10:
                self.adb.click(uniform(170,360),uniform(400,600))
                sleep(uniform(1,1.2))
                co = self.find_image('validate_building')
                if co is not None:
                    self.adb.click(uniform(-5,5)+co[0],uniform(-10,5)+co[1])
                    sleep(uniform(1, 1.2))
                    return
            if img.getpixel((8, 355))[2] > 225 and img.getpixel((8, 355))[1] < 10:
                print("x")

    def from_city_upgrade(self):
        while True:
            #Enter in the hut
            self.click_default_hut()
            #Trouve l'icone build
            co = self.find_build()

            while co is None:
                print("No builder available")
                sleep(uniform(10, 11))
                co = self.find_build()
            #Click sur l'icone build
            self.adb.click(uniform(0, 10) + co[0], uniform(0, 10) + co[1])
            sleep(uniform(1.2, 1.7))

            #Si il est dans le builder
            self.new_build()
            #Trouve l'icone upgrade
            co = self.find_build_upgrade()
            if co is not None:
                self.adb.click(uniform(0,10) + co[0],uniform(0,10)+ co[1])
                sleep(uniform(1.2, 1.7))
            else:
                print("Upgrade button not found")
                return
            x, y = uniform(920, 1050), uniform(530, 560)
            self.adb.click(x, y)

            sleep(uniform(1.2, 1.7))
            self.enter_city()
            sleep(uniform(2.3,3))
            self.click_help()
            sleep(uniform(1.2, 1.7))

a=Adb(1)
bot=Up(a)
bot.set_sel('1')
bot.adb.get_device()

bot.from_city_upgrade()

