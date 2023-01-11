import json
import logging
import multiprocessing
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from functools import wraps
from os.path import exists
from random import randint, uniform, shuffle, random, choice
from time import sleep, time, perf_counter

import cv2
import numpy as np
import pytesseract
import win32api
import win32con
import win32gui
import win32process
from PIL import Image
from numpy import array, ndarray
from psutil import pid_exists

import verification
from twocaptcha import TwoCaptcha

if not os.path.exists("user_settings.json"):
    with open('user_settings.json', 'w') as f:
        json.dump({}, f, indent=2)
        print("User settings created")

with open('user_settings.json') as config_file:
    data = json.load(config_file)

with open('path.json') as config_file: path = json.load(config_file)

center = (640, 360)
food_icon = ((400, 472), (603, 663))
wood_icon = ((598, 670), (603, 663))
stone_icon = ((786, 870), (603, 663))
gold_icon = ((977, 1050), (603, 663))

pytesseract.pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


def current_time():
    return datetime.now().strftime("%H:%M:%S")


def get_window_pid(title):
    hwnd = win32gui.FindWindow(None, title)
    thread_id, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid


def get_time(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = perf_counter()
        func_output = func(self, *args, **kwargs)
        end_time = perf_counter()

        if func.__name__ == "check_resolve":
            print(f'[ {current_time()} ] [ {self.name} ] Verification made in {(end_time - start_time):0.1f}')
            self.set_text(f'[{current_time()}] Verification made in {(end_time - start_time):0.1f}')
            logging.info(f"[{self.name}] Verification made in {(end_time - start_time):0.1f}")
        return func_output

    return wrapper


def clean_args(*args):
    list_args = []
    for args2 in args:
        if isinstance(args2, tuple) or isinstance(args2, list):
            for arg in args2:
                if isinstance(arg, Image.Image) or isinstance(arg, ndarray):
                    list_args.append("Image")
                else:
                    list_args.append(arg)
        else:
            list_args.append(args2)
    return tuple(list_args)


def get_name(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
        self.script_pause()
        logging.info(f"[ {self.name} ] FUNCTION : {func.__name__} ARGS : {clean_args(args)}")
        print(f"[ {current_time()} ] [ {self.name} ] FUNCTION : {func.__name__} ARGS : {clean_args(args)}")
        func_output = func(self, *args, **kwargs)
        return func_output

    return wrapper


def filter_coordinate(couple: tuple[int, int]):
    if couple[0] < 206:
        return False
    if couple[0] < 274 and couple[1] < 108:
        return False
    if couple[0] > 516 and couple[1] < 168:
        return False
    if couple[0] < 735 and couple[1] > 587:
        return False
    if couple[0] > 1146 and couple[1] < 218:
        return False
    return True


def change_resource_type(place: str) -> str:
    if place == "First":
        return "Second"
    elif place == "Second":
        return "Third"
    elif place == "Third":
        return "Fourth"
    elif place == "Fourth":
        return "Done"


class Tasks:
    def __init__(self, frame):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.current_profile = '1'
        self.frame = frame
        self.adb = frame.adb
        self.ppid = os.getppid()
        self.pid = get_window_pid(self.adb.name)
        self.language = None
        self.name = None
        self.resource_type = None
        self.sel = None

    def set_text(self, text):
        self.frame.write(text)

    def set_status(self, text):
        self.frame.update_label2(self.sel, text)

    def update_data(self):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        return self.data

    def set_sel(self, sel) -> None:
        self.data = self.update_data()
        self.sel = sel[0]
        self.name = self.data.get(self.sel).get('name', "Name not found")
        # print(self.name)
        self.resource_type = self.data[str(self.sel)]['schedules'][self.current_profile]["First"]
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")

    @get_name
    def print(self, text: str) -> None:
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
        # print(f'[ {current_time()} ] [ {self.name} ] {text}')
        # logging.info(f"[{self.name}] {text}")
        self.set_text(f"[{current_time()}] {text}")

    @get_name
    def click(self, x, y):
        self.adb.click(x, y)

    @get_name
    def swipe(self, x, y, x2, y2):
        self.adb.swipe(x, y, x2, y2)

    @get_name
    def swipe_arg(self, x, y, x2, y2, arg):
        # return self.click(x,y)
        self.adb.swipe_arg(x, y, x2, y2, arg)

    def swipe_right(self) -> None:
        """
        Send adb signal to swipe to the right
        """

        x1, y1, y2 = uniform(940, 960), uniform(335, 385), uniform(335, 385)
        x2 = x1 - uniform(710, 710)
        self.swipe(x1, y1, x2, y2)

    def swipe_left(self) -> None:
        """
        Send adb signal to swipe to the left
        """
        x1, y1, y2 = uniform(940, 960), uniform(335, 385), uniform(335, 385)
        x2 = x1 - uniform(710, 710)
        self.swipe(x2, y2, x1, y1)

    def swipe_up(self) -> None:
        """
        Send adb signal to swipe upward
        """
        x1, y1 = uniform(600, 680), uniform(540, 560)
        x2 = x1 + uniform(0, 30)
        y2 = y1 - uniform(390, 397)
        self.swipe(x2, y2, x1, y1)

    def swipe_down(self) -> None:
        """
        Send adb signal to swipe downward
        """
        x1, y1 = uniform(600, 680), uniform(540, 560)
        x2 = x1 + uniform(0, 30)
        y2 = y1 - uniform(390, 397)
        self.swipe(x1, y1, x2, y2)

    def swipe_right_low(self) -> None:
        """
        Send adb signal to swipe to the right
        """
        x1, y1, x2, y2 = uniform(700, 720), uniform(330, 380), uniform(260, 280), uniform(330, 380)
        self.swipe(x1, y1, x2, y2)

    def swipe_left_low(self) -> None:
        """
        Send adb signal to swipe to the left
        """
        x1, y1, x2, y2 = uniform(700, 720), uniform(330, 380), uniform(260, 280), uniform(330, 380)
        self.swipe(x2, y2, x1, y1)

    def swipe_up_low(self) -> None:
        """
        Send adb signal to swipe upward
        """
        x1, y1, x2, y2 = uniform(540, 560), uniform(540, 560), uniform(570, 600), uniform(200, 220)
        self.swipe(x2, y2, x1, y1)

    def swipe_down_low(self) -> None:
        """
        Send adb signal to swipe downward
        """
        x1, y1, x2, y2 = uniform(540, 560), uniform(540, 560), uniform(570, 600), uniform(200, 220)
        self.swipe(x1, y1, x2, y2)

    @get_name
    def little_zoom_from_x_y(self, x_click: int, y_click: int) -> None:
        if x_click > 950:
            self.swipe_left_low()
            return
        if x_click < 380:
            self.swipe_right_low()
            return
        if y_click < 150:
            self.swipe_down_low()
            return
        if y_click > 480:
            self.swipe_up_low()
            return

    @get_name
    def adjusted_leave_city(self, x_click: int, y_click: int) -> None:
        self.check_if_kill()
        self.zoom_out_city()
        self.check_if_kill()
        self.better_sleep((1, 2))
        self.little_zoom_from_x_y(x_click, y_click)
        return self.better_sleep((0.7, 1.4))

    @get_name
    def validate_co(self, co: tuple[int, int]) -> None | tuple[int, int]:
        # sourcery skip: merge-nested-ifs
        if co is not None:
            if (co[0] < 550 and co[1] < 100) or \
                    ((1180 < co[0] < 1235) and (520 < co[1] < 620)) or \
                    ((1159 < co[0] < 1235) and (150 < co[1] < 195)) or \
                    (co[0] < 556 and co[1] > 630) or \
                    (co[0] < 110 and co[1] > 495) or \
                    (co[0] > 1040 and co[1] < 160) or \
                    (co[1] > 515 and co[0] > 1175) or \
                    (co[0] < 120 and co[1] < 120) or \
                    (co[0] < 685 and co[1] > 615) or \
                    co[0] < 100 or \
                    co[1] < 35:
                co = None
        return co

    @get_name
    def better_sleep(self, limits: tuple[float, float]):
        self.data = self.update_data()
        a = limits[0]
        b = limits[1]
        if self.data[str(self.sel)]['schedules'][self.current_profile]["slow_mode"]:
            # self.set_text(tuple,tuple[0])
            a = a * self.data[str(self.sel)]['schedules'][self.current_profile]["sleep_multiplicator"]
            b = b * self.data[str(self.sel)]['schedules'][self.current_profile]["sleep_multiplicator"]
        sleep(uniform(a, b))

    @get_name
    def in_city(self) -> bool:
        """
        Check if the current view is set in the city
        :return: True if in city, False if not
        """
        return self.adb.find_img(target='gem_search_button') is None

    @get_name
    def leave_city_simple(self) -> bool:
        """
        -Enter and leave city if not in city
        -Leave city if in city
        """
        print(f'[ {current_time()} ] [ {self.name} ] leave_city_simple call')
        if self.in_city():
            print(f'[ {current_time()} ] [ {self.name} ] quiting city')
            self.click(uniform(24, 91), uniform(625, 680))
            self.better_sleep((1.5, 2))
        return True

    @get_name
    def leave_city(self) -> bool:
        """
        -Enter and leave city if not in city
        -Leave city if in city
        """
        if self.in_city():
            self.click(uniform(24, 91), uniform(625, 680))
            self.better_sleep((1.5, 2))
        else:
            self.click(uniform(24, 91), uniform(625, 680))
            self.better_sleep((1.5, 2))
            self.click(uniform(24, 91), uniform(625, 680))
        return True

    @get_name
    def click_loop(self) -> None:
        print(f'[ {current_time()} ] [ {self.name} ] click loop call')
        if not self.adb.find_img(target="gem_search_button"):
            print(f'[ {current_time()} ] [ {self.name} ] Loop icon not found, leaving the city')
            self.leave_city()
            self.better_sleep((2, 3))
        x = uniform(33, 76)
        y = uniform(517, 560)
        # print(x,y)
        self.click(x, y)
        self.better_sleep((0.3, 0.5))

    @get_name
    def click_food(self):
        x = uniform(400, 472)
        y = uniform(603, 663)
        self.click(x, y)
        self.resource_type = "food"
        self.better_sleep((0.3, 0.5))

    @get_name
    def click_wood(self) -> None:
        x = uniform(598, 670)
        y = uniform(603, 663)
        self.click(x, y)
        self.resource_type = "wood"
        self.better_sleep((0.3, 0.5))

    @get_name
    def click_stone(self) -> None:
        x = uniform(786, 870)
        y = uniform(603, 663)
        self.click(x, y)
        self.resource_type = "stone"
        self.better_sleep((0.3, 0.5))

    @get_name
    def click_gold(self) -> None:
        x = uniform(977, 1050)
        y = uniform(603, 663)
        self.click(x, y)
        self.resource_type = "gold"
        self.better_sleep((0.3, 0.5))

    @get_name
    def click_search_node(self, place: str) -> None:
        self.print(f"Looking for : {self.data[str(self.sel)]['schedules'][self.current_profile].get(place)} {place}")
        if self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "food":
            x = uniform(400, 472)
            y = uniform(463, 512)
            self.click(x, y)
        elif self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "wood":
            x = uniform(598, 670)
            y = uniform(463, 512)
            self.click(x, y)
        elif self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "stone":
            x = uniform(786, 870)
            y = uniform(463, 512)
            self.click(x, y)
        elif self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "gold":
            x = uniform(977, 1050)
            y = uniform(463, 512)
            self.click(x, y)

    @get_name
    def node_found(self) -> bool:
        if self.adb.find_img(target='search_button') is not None:
            self.print("Node not found")
            return False
        return True

    @get_name
    def click_minus(self) -> None:
        co = self.adb.find_img(target='minus_button')
        if co is None:
            self.better_sleep((0.2, 0.25))
            co = self.adb.find_img(target='minus_button')
        # print(x, y)

        x = co[0] + uniform(0, 30)
        y = co[1] + uniform(0, 27)
        # print(x, y)
        self.click(x, y)

    @get_name
    def click_plus(self) -> None:
        co = self.adb.find_img(target='plus_button')
        if co is None:
            self.better_sleep((0.2, 0.25))
            co = self.adb.find_img(target='plus_button')
        # print(x, y)
        x = co[0] + uniform(0, 30)
        y = co[1] + uniform(0, 27)
        # print(x, y)
        self.click(x, y)

    @get_name
    def restart_if_game_crashed(self):
        """
        Restart the game if the game crashed and start gathering gems
        """
        if not self.adb.is_game_alive():
            # try:
            #     self.leave_game()
            #     self.better_sleep((4, 5))
            # except:
            #     self.run_game()
            #     self.better_sleep((40, 60))
            #     self.check_resolve()
            #     self.leave_city()
            #     # print("premier leave city")
            #     self.better_sleep((1.5, 2))
            #     self.zoom_out_city()
            #     self.better_sleep((1.5, 2))
            #     self.scan_gem()
            #     self.better_sleep((0.125, 0.195))
            #     randomization = self.go_to(self.data[str(self.sel)]['schedules'][self.current_profile].get('city_x', 500), self.data[str(self.sel)]['schedules'][self.current_profile].get('city_y', 500))
            self.run_game()
            self.better_sleep((40, 60))
            self.check_resolve()
            self.leave_city()
            # print("premier leave city")
            self.better_sleep((1.5, 2))
            self.zoom_out_city()
            self.better_sleep((1.5, 2))
            self.scan_gem()
            self.better_sleep((0.125, 0.195))
            self.go_to(self.data[str(self.sel)]['schedules'][self.current_profile].get('city_x', 500),
                       self.data[str(self.sel)]['schedules'][self.current_profile].get('city_y', 500))

    @get_name
    def select_lineup_color(self, color: str) -> None:
        """
        Change the line-up until the yellow line-up is selected.
        """
        deadstop = 0
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
        while self.adb.find_img(target=f'{color}_icon', confidence=0.95) is None and self.adb.find_img(target=
                                                                                                       "troops_march_button") is not None:
            if deadstop == 5:
                self.click(uniform(700, 800), uniform(271, 300))
                self.better_sleep((0.557, 0.796))
                self.print("Error in line-up selection")
                self.set_text("Error in line-up selection")
                while True:
                    self.script_pause()
                    sleep(1)
            self.click(uniform(1092, 1114), uniform(225, 248))
            self.better_sleep((0.557, 0.796))
            deadstop = deadstop + 1
            self.print("Switching between line-up..")

    @get_name
    def find_cross(self) -> bool:
        """
        :return: True if node is occupied or someone is coming to the node
        :return: False if node is free to gather
        """
        self.print("Scanning the node..")
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        cropped_image = cv_image[230:480, 441:814]
        img = Image.fromarray(cropped_image)
        for i in range(img.size[0]):
            for y in range(img.size[1]):
                if (((img.getpixel((i, y))[0] < 5) and (img.getpixel((i, y))[1] < 5) and (
                        img.getpixel((i, y))[2] > 175) and (img.getpixel((i, y))[2] < 196) and (
                             (img.getpixel((i, y))[0] != 2) and (img.getpixel((i, y))[1] != 4) and (
                             img.getpixel((i, y))[2] != 183))) or
                        ((img.getpixel((i, y))[0] == 233) and (img.getpixel((i, y))[1] == 233) and (
                                img.getpixel((i, y))[2] == 233)) or
                        ((img.getpixel((i, y))[0] == 247) and (img.getpixel((i, y))[1] == 156) and (
                                img.getpixel((i, y))[2] == 47)) or
                        ((img.getpixel((i, y))[0] == 207) and (img.getpixel((i, y))[1] == 131) and (
                                img.getpixel((i, y))[2] == 40)) or
                        ((img.getpixel((i, y))[0] == 248) and (img.getpixel((i, y))[1] == 157) and (
                                img.getpixel((i, y))[2] == 48)) or
                        ((img.getpixel((i, y))[0] == 239) and (img.getpixel((i, y))[1] == 205) and (
                                img.getpixel((i, y))[2] == 165)) or
                        ((img.getpixel((i, y))[2] < 179) and (img.getpixel((i, y))[2] > 175) and (
                                img.getpixel((i, y))[1] > 116) and (img.getpixel((i, y))[1] < 119) and (
                                 img.getpixel((i, y))[0] < 2)) or
                        ((img.getpixel((i, y))[0] < 5) and (img.getpixel((i, y))[1] > 142) and (
                                img.getpixel((i, y))[1] < 150) and (img.getpixel((i, y))[2] < 200) and (
                                 img.getpixel((i, y))[2] > 190)) or
                        (img.getpixel((i, y)) == (0, 0, 178)) or
                        (img.getpixel((i, y)) == (2, 204, 2)) or
                        (img.getpixel((i, y)) == (195, 142, 0)) or
                        (img.getpixel((i, y)) == (0, 154, 14)) or
                        (img.getpixel((i, y)) == (0, 154, 13)) or
                        (img.getpixel((i, y)) == (1, 186, 0)) or
                        (img.getpixel((i, y)) == (0, 142, 193)) or
                        (img.getpixel((i, y)) == (12, 154, 1)) or
                        (img.getpixel((i, y)) == (1, 215, 0)) or
                        (img.getpixel((i, y)) == (1, 215, 0)) or
                        (img.getpixel((i, y)) == (1, 216, 0)) or
                        (img.getpixel((i, y)) == (253, 253, 253)) or
                        (img.getpixel((i, y)) == (49, 161, 255)) or
                        (img.getpixel((i, y)) == (2, 197, 2)) or
                        (img.getpixel((i, y)) == (247, 210, 167)) or
                        (img.getpixel((i, y)) == (255, 161, 49)) or
                        (img.getpixel((i, y)) == (253, 253, 253)) or
                        img.getpixel((i, y)) in [(167, 121, 28), (28, 121, 167)]):
                    self.print(f"{img.getpixel((i, y))}")
                    self.print("Node occupied")
                    return True
        return False

    @get_name
    def find_cross_enhanced(self, pil_image) -> bool:
        """
        :param: pil_image
        :return: False if node is free to gather
        """
        cv_image = array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        cropped_image = cv_image[230:480, 441:814]
        img = Image.fromarray(cropped_image)
        for i in range(img.size[0]):
            for y in range(img.size[1]):
                if ((img.getpixel((i, y)) == (0, 0, 178)) or (img.getpixel((i, y)) == (2, 204, 2)) or (
                        img.getpixel((i, y)) == (195, 142, 0)) or (img.getpixel((i, y)) == (0, 154, 14)) or (
                            img.getpixel((i, y)) == (0, 154, 13)) or (img.getpixel((i, y)) == (1, 186, 0)) or (
                            img.getpixel((i, y)) == (0, 142, 193)) or (
                            img.getpixel((i, y)) == (12, 154, 1)) or img.getpixel((i, y)) == (1, 215, 0)) or (
                        img.getpixel((i, y)) == (1, 215, 0)) or (img.getpixel((i, y)) == (1, 216, 0)) or (
                        img.getpixel((i, y)) == (253, 253, 253)) or (img.getpixel((i, y)) == (49, 161, 255)) or (
                        img.getpixel((i, y)) == (2, 197, 2)) or (
                        (img.getpixel((i, y))[0] == 247) and (img.getpixel((i, y))[1] == 156) and (
                        img.getpixel((i, y))[2] == 47) or
                        img.getpixel((i, y)) == (1, 214, 0)):
                    self.print(f"{img.getpixel((i, y))}")
                    self.print("Node occupied")
                    return True
        return False

    @get_name
    def find_cross_source(self, source) -> bool:
        """
        :param: pil_image or cv_image
        :return: True if node is occupied or someone is coming to the node
        :return: False if node is free to gather
        """
        img = Image.fromarray(source)
        for i in range(img.size[0]):
            for y in range(img.size[1]):
                if (((img.getpixel((i, y))[0] < 5) and (img.getpixel((i, y))[1] < 5) and (
                        img.getpixel((i, y))[2] > 175) and (img.getpixel((i, y))[2] < 196) and (
                             (img.getpixel((i, y))[0] != 2) and (img.getpixel((i, y))[1] != 4) and (
                             img.getpixel((i, y))[2] != 183))) or
                        ((img.getpixel((i, y))[0] == 233) and (img.getpixel((i, y))[1] == 233) and (
                                img.getpixel((i, y))[2] == 233)) or
                        ((img.getpixel((i, y))[0] == 247) and (img.getpixel((i, y))[1] == 156) and (
                                img.getpixel((i, y))[2] == 47)) or
                        ((img.getpixel((i, y))[0] == 207) and (img.getpixel((i, y))[1] == 131) and (
                                img.getpixel((i, y))[2] == 40)) or
                        ((img.getpixel((i, y))[0] == 248) and (img.getpixel((i, y))[1] == 157) and (
                                img.getpixel((i, y))[2] == 48)) or
                        ((img.getpixel((i, y))[0] == 239) and (img.getpixel((i, y))[1] == 205) and (
                                img.getpixel((i, y))[2] == 165)) or
                        ((img.getpixel((i, y))[2] < 179) and (img.getpixel((i, y))[2] > 175) and (
                                img.getpixel((i, y))[1] > 116) and (img.getpixel((i, y))[1] < 119) and (
                                 img.getpixel((i, y))[0] < 2)) or
                        ((img.getpixel((i, y))[0] < 5) and (img.getpixel((i, y))[1] > 142) and (
                                img.getpixel((i, y))[1] < 150) and (img.getpixel((i, y))[2] < 200) and (
                                 img.getpixel((i, y))[2] > 190)) or
                        (img.getpixel((i, y)) == (0, 0, 178)) or
                        (img.getpixel((i, y)) == (178, 0, 0)) or
                        (img.getpixel((i, y)) == (2, 204, 2)) or
                        (img.getpixel((i, y)) == (195, 142, 0)) or
                        (img.getpixel((i, y)) == (0, 142, 195)) or
                        (img.getpixel((i, y)) == (0, 154, 14)) or
                        (img.getpixel((i, y)) == (0, 154, 13)) or
                        (img.getpixel((i, y)) == (14, 154, 0)) or
                        (img.getpixel((i, y)) == (13, 154, 0)) or
                        (img.getpixel((i, y)) == (1, 186, 0)) or
                        (img.getpixel((i, y)) == (0, 186, 1)) or
                        (img.getpixel((i, y)) == (0, 142, 193)) or
                        (img.getpixel((i, y)) == (193, 142, 0)) or
                        (img.getpixel((i, y)) == (12, 154, 1)) or
                        (img.getpixel((i, y)) == (1, 154, 12)) or
                        (img.getpixel((i, y)) == (1, 215, 0)) or
                        (img.getpixel((i, y)) == (1, 216, 0)) or
                        (img.getpixel((i, y)) == (0, 215, 1)) or
                        (img.getpixel((i, y)) == (0, 216, 1)) or
                        (img.getpixel((i, y)) == (253, 253, 253)) or
                        (img.getpixel((i, y)) == (49, 161, 255)) or
                        (img.getpixel((i, y)) == (255, 161, 49)) or
                        (img.getpixel((i, y)) == (2, 197, 2)) or
                        (img.getpixel((i, y)) == (247, 210, 167)) or
                        (img.getpixel((i, y)) == (255, 161, 49)) or
                        (img.getpixel((i, y)) == (167, 210, 247)) or
                        (img.getpixel((i, y)) == (49, 161, 255)) or
                        (img.getpixel((i, y)) == (76, 150, 30)) or
                        (img.getpixel((i, y)) == (30, 150, 76)) or
                        img.getpixel((i, y)) in [(178, 118, 0), (0, 118, 178)] or
                        img.getpixel((i, y)) in [(167, 121, 28), (28, 121, 167)] or
                        img.getpixel((i, y)) in [(0, 143, 195), (195, 143, 0)]):
                    self.print(f"{img.getpixel((i, y))}")
                    self.print("Node occupied")
                    return True
        return False

    @get_name
    def already_mining(self, x, y, image) -> bool:
        """
        :param: x -> int - x location of the node
        :param: y -> int - y location of the node
        :param: image -> image - device screenshot
        :return: True if node is not free
        :return: False if node is free to gather
        """
        cv_image = array(image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        try:
            cropped_image = cv_image[y - 40:y + 50, x - 30:x + 50]
            # cv2.imwrite("gem_node.png", cropped_image)
            return self.find_cross_source(cropped_image)
        except Exception:
            if x < 50:
                x = 0
            if y < 30:
                y = 0
            cropped_image = cv_image[y:y + 50, x:x + 50]
            # cv2.imwrite("gem_node.png", cropped_image)
            return self.find_cross_source(cropped_image)

    @get_name
    def alliance_donation(self) -> None:
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

    @get_name
    def free_troop(self) -> bool:
        """
        :return: True if there's a empty queue
        :return: False if queues are occupied
        """
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = array(pil_image)
        cropped_image3 = cv_image[162:179, 1210:1242]
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        cropped_image1 = cv_image[162:179, 1212:1224]
        cropped_image2 = cv_image[162:178, 1228:1241]
        # cropped_image3 = cv_image[162:179, 1210:1242]
        # cv_image1 = cv2.cvtColor(cropped_image1, cv2.COLOR_BGR2GRAY)
        # cv_image2 = cv2.cvtColor(cropped_image2, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite("test1.png", cropped_image1)
        # cv2.imwrite("test2.png", cropped_image2)
        # cv2.imwrite("test3.png", cropped_image3)
        native_text = pytesseract.image_to_string(cropped_image3,
                                                  config=r'--oem 1 --psm 13 -c tessedit_char_whitelist=12345670/')
        text1 = pytesseract.image_to_string(cropped_image1,
                                            config=r'--oem 1 --psm 13 -c tessedit_char_whitelist=12345670/')
        text2 = pytesseract.image_to_string(cropped_image2,
                                            config=r'--oem 1 --psm 13 -c tessedit_char_whitelist=12345670/')
        # print(text0)
        # text1 = text1.replace("\n", "")
        # text2 = text2.replace("\n", "")
        # print(f"Text 1 : {text1} , Text 2 : {text2}")
        # self.set_text(f'[{current_time()}] Text 1 : {text1} , Text 2 : {text2}')
        # print(len(text1), len(text2))
        # logging.info(f"[{self.name}] Text 1 : {text1} , Text 2 : {text2}")
        # logging.info(f"[{self.name}] len(text1) : {len(text1)}, len(text2) : {len(text2)}")
        # if text1 == "" or text2 == "":
        #     return True
        print(f"[ {current_time()} ] [ {self.name} ] {native_text =}")
        if "/" in native_text:
            # list_text = text0.split("/")
            enhanced_text = native_text.split("/")[0] + native_text.split("/")[1]
        else:
            enhanced_text = native_text
        enhanced_text = enhanced_text.replace("\n", "")
        print(f"[ {current_time()} ] [ {self.name} ] {enhanced_text =}")
        if len(enhanced_text) < 2:
            return True
        if len(enhanced_text) == 2:
            return enhanced_text[0] < enhanced_text[1]
        # return text1 < text2 if len(text1) == 1 and len(text2) == 1 else False

    @get_name
    def claim_campaign(self):
        # Open du menu
        if self.adb.find_img(target='menu_opened', confidence=0.8) is None:
            x, y = uniform(1200, 1250), uniform(650, 690)
            self.click(x, y)
            self.better_sleep((1.725, 1.995))
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        cropped_image = cv_image[630:660, 843:895]

        number = pytesseract.image_to_string(cropped_image, config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=12345670.')
        # print(number)
        if not '.' in number:
            try:
                condition = int(number) > 15
            except Exception as e:
                condition = False
            if condition:
                self.click(uniform(808, 850), uniform(651, 692))
                self.better_sleep((1.3, 2.2))
                self.click(uniform(150, 266), uniform(250, 390))
                self.better_sleep((1.3, 2.2))
                self.click(uniform(101, 149), uniform(208, 255))
                self.better_sleep((1.3, 2.2))
                co = self.adb.find_img(target="chest_confirm_button")
                if co is not None:
                    self.click(co[0] + uniform(0, 149), co[1] + uniform(0, 20))
                    self.better_sleep((1.3, 2.2))
                for _ in range(2):
                    self.click(uniform(21, 56), uniform(14, 58))
                    self.better_sleep((1.3, 2.2))

    @get_name
    def claim_daily_chest(self):
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        chests = ['legendary_chest', 'material_chest', 'golden_chest', 'silver_chest']
        entered = False
        for chest in chests:
            co = self.adb.find_img_src_conf(cv_image, chest, 0.85)
            if co is not None:
                entered = True
                self.click(co[0] + uniform(0, 35), co[1] + uniform(0, 35))
                self.better_sleep((1.7, 3))
                open_chests = self.adb.find_multiple_img("open_chest")
                for open in open_chests:
                    self.click(open[0] + uniform(0, 127), open[1] + uniform(0, 47))
                    self.better_sleep((5, 8))
                    confirm = self.adb.find_img(target="confirm_tavern")
                    if confirm is not None:
                        self.click(confirm[0] + uniform(0, 127), confirm[1] + uniform(0, 47))
                        self.better_sleep((1.7, 3))
                        confirm = self.adb.find_img(target="confirm_tavern")
                        if confirm is not None:
                            self.click(confirm[0] + uniform(0, 127), confirm[1] + uniform(0, 47))
                            self.better_sleep((1.7, 3))

                if chest == 'legendary_chest':
                    self.click(uniform(25, 55), uniform(20, 56))
                    self.better_sleep((2.5, 5))
                    self.close_chest_popup()
                    pil_image = self.adb.get_curr_device_screen_img()
                    cv_image = array(pil_image)
                    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
                self.better_sleep((1.7, 3))

        if entered:
            self.click(uniform(25, 55), uniform(20, 56))
            self.better_sleep((1.7, 3))
            self.close_chest_popup()

    @get_name
    def free_troop_gem(self) -> bool:
        """
        :return: True if there's a empty queue
        :return: False if queues are occupied
        """

        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        cropped_image = cv_image[13:35, 1225:1254]
        cv_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(cv_image)
        text = text.replace("\n", "")
        if len(text) == 3:
            if text[0] < text[2]:
                self.print("Empty queue found")
                return True
            else:
                return False
        else:
            return False
        # return text[0] < text[2] if len(text) == 3 else False

    @get_name
    def get_number_free_troop(self) -> int:
        """
        :return: True if there's a empty queue
        :return: False if queues are occupied
        """
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        cropped_image1 = cv_image[162:179, 1212:1224]
        cropped_image2 = cv_image[162:178, 1228:1241]
        cropped_image3 = cv_image[162:179, 1210:1242]
        # cv_image1 = cv2.cvtColor(cropped_image1, cv2.COLOR_BGR2GRAY)
        # cv_image2 = cv2.cvtColor(cropped_image2, cv2.COLOR_BGR2GRAY)
        text1 = pytesseract.image_to_string(cropped_image1,
                                            config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=12345670/')
        text2 = pytesseract.image_to_string(cropped_image2,
                                            config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=12345670/')
        text1 = text1.replace("\n", "")
        text2 = text2.replace("\n", "")
        print("Text 1 : ", text1, "\nText 2 : ", text2)
        print(len(text1), len(text2))
        self.set_text(f'[{current_time()}] Text 1 : {text1} , Text 2 : {text2}')
        logging.info(f"[{self.name}] Text 1 : {text1} , Text 2 : {text2}")
        logging.info(f"[{self.name}] len(text1) : {len(text1)}, len(text2) : {len(text2)}")
        if text1 == "" and text2 == "":
            return 5
        return int(text2) - int(text1) if len(text1) == 1 and len(text2) == 1 else 0

    @get_name
    def use_enhanced_buff(self) -> None:
        buffs_to_do = []
        buffs_to_do.extend(self.get_remaining_buffs())

        self.print(f"Buffs : {buffs_to_do}")
        # logging.info(f"[ {self.name} ] Buffs : {buffs}")
        # buffs_to_do = []
        # for i in range(0, len(buffs), 2):
        #     # print("buff", buffs[i], buffs[i + 1])
        #     if buffs[i] is not None or buffs[i + 1] is not None:
        #         continue
        #     if buffs[i] is None and buffs[i + 1] is None:
        #         if i == 0:
        #             buffs_to_do.append("speed")
        #         elif i == 2:
        #             buffs_to_do.append("food")
        #         elif i == 4:
        #             buffs_to_do.append("wood")
        #         elif i == 6:
        #             buffs_to_do.append("gold")
        #         elif i == 8:
        #             buffs_to_do.append("stone")
        # self.print(f"Buffs remaining : {buffs_to_do}")
        # logging.info(f"[ {self.name} ] Buffs remaining : {buffs_to_do}")
        if buffs_to_do:
            temp3 = self.adb.find_img(target='menu_opened')
            if temp3 is None:
                x, y = uniform(1200, 1250), uniform(650, 690)
                # else:
                #     # x, y = temp3[0] + uniform(0, 20), temp3[1] + uniform(0, 15)
                self.click(x, y)
                self.better_sleep((0.725, 1.295))
            x, y = uniform(910, 950), uniform(650, 690)
            self.click(x, y)
            self.better_sleep((1.895, 2.3))
            x, y = uniform(490, 600), uniform(65, 100)
            self.click(x, y)
            self.better_sleep((1.195, 2))
            shuffle(buffs_to_do)
            if "speed" in buffs_to_do:
                buffs_to_do.remove("speed")
                buffs_to_do.insert(0, "speed")
            scrolled = False
            for element in buffs_to_do:
                # print(element)
                co = self.adb.find_img(target="no")
                if co is not None:
                    self.click(co[0] + uniform(0, 30), co[1] + uniform(1, 15))
                    self.better_sleep((1.9, 3))
                if element == "speed":
                    temp = self.adb.find_img(target='items\\enhanced_gathering_purple', confidence=0.80)
                    temp2 = self.adb.find_img(target='items\\enhanced_gathering_blue', confidence=0.80)
                    if temp is not None or temp2 is not None:
                        if temp is not None:
                            co = temp
                        else:
                            co = temp2
                        x, y = co[0] + uniform(0, 60), co[1] + uniform(0, 60)
                        self.click(x, y)
                        self.better_sleep((1.195, 2))
                        x, y = uniform(910, 1050), uniform(575, 622)
                        self.click(x, y)
                        self.better_sleep((1.195, 2))
                    #     continue
                    # if temp is not None:
                    #     x, y = temp[0] + uniform(0, 60), temp[1] + uniform(0, 60)
                    #     self.click(x, y)
                    #     self.better_sleep((1.195, 2))
                    #     x, y = uniform(910, 1050), uniform(575, 622)
                    #     self.click(x, y)
                    #     self.better_sleep((1.195, 2))
                    #     continue
                    # if temp is None and temp2 is not None:
                    #     x, y = temp2[0] + uniform(0, 60), temp2[1] + uniform(0, 60)
                    #     self.click(x, y)
                    #     self.better_sleep((1.195, 2))
                    #     x, y = uniform(910, 1050), uniform(575, 622)
                    #     self.click(x, y)
                    #     self.better_sleep((1.195, 2))
                if not scrolled:
                    scrolled = True
                    x1, y1 = uniform(586, 800), uniform(457, 487)
                    x2, y2 = x1 + uniform(-10, 10), y1 - uniform(300, 350)
                    self.swipe(x1, y1, x2, y2)
                if element != "speed":
                    temp = self.adb.find_img(target='items\\enhanced_' + element + '_blue')
                    temp2 = self.adb.find_img(target='items\\enhanced_' + element + '_green')
                    # print(f"{temp=} {temp2=}")
                    # if temp is None and temp2 is None:
                    #     # x1, y1 = uniform(586, 800), uniform(457, 487)
                    #     # x2, y2 = x1 + uniform(-10, 10), y1 - uniform(300, 350)
                    #     # self.swipe(x1, y1, x2, y2)
                    #     # self.better_sleep((2, 3))
                    #     temp = self.adb.find_img(target='items\\enhanced_' + element + '_blue')
                    #     temp2 = self.adb.find_img(target='items\\enhanced_' + element + '_green')
                    #     if temp is None and temp2 is None:
                    #         continue
                    # else:
                    if temp is not None or temp2 is not None:
                        if temp is not None:
                            co = temp
                        else:
                            co = temp2
                        x, y = co[0] + uniform(0, 60), co[1] + uniform(0, 60)
                        self.click(x, y)
                        self.better_sleep((1.195, 2))
                        x, y = uniform(910, 1050), uniform(575, 622)
                        self.click(x, y)
                        self.better_sleep((1.195, 2))
                    # if temp is not None:
                    #     x, y = temp[0] + uniform(0, 60), temp[1] + uniform(0, 60)
                    #     self.click(x, y)
                    #     self.better_sleep((1.195, 2))
                    #     x, y = uniform(910, 1050), uniform(575, 622)
                    #     self.click(x, y)
                    #     self.better_sleep((1.195, 2))
                    #     continue
                    # if temp is None and temp2 is not None:
                    #     x, y = temp2[0] + uniform(0, 60), temp2[1] + uniform(0, 60)
                    #     self.click(x, y)
                    #     self.better_sleep((1.195, 2))
                    #     x, y = uniform(910, 1050), uniform(575, 622)
                    #     self.click(x, y)
                    #     self.better_sleep((1.195, 2))

            co = self.adb.find_img(target="no")
            if co is not None:
                self.click(co[0] + uniform(0, 30), co[1] + uniform(1, 15))
                self.better_sleep((1.9, 3))
            self.better_sleep((1, 2))
            co = self.adb.find_img(target="cross")
            if co is not None:
                # print("Cross found")
                self.click(co[0] + uniform(0, 50), co[1] + uniform(0, 50))
                self.better_sleep((1, 2))

    @get_name
    def get_remaining_buffs(self):
        buffs_to_do = []
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = array(pil_image)
        image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        image = image[0:110, 0:680]
        here = False
        for buffs_string in ['purple', 'blue']:
            co = self.adb.find_img(source=image, target=f'buffs\\enhanced_gathering_{buffs_string}', confidence=0.8)
            if co is not None:
                here = True
                break
        if not here:
            buffs_to_do.append("speed")
        for rss_type in ['food', 'wood', 'stone', 'gold']:
            here = False
            for buff_type in ['blue', 'green']:
                co = self.adb.find_img(source=image, target=f'buffs\\enhanced_{rss_type}_{buff_type}', confidence=0.8)
                if co is not None:
                    here = True
                    break
            if not here:
                buffs_to_do.append(rss_type)
        return buffs_to_do

    @get_name
    def change_resource_type2(self, place: str) -> str:
        # print(f'[ {current_time()} ] [ {self.name} ] change_resource_type2 call')
        if place == "First":
            return "Second"
        elif place == "Second":
            return "Third"
        elif place == "Third":
            return "Fourth"
        elif place == "Fourth":
            return "Fifth"
        elif place == "Fifth":
            return "Sixth"
        elif place == "Sixth":
            return "Seventh"
        elif place == "Seventh":
            return "Done"

    @get_name
    def change_x_y_by_resource_type(self, place: str) -> tuple[float, float]:
        if self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "food":
            x, y = uniform(food_icon[0][0], food_icon[0][1]), uniform(food_icon[1][0], food_icon[1][1])
        elif self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "wood":
            x, y = uniform(wood_icon[0][0], wood_icon[0][1]), uniform(wood_icon[1][0], wood_icon[1][1])
        elif self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "stone":
            x, y = uniform(stone_icon[0][0], stone_icon[0][1]), uniform(stone_icon[1][0], stone_icon[1][1])
        else:  # Gold
            x, y = uniform(gold_icon[0][0], gold_icon[0][1]), uniform(gold_icon[1][0], gold_icon[1][1])
        # print(f'[ {current_time()} ] [ {self.name} ] chance rss type call')
        return x, y

    @get_name
    def minable(self) -> bool:
        if self.adb.find_img(target="search_button") is None and not self.find_cross():
            return True
        self.print("Unable to gather this node")
        return False

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

    @get_name
    def click_on_node(self) -> bool:
        """
        Click on node and click on send troop menu
        :return: True is successful
        :return: False is not successful
        """
        i = 0
        self.print("Clicking on the node..")
        while self.adb.find_img(target="resource_gather_button") is None:
            x, y = uniform(610, 650), uniform(340, 388)
            self.click(x, y)
            self.better_sleep((0.725, 0.995))
            i = i + 1
            if i == 4:
                return False
        self.better_sleep((1.0, 1.395))
        co = self.adb.find_img(target="resource_gather_button")
        if co is not None:
            x, y = co[0], co[1]
            self.click(x + uniform(0, 150), y + uniform(0, 30))
            self.better_sleep((1.325, 2.795))
            return True
        else:
            self.print("Unable to click on the node, leaving the node !")
            return False

    def click_on_fort1(self) -> bool:
        """
        Click on node and click on send troop menu
        :return: True is successful
        :return: False is not successful
        """
        i = 0
        while self.adb.find_img(target="red_rally_button") is None:
            x, y = uniform(610, 650), uniform(340, 388)
            self.click(x, y)
            self.better_sleep((0.725, 0.995))
            i = i + 1
            if i == 2:
                return False
        self.better_sleep((1.0, 1.395))
        co = self.adb.find_img(target="blue_rally_button")
        if co is not None:
            x, y = co[0], co[1]
            x, y = x + uniform(0, 150), y + uniform(0, 30)
            self.click(x, y)
            self.better_sleep((1.325, 1.795))
            return True
        else:
            return False

    @get_name
    def send_new_troop(self, deadstop=0, color='yellow') -> bool:
        """
        Send a new troop to gather the gem node
        :return: True is successfully
        :return: False is not successfully
        """

        self.print("Trying to send new troop..")
        print(f"[ {current_time()} ] [ {self.name} ] Send new troop count : {deadstop}")
        if deadstop == 5:
            self.click(uniform(700, 800), uniform(300, 500))
            self.better_sleep((1.325, 1.795))
            return False
        self.check_if_kill()
        co = self.adb.find_img(target="new_troops_button")
        if co is not None:
            # print("Home button found")
            x, y = co[0], co[1]
            x, y = x + uniform(0, 20), y + uniform(0, 20)
            self.click(x, y)
            self.better_sleep((1.825, 2.495))
            x_click, y_click = uniform(1090, 1111), uniform(329, 348)
            self.better_sleep((1.225, 1.795))
            self.select_lineup_color(color=color)
            for i in range(7):  # change if you have 6-7 troops
                self.check_if_kill()
                x_click, y_click = uniform(1096, 1118), uniform(282 + i * 54, 302 + i * 54)
                self.click(x_click, y_click)
                self.better_sleep((1, 2))
                if color != 'red':
                    cos = self.adb.find_multiple_img("choose_right", 0.8)
                    # for co in cos:
                    #     if co[0] > 1060 and co[1] > 200:
                    #         final.append(co)
                    final = list(filter(lambda co: co[0] > 1060 and co[1] > 200, cos))
                    if final != []:
                        x, y = self.adb.find_img(target="troops_march_button")
                        x, y = x + uniform(0, 20), y + uniform(0, 20)
                        self.check_if_kill()
                        self.click(x, y)
                        self.better_sleep((0.5, 0.7))
                        self.print("New Troop sent !")
                        return True

                # if self.adb.find_img(target="choose_right", confidence=0.8):
                #     x, y = self.adb.find_img(target="troops_march_button")
                #     x, y = x + uniform(0, 20), y + uniform(0, 20)
                #     self.check_if_kill()
                #     self.click(x, y)
                #     self.better_sleep((0.5, 0.7))
                #     return True
            self.check_if_kill()
            co = self.adb.find_img(target="troops_march_button")
            if co is None:
                return self.send_new_troop(deadstop=deadstop + 1)
            x, y = co[0], co[1]
            x, y = x + uniform(0, 20), y + uniform(0, 20)
            self.click(x, y)
            self.check_if_kill()
            self.better_sleep((0.5, 0.7))
            self.print("New Troop sent !")
            return True
        co = self.adb.find_img(target="march_bar")
        if co is not None and self.free_troop_gem():
            x, y = uniform(1177, 1250), uniform(80, 116)
            self.check_if_kill()
            self.better_sleep((0.5, 0.7))
            return self.send_new_troop(deadstop=deadstop + 1)
        self.print("Unable to send a new troop")
        return False

    @get_name
    def send_nearest_troop_gem(self, deadstop=0) -> bool:
        """
        Send the nearest troop to gather the gem node
        :return: True if successfully
        """

        try:
            for i in range(1, 4):
                points = self.adb.find_multiple_img(target=f"back_icon{i}")
                if points != []:
                    break
            if points == []:
                return False
            # if not points:
            #     points = self.adb.find_multiple_img("back_icon2")
            #     if not points:
            #         points = self.adb.find_multiple_img("back_icon3")
            #         if not points:
            #             return False
            timer = []
            for i in range(len(points)):
                self.click(points[i][0] + uniform(-20, 0), points[i][1] + uniform(-20, 0))
                self.better_sleep((1, 1.7))
                pil_image = self.adb.get_curr_device_screen_img()
                cv_image = array(pil_image)
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
                co = self.adb.find_img(source=cv_image, target="march_bar", confidence=0.8)
                if co is not None:
                    x, y = co[0], co[1]
                    cv_image = array(pil_image)
                    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
                    cropped_image = cv_image[y + 30:y + 50, x:x + 120]
                    # cv2.imwrite("timer.png", cropped_image)
                    string = pytesseract.image_to_string(cropped_image,
                                                         config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=1234567890:')
                    string = string.replace("\n", "")
                    # print(string)
                    datetime_object = datetime.strptime(string, '%H:%M:%S').time()
                    timer.append(
                        [datetime_object, (points[i][0] + uniform(-20, 0), points[i][1] + uniform(-20, 0)), (x, y)])

            def takeFirst(elem):
                return elem[0]

            timer.sort(key=takeFirst)
            fastest = timer[0][1]
            # print(timer)
            # print(fastest)
            self.click(x=fastest[0], y=fastest[1])
            self.better_sleep((0.9, 1.3))
            fastest = timer[0][2]
            # print(fastest)
            self.click(x=fastest[0] + uniform(90, 150), y=fastest[1] + uniform(-1, 20))
            self.better_sleep((0.9, 1.3))

            if self.adb.find_img(target="troops_march_button") is not None:
                self.click(x=uniform(1110, 1127), y=uniform(30, 55))
                self.better_sleep((0.9, 1.3))
                return self.send_new_troop()
            self.print("Nearest troop sent to the node..")
            return True
        except Exception as e:
            print(e)
            self.better_sleep((5, 10))
            if deadstop == 2:
                self.click(uniform(700, 720), uniform(300, 340))
                self.better_sleep((1, 3))
                return False
            return self.send_nearest_troop_gem(deadstop=deadstop + 1)

    @get_name
    def recall(self, nb_troop: int) -> bool:
        self.print('Recalling troops')
        print(nb_troop)
        x, y = uniform(1170, 1183), uniform(160, 175)
        self.click(x, y)
        self.better_sleep((1.595, 2))
        nb_to_go = nb_troop
        breakint = 0
        while nb_to_go > 0:
            print(nb_to_go)
            co = self.adb.find_img(target="return_button")
            while co is None and breakint != 4:
                print(
                    f'[ {current_time()} ] [ {self.name} ] Return button not found')

                y, x = uniform(290, 480), uniform(460, 560)
                x2, y2 = x + uniform(-30, 30), y + uniform(-200, -100)
                self.swipe(x, y, x2, y2)
                self.better_sleep((2, 3))
                co = self.adb.find_img(target="return_button")
                breakint += 1
            if co is not None:
                self.click(co[0] + uniform(0, 10), co[1] + uniform(0, 10))
            self.better_sleep((1.695, 2))
            nb_to_go = nb_to_go - 1
        sleep(0.5)
        x, y = uniform(1080, 1093), uniform(72, 88)
        self.click(x, y)
        return True

    @get_name
    def send_troop(self) -> bool:
        self.print("Trying to send a new troop..")
        if self.data[str(self.sel)]['schedules'][self.current_profile]['rss_custom_preset']:
            self.send_new_troop()
            self.better_sleep((0.7, 1.1))
        else:
            co = self.adb.find_img(target="new_troops_button")
            if co is None:
                return False
            x, y = co[0], co[1]
            x, y = x + uniform(0, 160), y + uniform(0, 30)
            self.click(x, y)
            self.better_sleep((2.325, 2.795))
            x, y = self.adb.find_img(target="troops_march_button")
            x, y = x + uniform(0, 80), y + uniform(0, 20)
            self.click(x, y)
            self.better_sleep((0.7, 1.1))
        if self.adb.find_img(target="troops_march_button") is not None:
            self.click(uniform(1106, 1123), uniform(36, 55))
            self.better_sleep((1.1, 1.5))
            self.print("Cannot send the troop")
            return False
        self.print("Troop sent !")
        return True

    @get_name
    def claim_daily_vip(self) -> None:
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv_image)
        if img.getpixel((186, 50)) == (0, 0, 227):
            self.click(uniform(100, 200), uniform(56, 69))
            self.better_sleep((1.25, 2))
            pil_image = self.adb.get_curr_device_screen_img()
            cv_image = array(pil_image)
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv_image)
            if img.getpixel((1041, 155)) == (0, 0, 227):
                self.click(uniform(1000, 1044), uniform(163, 192))
                self.better_sleep((2, 2.5))
                self.click(uniform(1082, 1100), uniform(73, 90))
                self.better_sleep((2, 2.5))
            co = self.adb.find_img(target="claim_daily")
            if co is not None:
                self.click(uniform(co[0] - 5, co[0] + 80), uniform(co[1], co[1] + 25))
                self.better_sleep((4.5, 6))
                self.click(uniform(300, 1000), uniform(33, 87))
                self.better_sleep((1.25, 2))
            self.click(uniform(1082, 1100), uniform(73, 90))
            self.better_sleep((1.25, 2))

    @get_name
    def wait_until_connected(self) -> None:
        self.print("Script is paused until reconnected..")
        condition = True
        while condition:
            co = self.adb.find_img(target="menu_button", confidence=0.8)
            if co is not None:
                condition = False
            co = self.adb.find_img(target="hammer", confidence=0.8)
            if co is not None:
                condition = False
            co = self.adb.find_img(target="mightiest_gov", confidence=0.8)
            if co is not None:
                self.click(uniform(co[0] + 5, co[0] + 20), uniform(co[1] + 5, co[1] + 20))
                condition = False
            self.better_sleep((10, 15))
            self.check_reconnect()

    @get_name
    def run_game(self, count=0) -> None:
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a", )
        # self.adb.connect_to_device()
        a = self.adb.is_game_alive()
        if a:
            print(f"[ {current_time()} ] [ {self.name} ] Looks like game is running ")
        if not a:
            print(f"[ {current_time()} ] [ {self.name} ] Looks like game is not running ")
            co = self.adb.find_img(target="rokicon", confidence=0.8)
            print(f"{co =}")
            if co is not None:
                self.click(co[0], co[1])
                return self.wait_until_connected()
            else:
                if count == 0:
                    self.adb.home_button()
                    sleep(3)
                    return self.run_game(count=1)
                if count == 1:
                    if self.language is None or self.language == "eng":
                        for _ in range(2):
                            string = self.adb.get_device().shell("am start -n com.lilithgame.roc.gp/com.harry.engine.MainActivity")
                            # print(f"{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }")
                            logging.info(
                                f"[{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }")
                            if 'Error' in str(string):
                                break
                            if 'Activity not started' not in str(string):
                                self.print("Starting the game !")
                                self.wait_until_connected()
                                self.language = "eng"
                                return self.run_game(count=2)
                            if 'Activity not started' in str(string):
                                return
                    if self.language is None or self.language == "vn":
                        for i in range(2):
                            string = self.adb.get_device().shell("am start -n com.rok.gp.vn/com.harry.engine.MainActivity")
                            # print(f"{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }")
                            logging.info(
                                f"[{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }")
                            if 'Error' in str(string):
                                # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] shell dumpsys activity activities')
                                return
                            if 'Activity not started' not in str(string):
                                self.print("Starting the game !")
                                self.wait_until_connected()
                                self.language = "vn"
                                return self.run_game(count=2)
                            if 'Activity not started' in str(string):
                                return
                    if self.language is None or self.language == "kr":
                        for i in range(2):
                            string = self.adb.get_device().shell(
                                "am start -n com.lilithgame.rok.gpkr/com.harry.engine.MainActivity")
                            # print(f"{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }")
                            logging.info(
                                f"[{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }")
                            if 'Error' in str(string):
                                # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] shell dumpsys activity activities')
                                return
                            if 'Activity not started' not in str(string):
                                self.print("Starting the game !")
                                self.wait_until_connected()
                                self.language = "kr"
                                return self.run_game(count=2)
                            if 'Activity not started' in str(string):
                                return

                self.print("ERROR CANNOT START THE GAME.")
                while True:
                    self.set_status("ERROR CANNOT START GAME")
                    self.script_pause()
                    sleep(1)

        #
        # print(f"[{self.name} ] Game is active.")
        # self.set_text(f'[{current_time()}]  Game is active.')
        # logging.info(f"[{self.name}] Game is active.")

    @get_name
    def resolve_captcha(self, compteur=0):
        """
        Resolve verification
        """
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
        print(f"[ {current_time()} ] [ {self.name} ] Resolve count = {compteur}")
        if compteur>5:
            self.print("Error in resolving the captcha, human action needed.")
            self.status("Error")
            while True:
                self.script_pause()
                sleep(1)
        try:
            pil_image = self.adb.get_curr_device_screen_img()
            cv_image = array(pil_image)
            cropped_image = cv_image[100:560, 440:840]
            cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(cropped_image)

            im_pil.save(f"captcha{self.sel}.jpg", optimize=True, quality=80)
            sleep(0.5)
            size = os.path.getsize(os.path.abspath(os.getcwd()) + f"captcha{self.sel}.jpg")
            if size > 99999:
                self.print(f"Captcha is too big ({size}), refreshing it..")
                self.adb.click(uniform(508, 532), uniform(580, 596))
                self.better_sleep((4,7))
                return self.resolve_captcha(compteur+1)
            result = verification.solve(f"captcha{self.sel}.jpg", self.sel)
            if result == 0:
                if compteur >= 3:
                    self.click(uniform(100, 300), uniform(100, 400))
                    self.better_sleep((2, 3))
                    return None
                co = self.adb.find_img(target="refresh_resolve", confidence=0.90)
                # print(f"{co = }")
                if co is not None:
                    x, y = co[0] + 3, co[1] + 3
                    self.click(x, y)
                    self.better_sleep((2, 3))
                return self.resolve_captcha(compteur=compteur + 1)
            if result['code'] is None:
                co = self.adb.find_img(target="refresh_resolve", confidence=0.9)
                # print(f"{co = }")
                if co is not None:
                    x, y = co[0] + 3, co[1] + 3
                    self.click(x, y)
                    self.better_sleep((2, 3))
                return self.resolve_captcha(compteur=compteur + 1)
            if result['code'] == 0:
                if compteur >= 3:
                    self.click(uniform(100, 300), uniform(100, 400))
                    self.better_sleep((2, 3))
                    return None
                co = self.adb.find_img(target="refresh_resolve", confidence=0.9)
                # print(f"{co = }")
                if co is not None:
                    x, y = co[0] + 3, co[1] + 3
                    self.click(x, y)
                    self.better_sleep((2, 3))
                return self.resolve_captcha(compteur=compteur + 1)

            co = verification.string_to_co(result['code'])
            if self.adb.find_img_cv(cropped_image) is not None:
                for x, y in co:
                    self.click(x, y)
                    self.better_sleep((0.4, 0.795))
                self.click(uniform(700, 830), uniform(570, 600))
                self.better_sleep((1, 1.795))
            return result['captchaId']
        except Exception as e:
            print(f"[ {current_time()} ] [ {self.name} ] Exception raised during the resolving of the captcha (task.py related) :\n{e}")
            logging.info(f"[{self.name}] Exception raised during the resolving of the captcha (task.py related) :\n{e}")
            self.click(uniform(507, 533), uniform(573, 599))
            self.print("Refreshing the captcha.")
            self.better_sleep((4, 7))
            return self.resolve_captcha(compteur=compteur + 1)

    def script_pause(self):
        try:
            said = False
            while self.frame.pause:
                if not said:
                    print(f"[ {current_time()} ] [ {self.name} ] Script is paused.")
                    logging.info(f"[{self.name}] Script is paused.")
                    self.set_text(f"[{current_time()}] Script is paused.")
                    said = True
                    # self.set_text("Script paused.")
                sleep(1)

            if self.frame.stop:
                self.frame.stop = False
                sys.exit(1)
        except:
            sys.exit(1)

    @get_name
    def zoom_out_city(self) -> None:
        """
        Leave the city by sending 'F5' key signal to the emulator
        """

        self.script_pause()
        try:
            self.print("Zooming out..")
            co = self.adb.find_img(target='gem_search_button')
            if co is not None:
                hwnd = win32gui.FindWindow(None, self.adb.name)
                hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)
                for _ in range(4):
                    self.script_pause()
                    boolean = self.adb.find_img(target="gem_search_button")
                    if boolean is not None:
                        for _ in range(2):
                            self.script_pause()
                            win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
                            win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, win32con.VK_F6, 0)
                            sleep(0.20)
                            win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
                            win32api.PostMessage(hwndChild, win32con.WM_KEYUP, win32con.VK_F6, 0)
                            self.better_sleep((1.4, 2))
                    else:
                        break
        except Exception as e:
            print(e)

    @get_name
    def go_to(self, x, y, last=None) -> int:
        """
        Define starting path
        :param: x -> int x map location
        :param: y -> int y map location
        :return: starting location between 0,1,2,3
        """
        radius = self.data[str(self.sel)]['schedules'][self.current_profile].get('radius')
        randomization = randint(0, 3)

        while randomization == last or None:
            randomization = randint(0, 3)

        print(f"[ {current_time()} ] [ {self.name} ] The bot selected the path nº{randomization}.")
        self.set_text(f'[{current_time()}] The bot selected the path nº{randomization}.')

        coordinates = {
            0: (x - int((radius * (4 / 3))) + randint(2, 8), y + int((radius * (4 / 3))) + randint(-8, -2)),
            1: (x + int((radius * (4 / 3))) + randint(-8, -2), y + int((radius * (4 / 3))) + randint(-8, -2)),
            2: (x + int((radius * (4 / 3))) + randint(-8, -2), y - int((radius * (4 / 3))) + randint(2, 8)),
            3: (x - int((radius * (4 / 3))) + randint(2, 8), y - int((radius * (4 / 3))) + randint(2, 8))
        }
        # if randomization == 0:
        #     print(f"[ {current_time()} ] [ {self.name} ] The bot will now go in the top left corner")
        #     self.set_text(f'[{current_time()}] The bot will now go in the top left corner.')
        #     x2, y2 = x - int((radius * (4 / 3))) + randint(2, 8), y + int((radius * (4 / 3))) + randint(-8, -2)
        # elif randomization == 1:
        #     print(f"[ {current_time()} ] [ {self.name} ] The bot will now go in the top right corner")
        #     self.set_text(f'[{current_time()}] The bot will now go in the top right corner.')
        #     x2, y2 = x + int((radius * (4 / 3))) + randint(-8, -2), y + int((radius * (4 / 3))) + randint(-8, -2)
        # elif randomization == 2:
        #     print(f"[ {current_time()} ] [ {self.name} ] The bot will now go in the bottom right corner")
        #     self.set_text(f'[{current_time()}] The bot will now go in the bottom right corner.')
        #     x2, y2 = x + int((radius * (4 / 3))) + randint(-8, -2), y - int((radius * (4 / 3))) + randint(2, 8)
        # else:# if randomization == 3:
        #     print(f"[ {current_time()} ] [ {self.name} ] The bot will now go in the bottom left corner")
        #     self.set_text(f'[{current_time()}] The bot will now go in the bottom left corner.')
        #     x2, y2 = x - int((radius * (4 / 3))) + randint(2, 8), y - int((radius * (4 / 3))) + randint(2, 8)

        x2, y2 = coordinates[randomization][0], coordinates[randomization][1]
        x3, y3 = uniform(290, 400), uniform(15, 26)
        self.click(x3, y3)
        self.better_sleep((0.3, 0.5))
        for i in range(2):
            self.click(uniform(400, 480), uniform(130, 150))
            self.better_sleep((0.3, 0.5))
            if i == 0:
                # string = "input keyevent --longpress 67 67 67 67 67"
                string = "input keyevent 67 67 67 67 67 67"
                self.adb.get_device().shell(string)
                self.better_sleep((0.3, 0.5))
                self.adb.get_device().shell(
                    f"input text {self.data[str(self.sel)]['schedules'][self.current_profile].get('kingdom')}")
                self.better_sleep((0.3, 0.5))
        self.better_sleep((0.3, 0.5))
        for i in range(2):
            self.click(uniform(590, 685), uniform(130, 150))
            self.better_sleep((0.3, 0.5))
            if i == 0:
                string = f'input text {x2}'
                self.adb.get_device().shell(string)
                self.better_sleep((0.3, 0.5))
        self.better_sleep((0.3, 0.5))
        for i in range(2):
            self.click(uniform(750, 830), uniform(130, 150))
            self.better_sleep((0.3, 0.5))
            if i == 0:
                string = f'input text {y2}'
                self.adb.get_device().shell(string)
                self.better_sleep((0.3, 0.5))
        self.better_sleep((0.3, 0.5))
        for _ in range(2):
            self.click(uniform(860, 900), uniform(123, 158))
        self.better_sleep((1, 2))
        return randomization

    @get_name
    def click_on_fort(self) -> bool:
        i = 0
        while co:=self.adb.find_img(target="fort_rally_button1") is None:
            x, y = uniform(610, 650), uniform(340, 388)
            self.click(x, y)
            self.better_sleep((0.725, 0.995))
            i = i + 1
            if i == 4:
                return False
        self.better_sleep((1.0, 1.395))
        # co = self.adb.find_img(target="fort_rally_button1")
        if co is not None:
            x, y = co[0], co[1]
            x, y = x + uniform(0, 144), y + uniform(0, 30)
            self.click(x, y)
            self.better_sleep((1.325, 1.795))
            return True
        else:
            return False

    @get_name
    def scan_gem(self):
        """
        Scan device screenshot to find gem node,          not 100% working need improvement
        :return: None
        """
        self.data = self.update_data()
        self.restart_if_game_crashed()
        screen = self.adb.get_cv2_img()

        info_screen = screen[470:700, 0:115]
        cropped_image = screen[420:540, 480:810]

        if random() > 0.7:
            co = self.adb.find_img(source=screen, target="verification_button", confidence=0.8)
            if co is not None:
                self.check_resolve()
            self.check_reconnect(cropped_image)

        if random() > 0.4:
            self.check_download_page(screen)
            self.leave_kd_buff(screen)

        cropped_image = screen[616:710, 1168:1270]

        if self.adb.find_img(source=cropped_image, target="map_icon", confidence=0.8) is not None:
            self.click(uniform(500, 700), uniform(250, 450))
            self.better_sleep((1, 2))
            return self.zoom_out_city()

        if self.adb.find_img(source=info_screen, target="hammer", confidence=0.8) is not None:
            self.click(uniform(24, 91), uniform(625, 680))
            self.better_sleep((1.5, 2))
            self.zoom_out_city()
            self.better_sleep((2, 3))
            screen = self.adb.get_cv2_img()

        if self.adb.find_img(source=info_screen, target="gem_search_button", confidence=0.8) is not None:
            self.zoom_out_city()
            self.better_sleep((2, 3))
            screen = self.adb.get_cv2_img()

        for second_string in ["left", "mid", "right"]:
            for first_string in ["up", "mid", "down"]:
                self.check_if_kill()
                co = self.validate_co(self.adb.find_img(source=screen, target=f"gem_icon_day_{first_string}_{second_string}", confidence=0.8))
                if co is None:
                    co = self.validate_co(self.adb.find_img(source=screen, target=f"gem_icon_night_{first_string}_{second_string}", confidence=0.8))
                if co is not None:
                    self.print(f"Gem node Found - x: {co[0]} y:{co[1]}")
                    self.check_if_kill()
                    if self.already_mining(co[0], co[1], screen):
                        self.print(f"Already mining this gem node")
                        continue
                    self.print(f"Node x:{co[0]}, y:{co[1]}")
                    self.click(co[0], co[1])
                    x_click = co[0]
                    y_click = co[1]
                    self.better_sleep((2, 2.5))
                    self.check_if_kill()
                    self.check_resolve()
                    while True:
                        self.leave_kd_buff()
                        if self.check_log_back():
                            self.print("You interrupted gem gathering by connecting from an other device, bot is restarting it")
                            return self.gather_gem()
                        screen = self.adb.get_cv2_img()
                        cv_image = screen[0:100, 0:800]
                        if self.adb.find_img(target="block_icon", source=cv_image, confidence=0.9) is not None:
                            self.print("Bot detected the block icon, now cancelling the function..")
                            return False

                        if self.find_cross():
                            return self.adjusted_leave_city(x_click, y_click)

                        if not self.click_on_node():
                            return self.adjusted_leave_city(x_click, y_click)

                        if self.free_troop_gem():
                            self.click(uniform(1172, 1222), uniform(77, 112))
                            # self.better_sleep((0.6, 1))
                            self.check_if_kill()

                        self.better_sleep((1.3, 2))
                        # print(f'[ {current_time()} ] [ {self.name} ] Trying to send new troop..')
                        # logging.info(f"[{self.name}] Trying to send new troop..")
                        # self.set_text(f'[{current_time()}] Trying to send new troop..')

                        if self.send_new_troop():
                            self.check_if_kill()
                            break
                        # else:
                        #     print(f'[ {current_time()} ] [ {self.name} ] Unable to send a new troop')
                        #     logging.info(f"[{self.name}] Unable to send a new troop")
                        #     self.set_text(f'[{current_time()}] Unable to send a new troop')

                        # print(f'[ {current_time()} ] [ {self.name} ] Trying to send the nearest troop..')
                        # logging.info(f"[{self.name}] Trying to send the nearest troop..")
                        # self.set_text(f'[{current_time()}] Trying to send the nearest troop..')
                        self.print("Trying to send the nearest troop..")
                        if self.send_nearest_troop_gem():
                            if self.adb.find_img(target="new_troops_button"):
                                # print(f'[ {current_time()} ] [ {self.name} ] Sending a new troop')
                                # logging.info(f"[{self.name}] Sending a new troop")
                                # self.set_text(f'[{current_time()}] Sending a new troop')
                                self.send_new_troop()
                                self.check_if_kill()
                            self.check_if_kill()
                            break
                        else:
                            self.print("All queues are occupied")

                        self.check_if_kill()
                        self.click(uniform(400, 700), uniform(300, 400))
                        self.better_sleep((1.8, 3))
                        self.check_resolve()

                        scan_frequency = randint(
                            self.data[str(self.sel)]['schedules'][self.current_profile].get("gem_check1"),
                            self.data[str(self.sel)]['schedules'][self.current_profile].get("gem_check2")
                        )

                        self.print(f"Script is paused for {scan_frequency} seconds")
                        scan_frequency_timer = 0

                        for i in range(scan_frequency):
                            self.script_pause()
                            if self.check_log_back():
                                self.print("You interrupted gem gathering by connecting from an other device, bot is restarting it")
                                return self.gather_gem()
                            sleep(1)
                            scan_frequency_timer += 1
                            if scan_frequency_timer >= 20:
                                self.run_game()
                                timer_image = self.adb.get_cv2_img()
                                cross_image = timer_image[240:490, 490:790]
                                back_image = timer_image[150:477, 1160:]
                                if self.find_cross_source(cross_image):
                                    return self.adjusted_leave_city(x_click, y_click)
                                if self.data[str(self.sel)]['schedules'][self.current_profile].get("gem_experimental"):
                                    if self.adb.find_img(target="back_normal_view", source=back_image, confidence=0.9) is not None:
                                        self.print("Bot detected a troop is going back to the city, now bypassing the sleep time..")
                                        break
                                scan_frequency_timer = 0
                    self.better_sleep((1, 1.895))
                    self.check_resolve()
                    return self.adjusted_leave_city(x_click, y_click)

    @get_name
    def swipe_scan(self, scan, direction):
        self.check_if_kill()
        self.script_pause()
        # print(f'[ {current_time()} ] [ {self.name} ] {direction = } {scan = }')
        direction()
        self.better_sleep((1, 1.25))
        return scan()

    @get_name
    def clear_fog(self, starting_time=None):
        self.data = self.update_data()
        self.leave_city()
        self.better_sleep((1, 1.895))
        self.go_city()
        if starting_time is None:
            starting_time = time()
        time_restart = time()
        if self.data[str(self.sel)]['schedules'][self.current_profile].get('scout_duration1', 60) > \
                self.data[str(self.sel)]['schedules'][self.current_profile].get('scout_duration2', 90):
            self.data[self.sel]['schedules'][self.current_profile]['scout_duration1'], \
                self.data[self.sel]['schedules'][self.current_profile]['scout_duration2'] = \
                self.data[self.sel]['schedules'][self.current_profile]['scout_duration2'], \
                    self.data[self.sel]['schedules'][self.current_profile]['scout_duration1']

        generated_time = (
                randint(self.data[str(self.sel)]['schedules'][self.current_profile].get('scout_duration1'),
                        self.data[str(self.sel)]['schedules'][self.current_profile].get('scout_duration2')) * 60)
        time_to_beat = starting_time + generated_time
        self.print(f"Clearing fog for ~{generated_time // 60} minutes")
        count = False
        while time_to_beat > time():
            if self.check_log_back():
                self.print(f"You interrupted fog exploration by connecting from an other device, bot is restarting it")
                return self.clear_fog(starting_time)
            self.check_reconnect()
            if not count:
                x, y = self.data[str(self.sel)]['schedules'][self.current_profile].get('scout_building_x', 750), \
                    self.data[str(self.sel)]['schedules'][self.current_profile].get(
                        'scout_building_y', 750)
                self.click(uniform(x - 10, x + 10), uniform(y - 10, y - 10))
                self.better_sleep((1.25, 1.75))
                co = self.adb.find_img(target="scout_button")
                for _ in range(2):
                    if co is None:
                        self.print("Unable to find the scout button")
                        sleep(5)
                        co = self.adb.find_img(target="scout_button")
                if co is None:
                    co = self.adb.find_img(target="scout_button2")
                    for _ in range(2):
                        if co is None:
                            self.print("Unable to find the scout button")
                            sleep(5)
                            co = self.adb.find_img(target="scout_button2")
                if co is None:
                    self.print("Unable to find the scout button, try to place the building in the center of your city so the bot can see the icons.")
                    return
                self.click(uniform(co[0], co[0] + 30), uniform(co[1], co[1] + 30))
                self.better_sleep((3, 4.5))

            co = self.adb.find_img(target="explore_button_scout")
            if co is not None:
                self.click(uniform(co[0], co[0] + 100), uniform(co[1], co[1] + 25))
                self.better_sleep((3, 4.5))
                co = self.adb.find_img(target="explore_button_fog")
                if co is not None:
                    self.click(uniform(co[0], co[0] + 60), uniform(co[1], co[1] + 30))
                    self.better_sleep((3, 4.5))
                co = self.adb.find_img(target="send_button_scout")
                if co is not None:
                    self.click(uniform(co[0], co[0] + 90), uniform(co[1], co[1] + 30))
                    self.better_sleep((3, 4.5))
                self.print("Scout sent!")
                self.check_resolve()
                self.go_city()
                self.better_sleep((3, 4.5))
                count = False
            else:
                time_to_sleep = randint(5, 10)
                self.print(f"All scout seems occupied, waiting for {time_to_sleep:0.1f} seconds")
                count = True
                for _ in range(time_to_sleep):
                    self.script_pause()
                    sleep(1)

    @get_name
    def clear_all_healing(self):
        for i in range(2):
            buttons = self.adb.find_multiple_img("healing_scroll")
            pil_image = self.adb.get_curr_device_screen_img()
            cv_image = array(pil_image)
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            # cv2.imwrite("timer.png", cropped_image)
            for button in buttons:
                cropped_image = cv_image[button[1]:button[1] + 25, 950:1020]
                string = pytesseract.image_to_string(cropped_image,
                                                     config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=1234567890:')
                string = string.replace("\n", "")
                if string not in ["0", ""]:
                    self.click(uniform(950, 1020), uniform(button[1] + 5, button[1] + 20))
                    self.better_sleep((1, 1.5))
                    string = "input keyevent 67 67 67 67 67 67 67 67 67"
                    self.adb.get_device().shell(string)
                    self.better_sleep((1, 1.5))
                    self.adb.get_device().shell("input text 0")
                    self.better_sleep((1, 1.5))
                    for _ in range(2):
                        self.click(uniform(200, 500), uniform(180, 460))
                    self.better_sleep((1, 1.5))
            if len(buttons) < 3 and i == 0:
                break
            if i == 0:
                self.swipe(uniform(740, 780), uniform(436, 450), uniform(740, 780), uniform(140, 150))
                self.better_sleep((1, 1.5))
        self.swipe(uniform(740, 780), uniform(140, 150), uniform(740, 780), uniform(630, 650))
        self.better_sleep((1, 1.5))

    @get_name
    def close_chest_popup(self):
        for i in range(2):
            co = self.adb.find_img(f"popup{i}")
            if co is not None:
                self.click(uniform(1102, 1030), uniform(92, 118))
                self.better_sleep((2, 4))

    @get_name
    def heal_troops(self):
        # self.go_city(
        if self.data[str(self.sel)]['schedules'][self.current_profile].get('heal_troop'):
            tier_icons = []
            tiers = [1, 2, 3, 4, 5]
            for tier in tiers:
                cos = self.adb.find_multiple_img(f"t{tier}_badge", 0.65)
                cos = list(filter(filter_coordinate, cos))
                tier_icons.extend(cos)
            if tier_icons is not None and len(tier_icons) != 0:
                print(tier_icons)
                shuffle(tier_icons)
                self.click(tier_icons[0][0] + uniform(-5, 20), tier_icons[0][1] + uniform(-15, 10))
                self.better_sleep((1, 1.8))
            self.print("après les tier_icons")
            # print(f"{self.data[str(self.sel)]['schedules'][self.current_profile].get('healing_building_x') =}")
            healing_hut = (
                self.data[str(self.sel)]['schedules'][self.current_profile].get('healing_building_x') + uniform(-5, 5),
                self.data[str(self.sel)]['schedules'][self.current_profile].get('healing_building_y') + uniform(-5, 5)
            )
            self.print(f"Healing building placement (randomised) : {healing_hut}")
            self.click(healing_hut[0], healing_hut[1])
            # print("après les healing_hut")
            co = self.adb.find_img(target="heal_icon")
            if co is None:
                co = self.adb.find_img(target="heal_icon")
            if co is None:
                self.print(f"Healing not found")
                return
            if self.adb.find_img(target="speedup_healing") is not None:
                self.print("Speed-up button found, can't heal more troops..")
                return
            self.print(f"{co =}")
            self.click(co[0] + uniform(0, 60), co[1] + uniform(0, 60))

            # print(f'[ {current_time()} ] [ {self.name} ] Bot will now look for the healing icon..')
            # logging.info(f"[{self.name}] Bot will now look for the healing icon..")
            # while self.adb.find_img("heal_icon") is None:
            #     sleep(uniform(30,40))
            # print(f'[ {current_time()} ] [ {self.name} ] Healing icon found')
            # logging.info(f"[{self.name}] Healing icon found")
            # x,y = self.adb.find_img("heal_icon")
            # self.click(x,y)
            self.better_sleep((1.5, 2.4))
            cv_image = self.adb.get_cv2_img()
            cropped_image = cv_image[541:568, 265:434]
            # cv2.imwrite("timer.png", cropped_image)
            string = pytesseract.image_to_string(cropped_image,
                                                 config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=1234567890/,')
            string = string.replace("\n", "")
            for i in range(4):
                string = string.replace(",", "")
            nb_heal = string.split("/")
            print(string, nb_heal)
            if int(self.data[str(self.sel)]['schedules'][self.current_profile].get('healing_count')) > int(nb_heal[0]):
                self.click(uniform(880, 1018), uniform(560, 600))
                self.better_sleep((1, 1.5))
                self.click_help()
                return
            if self.adb.find_img(target="healing_scroll") is None:
                self.click(uniform(1083, 1098), uniform(71, 92))
                return self.better_sleep((1.5, 2.4))
            self.clear_all_healing()
            self.click(uniform(960, 1010), uniform(220, 237))
            self.better_sleep((0.5, 1))
            string = "input keyevent 67 67 67 67 67 67 67 67 67"
            self.adb.get_device().shell(string)
            self.better_sleep((0.3, 0.5))
            self.adb.get_device().shell(
                f"input text {self.data[str(self.sel)]['schedules'][self.current_profile].get('healing_count')}")
            self.better_sleep((1, 1.5))
            self.click(uniform(187, 170), uniform(226, 400))
            self.click(uniform(880, 1018), uniform(560, 600))
            self.better_sleep((1, 1.5))
            self.click_help()

    @get_name
    def produce_materials(self):
        self.data = self.update_data()
        # co = self.adb.find_img("forge_icon")
        # if co is not None:
        #     self.click(co[0] + uniform(0, 24), co[1] + uniform(80, 100))
        #     self.better_sleep((1, 1.5))
        # else:
        strings = ["forge_icon", "bones_icon", "ebony_icon", "leather_icon", "stone_icon"]
        for string in strings:
            co = self.adb.find_img(string)
            if co is not None:
                if string != "forge_icon":
                    self.click(co[0] + uniform(0, 24), co[1] + uniform(0, 24))
                    self.better_sleep((1, 1.5))
                self.click(co[0] + uniform(0, 24), co[1] + uniform(80, 100))
                self.better_sleep((1, 1.5))
                break
        co = self.adb.find_img(target="forge_button")
        if co is not None:
            self.click(co[0] + uniform(0, 50), co[1] + uniform(0, 60))
            self.better_sleep((1, 1.5))
            cv_image = self.adb.get_cv2_img()
            nb = 0
            for i in range(1, 6):
                co = self.adb.find_img(target=f"forge_{i}", source=cv_image, confidence=0.9)
                if co is not None:
                    nb = 6 - i
                    break
            if nb != 0:
                for i in range(1, nb + 1):
                    materials = {
                        "leather": (uniform(737, 785), uniform(208, 255)),
                        "stone": (uniform(830, 880), uniform(208, 255)),
                        "ebony": (uniform(922, 972), uniform(208, 255)),
                        "bones": (uniform(1018, 1064), uniform(208, 255)),
                    }
                    string = self.data[self.sel]['schedules'][self.current_profile][f'material_choice_{i}']

                    self.click(materials[string][0], materials[string][1])

                    # if self.data[self.sel]['schedules'][self.current_profile][f'material_choice_{i}'] == "leather":
                    #     self.click(uniform(737, 785), uniform(208, 255))
                    # if self.data[self.sel]['schedules'][self.current_profile][f'material_choice_{i}'] == "stone":
                    #     self.click(uniform(830, 880), uniform(208, 255))
                    # if self.data[self.sel]['schedules'][self.current_profile][f'material_choice_{i}'] == "ebony":
                    #     self.click(uniform(922, 972), uniform(208, 255))
                    # if self.data[self.sel]['schedules'][self.current_profile][f'material_choice_{i}'] == "bones":
                    #     self.click(uniform(1018, 1064), uniform(208, 255))
                    self.better_sleep((0.5, 1.2))
            self.click(uniform(1080, 1100), uniform(70, 90))
            self.better_sleep((1, 1.425))

    @get_name
    def scan_fort(self):
        """
        Scan device screenshot to find gem node,          not 100% working need improvement
        :return: None
        """
        self.data = self.update_data()
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO,
                            format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
        self.restart_if_game_crashed()
        screen = self.adb.get_curr_device_screen_img()
        info_screen = array(screen)
        info_screen = cv2.cvtColor(info_screen, cv2.COLOR_BGR2RGB)
        info_screen = info_screen[470:700, 0:115]

        if self.adb.find_img(source=info_screen, target="gem_search_button", confidence=0.8) is not None:
            self.zoom_out_city()
            self.better_sleep((2, 3))
            screen = self.adb.get_curr_device_screen_img()

        if self.adb.find_img(source=info_screen, target="hammer", confidence=0.8) is not None:
            self.click(uniform(24, 91), uniform(625, 680))
            self.better_sleep((1.5, 2))
            self.zoom_out_city()
            self.better_sleep((2, 3))
            screen = self.adb.get_curr_device_screen_img()

        screen = array(screen)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

        if not self.data[self.sel]['schedules'][self.current_profile]["mauraudeurs_forts"]:
            for second_string in ["left", "mid", "right"]:
                for first_string in ["up", "mid", "down"]:
                    self.check_if_kill()
                    # f"{screen}fort_icon_day_{first_string}_{second_string}"
                    co = self.adb.find_img(source=screen, target=f"fort_icon_day_{first_string}_{second_string}", confidence=0.8)
                    co = self.validate_co(co)
                    if co is None:
                        co = self.adb.find_img(source=screen, target=f"fort_icon_night_{first_string}_{second_string}", confidence=0.8)
                        co = self.validate_co(co)
                    if co is not None:
                        print(
                            f'[ {current_time()} ] [ {self.name} ] Fort Found - x: {co[0]} y:{co[1]}')
                        logging.info(f"[{self.name}] Fort Found - x: {co[0]} y:{co[1]}")
                        self.set_text(f'[{current_time()}] Fort Found - x: {co[0]} y:{co[1]}')
                        self.check_if_kill()
                        if self.already_mining(co[0], co[1], screen):
                            self.print("Someone is already rallying it")
                            continue
                        self.click(co[0], co[1])
                        print(co[0], co[1])
                        logging.info(f"[{self.name}] x = {co[0]} y = {co[1]}")
                        self.set_text(f'[{current_time()}] x = {co[0]} y = {co[1]}')
                        x_click = co[0]
                        y_click = co[1]
                        self.better_sleep((2, 2.5))
                        self.check_if_kill()
                        self.check_resolve()
                        self.print("Scanning the fort..")
                        if self.find_cross():
                            self.print("Someone is already rallying it")
                            return self.adjusted_leave_city(x_click, y_click)
                        else:
                            self.check_if_kill()
                            bo1 = self.click_on_fort()
                            if not bo1:
                                self.print("Unable to click on the fort, leaving the fort !")
                                # return self.adjusted_leave_city(x_click, y_click)
                                return False
                            else:

                                self.better_sleep((1, 1.5))
                                co = self.adb.find_img(target="fort_rally_button2")
                                if co is not None:
                                    fivemins = (uniform(800, 925), uniform(188, 213))
                                    tenmins = (uniform(960, 1088), uniform(188, 213))
                                    thirtymins = (uniform(800, 925), uniform(238, 260))
                                    if self.data[str(self.sel)]['schedules'][self.current_profile].get(
                                            'rally_time') == 5:
                                        self.click(fivemins[0], fivemins[1])
                                    if self.data[str(self.sel)]['schedules'][self.current_profile].get(
                                            'rally_time') == 10:
                                        self.click(tenmins[0], tenmins[1])
                                    if self.data[str(self.sel)]['schedules'][self.current_profile].get(
                                            'rally_time') == 30:
                                        self.click(thirtymins[0], thirtymins[1])
                                    self.better_sleep((0.7, 1.2))
                                    self.click(co[0] + uniform(0, 147), co[1] + uniform(0, 54))
                                    self.better_sleep((1.1, 1.5))
                                    self.select_lineup_color(color='red')
                                    self.better_sleep((0.7, 1.2))
                                    if self.data[str(self.sel)]['schedules'][self.current_profile].get(
                                            'rally_type') == 'inf':
                                        # self.click(uniform(982,998),uniform(280,298))
                                        # self.better_sleep((0.7, 1.2))
                                        self.click(uniform(657, 680), uniform(96, 117))
                                        self.better_sleep((0.7, 1.2))
                                    if self.data[str(self.sel)]['schedules'][self.current_profile].get(
                                            'rally_type') == 'cav':
                                        # self.click(uniform(982,998),uniform(390,405))
                                        # self.better_sleep((0.7, 1.2))
                                        self.click(uniform(770, 795), uniform(96, 117))
                                        self.better_sleep((0.7, 1.2))
                                    if self.data[str(self.sel)]['schedules'][self.current_profile].get(
                                            'rally_type') == 'archers':
                                        # self.click(uniform(982,998),uniform(330,350))
                                        # self.better_sleep((0.7, 1.2))
                                        self.click(uniform(886, 906), uniform(96, 117))
                                        self.better_sleep((0.7, 1.2))
                                    self.click(uniform(1092, 1112), uniform(330, 350))
                                    self.better_sleep((0.5, 1))
                                    pil_image = self.adb.get_curr_device_screen_img()
                                    cv_image = array(pil_image)
                                    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
                                    x, y = self.adb.find_img(source=cv_image, target="troops_march_button", confidence=0.8)
                                    cropped_image = cv_image[y + 30:y + 50, x + 20:x + 110]
                                    # cv2.imwrite("timer.png", cropped_image)
                                    string = pytesseract.image_to_string(cropped_image,
                                                                         config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=1234567890:')
                                    string = string.replace("\n", "")
                                    # print(string)
                                    print(f"{string = }")
                                    datetime_object = datetime.strptime(string, '%H:%M:%S').time()
                                    print(datetime_object)
                                    print(f'[ {current_time()} ] [ {self.name} ] Starting the rally..')
                                    logging.info(f"[{self.name}] Starting the rally..")
                                    self.set_text(f'[{current_time()}] Starting the rally..')
                                    self.click(x, y)
                                    self.better_sleep((0.5, 1))
                                    self.go_city()
                                    self.better_sleep((0.5, 1))
                                    self.print(
                                        f"You selected {self.data[str(self.sel)]['schedules'][self.current_profile].get('rally_time')} minutes")
                                    self.print(f"Rally leader marching time is {datetime.strptime(string, '%H:%M:%S').strftime('%S')}")
                                    self.print("Bot is now paused until the rally leader come back..")
                                    time_to_wait1 = int(self.data[str(self.sel)]['schedules'][self.current_profile].get(
                                        'rally_time')) * 60 + int(
                                        datetime.strptime(string, '%H:%M:%S').strftime('%S'))
                                    time_to_wait2 = int(self.data[str(self.sel)]['schedules'][self.current_profile].get(
                                        'rally_time')) * 60 + int(
                                        datetime.strptime(string, '%H:%M:%S').strftime('%S')) * 2
                                    self.print(
                                        f"Bot will wait around {time_to_wait2 / 60} minutes to complete the task, the bot will now sleep for this time")
                                    for _ in range(time_to_wait2):
                                        self.script_pause()
                                        sleep(1)
                                    self.heal_troops()
                                    return True
        else:
            self.check_if_kill()
            co = self.adb.find_img(source=screen, target="maraudeurs_forts_icon", confidence=0.8)
            co = self.validate_co(co)
            if co is not None:
                self.print(f"Fort Found - x: {co[0]} y:{co[1]}")
                self.check_if_kill()
                if self.already_mining(co[0], co[1], screen):
                    self.print("Someone is already rallying it")
                self.click(co[0], co[1])
                print(co[0], co[1])
                logging.info(f"[{self.name}] x = {co[0]} y = {co[1]}")
                self.set_text(f'[{current_time()}] x = {co[0]} y = {co[1]}')
                x_click = co[0]
                y_click = co[1]
                self.better_sleep((2, 2.5))
                self.check_if_kill()
                print(
                    f'[ {current_time()} ] [ {self.name} ] Checking verification..')
                logging.info(f"[{self.name}] Checking verification..")
                self.set_text(f'[{current_time()}] Checking verification..')
                self.check_resolve()
                print(
                    f'[ {current_time()} ] [ {self.name} ] Scanning the fort..')
                logging.info(f"[{self.name}] Scanning the fort..")
                self.set_text(f'[{current_time()}] Scanning the fort..')
                if self.find_cross():
                    print(
                        f'[ {current_time()} ] [ {self.name} ] Someone is already rallying it..')
                    logging.info(f"[{self.name}] Someone is already rallying it..")
                    self.set_text(f'[{current_time()}] Someone is already rallying it..')
                    return self.adjusted_leave_city(x_click, y_click)
                else:
                    self.check_if_kill()
                    bo1 = self.click_on_fort()
                    if not bo1:
                        print(
                            f'[ {current_time()} ] [ {self.name} ] Unable to click on the fort, leaving the fort !')
                        logging.info(f"[{self.name}] Unable to click on the fort, leaving the fort !")
                        self.set_text(f'[{current_time()}] Unable to click on the fort, leaving the fort !')
                        # return self.adjusted_leave_city(x_click, y_click)
                        return False
                    else:

                        self.better_sleep((1, 1.5))
                        co = self.adb.find_img(target="fort_rally_button2")
                        if co is not None:
                            fivemins = (uniform(800, 925), uniform(188, 213))
                            tenmins = (uniform(960, 1088), uniform(188, 213))
                            thirtymins = (uniform(800, 925), uniform(238, 260))
                            if self.data[str(self.sel)]['schedules'][self.current_profile].get('rally_time') == 5:
                                self.click(fivemins[0], fivemins[1])
                            if self.data[str(self.sel)]['schedules'][self.current_profile].get('rally_time') == 10:
                                self.click(tenmins[0], tenmins[1])
                            if self.data[str(self.sel)]['schedules'][self.current_profile].get('rally_time') == 30:
                                self.click(thirtymins[0], thirtymins[1])
                            self.better_sleep((0.7, 1.2))
                            self.click(co[0] + uniform(0, 147), co[1] + uniform(0, 54))
                            self.better_sleep((1.1, 1.5))
                            self.select_lineup_color(color='red')
                            self.better_sleep((0.7, 1.2))
                            if self.data[str(self.sel)]['schedules'][self.current_profile].get('rally_type') == 'inf':
                                # self.click(uniform(982,998),uniform(280,298))
                                # self.better_sleep((0.7, 1.2))
                                self.click(uniform(657, 680), uniform(96, 117))
                                self.better_sleep((0.7, 1.2))
                            if self.data[str(self.sel)]['schedules'][self.current_profile].get('rally_type') == 'cav':
                                # self.click(uniform(982,998),uniform(390,405))
                                # self.better_sleep((0.7, 1.2))
                                self.click(uniform(770, 795), uniform(96, 117))
                                self.better_sleep((0.7, 1.2))
                            if self.data[str(self.sel)]['schedules'][self.current_profile].get(
                                    'rally_type') == 'archers':
                                # self.click(uniform(982,998),uniform(330,350))
                                # self.better_sleep((0.7, 1.2))
                                self.click(uniform(886, 906), uniform(96, 117))
                                self.better_sleep((0.7, 1.2))
                            self.click(uniform(1092, 1112), uniform(330, 350))
                            self.better_sleep((0.5, 1))
                            pil_image = self.adb.get_curr_device_screen_img()
                            cv_image = array(pil_image)
                            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
                            x, y = self.adb.find_img(source=cv_image, target="troops_march_button", confidence=0.8)
                            cropped_image = cv_image[y + 30:y + 50, x + 20:x + 110]
                            # cv2.imwrite("timer.png", cropped_image)
                            string = pytesseract.image_to_string(cropped_image,
                                                                 config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=1234567890:')
                            string = string.replace("\n", "")
                            # print(string)
                            print(f"{string = }")
                            datetime_object = datetime.strptime(string, '%H:%M:%S').time()
                            print(datetime_object)
                            self.print("Starting the rally..")
                            self.click(x, y)
                            self.better_sleep((0.5, 1))
                            self.go_city()
                            self.better_sleep((0.5, 1))
                            self.print("Bot is now paused until the rally leader come back..")
                            self.print(f'You selected {self.data[str(self.sel)]["schedules"][self.current_profile].get("rally_time")} minutes')
                            self.print(f"Rally leader marching time is {datetime.strptime(string, '%H:%M:%S').strftime('%S')}")
                            time_to_wait1 = int(self.data[str(self.sel)]['schedules'][self.current_profile].get(
                                'rally_time')) * 60 + int(
                                datetime.strptime(string, '%H:%M:%S').strftime('%S'))
                            time_to_wait2 = int(self.data[str(self.sel)]['schedules'][self.current_profile].get(
                                'rally_time')) * 60 + int(
                                datetime.strptime(string, '%H:%M:%S').strftime('%S')) * 2
                            self.print(
                                f"Bot will wait around {time_to_wait2 / 60} minutes to complete the task, the bot will now sleep for this time")
                            for _ in range(time_to_wait2):
                                self.script_pause()
                                sleep(1)
                            # return self.heal_troops()
                            return True

    @get_name
    def random_macro(self) -> None:
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
        try:
            with open('path.json', encoding="UTF-8") as config_file:
                path_json = json.load(config_file)
            for name in ["com.lilithgame.roc.gp.cfg", "com.rok.gp.vn.cfg", "com.lilithgame.rok.gpkr.cfg", "com.lilithgames.rok.gp.jp.cfg",
                         "com.lilithgames.rok.gpkr.cfg"]:
                path = path_json['bluestacks'][:-15] + "Engine\\UserData\\InputMapper\\UserFiles\\" + name
                if os.path.isfile(path):
                    break
            # path = path_json['bluestacks'][:-15] + "Engine\\UserData\\InputMapper\\UserFiles\\com.lilithgame.roc.gp.cfg"
            # if not os.path.isfile(path):
            #     path = path_json['bluestacks'][:-15] + "Engine\\UserData\\InputMapper\\UserFiles\\com.rok.gp.vn.cfg"
            #     if not os.path.isfile(path):
            #         path = path_json['bluestacks'][
            #                :-15] + "Engine\\UserData\\InputMapper\\UserFiles\\com.lilithgame.rok.gpkr.cfg"
            #         if not os.path.isfile(path):
            #             path = path_json['bluestacks'][
            #                    :-15] + "Engine\\UserData\\InputMapper\\UserFiles\\com.lilithgames.rok.gp.jp.cfg"
            path2 = path.replace("cfg", "json")
            # print(f"{path = }")
            # print(f"{path2 = }")
            shutil.copy(path, path2)
            # print("test")
            with open(path2, encoding="UTF-8") as config_file:
                path_json = json.load(config_file)
            for element in path_json['ControlSchemes']:
                if element["Name"] == "Custom":
                    # print(element["Name"])
                    for macro in element["GameControls"]:
                        # print(macro)
                        if macro["KeyOut"] == "F6":
                            # print("True")
                            x1 = randint(22, 30)
                            x2 = randint(22, 30)
                            y = randint(25, 30)
                            macro["X1"] = x1
                            macro["X2"] = x1
                            macro["Y1"] = y + 0.64
                            macro["Y2"] = y + 43.42
            with open(path2, 'w', encoding="UTF-8") as outfile:
                json.dump(path_json, outfile, ensure_ascii=False)
            shutil.copy(path2, path)

        except Exception as e:
            for _ in range(5):
                self.print("/!\ FIX IT !! /!\ ")
            print(
                f"[ {current_time()} ] [ {self.name} ] Wrong macro location, cannot randomise it.. Please import the file com.lilithgame.roc.gp.cfg \nIf you don't know how to do it please watch the video in the #tutorial\n{e}")
            self.print(
                "Wrong macro location, cannot randomise it.. Please import the file com.lilithgame.roc.gp.cfg \nIf you don't know how to do it please watch the video in the #tutorial")
            for _ in range(5):
                self.print("/!\ FIX IT !! /!\ ")

    @get_name
    def start_fort(self):
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
        self.random_macro()
        print(f'[ {current_time()} ] [ {self.name} ] Script starting !')
        self.set_text(
            f"[{current_time()}] Script starting !")
        logging.info(f"[{self.name}] Script starting !")
        if not self.enough_action_points():
            self.print("Bot detected you are low in action point, bot prefers to not start a rally !")
            return
        self.run_game()
        self.check_resolve()
        self.leave_city()
        # print("premier leave city")
        self.better_sleep((1.5, 2))
        self.zoom_out_city()
        self.better_sleep((1.5, 2))
        if self.scan_fort(): return
        randomization = self.go_to(self.data[str(self.sel)]['schedules'][self.current_profile].get('city_x', 500),
                                   self.data[str(self.sel)]['schedules'][self.current_profile].get('city_y', 500))
        self.check_if_kill()
        radius = (self.data[str(self.sel)]['schedules'][self.current_profile].get('rally_radius', 50) // 10)
        width = radius + 1
        height = radius + 1
        starting_time = time()
        time_to_beat = starting_time + (60 * 60)
        # print(f'starting_time : {datetime.fromtimestamp(starting_time).strftime("%H:%M:%S")} , time to beat : {datetime.fromtimestamp(time_to_beat).strftime("%H:%M:%S")} , {starting_time>time_to_beat = }')
        self.print(f"Bot will search a fort until : {datetime.fromtimestamp(time_to_beat).strftime('%H:%M:%S')}")
        while time_to_beat > time():
            self.run_game()
            self.print(
                f"time to beat : {datetime.fromtimestamp(time_to_beat).strftime('%H:%M:%S')}\nCurrent time : {current_time()}\nTime to beat > current time : {time_to_beat > time()}")
            pil_image = self.adb.get_curr_device_screen_img()
            cv_image = np.array(pil_image)
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            cropped_image = cv_image[0:100, :800]
            if self.adb.find_img(target="block_icon", source=cropped_image, confidence=0.90) is not None:
                return
            self.check_if_kill()
            if self.scan_fort(): return
            self.check_reconnect(cv_image)
            self.check_log_back()
            self.check_resolve(False)

            if randomization == 0:
                for y in range(width - 1):
                    self.check_if_kill()
                    for _ in range(width):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_fort, self.swipe_right) == True:
                            return
                        # self.better_sleep((0.125, 0.195))

                    if self.swipe_scan(self.scan_fort, self.swipe_down):
                        return
                    # self.better_sleep((0.525, 0.795))
                    if time_to_beat < time(): return
                    self.check_resolve(False)
                    self.check_if_kill()

                    for _ in range(width):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_fort, self.swipe_left):
                            return
                        # self.better_sleep((0.125, 0.195))
                    self.check_resolve(False)
                    if time_to_beat < time(): return

                    if y != (width - 2):
                        if self.swipe_scan(self.scan_fort, self.swipe_down):
                            return
                    # self.better_sleep((0.125, 0.195))

            if randomization == 2:
                for y in range(width - 1):
                    if time_to_beat < time(): return
                    self.check_if_kill()
                    for _ in range(width):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_fort, self.swipe_left):
                            return
                        # self.better_sleep((0.125, 0.195))
                    if self.swipe_scan(self.scan_fort, self.swipe_up):
                        return
                    # self.better_sleep((0.125, 0.195))
                    if time_to_beat < time(): return
                    self.check_resolve(False)
                    self.check_if_kill()

                    for _ in range(width):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_fort, self.swipe_right):
                            return
                        # self.better_sleep((0.125, 0.195))
                    self.check_resolve(False)
                    if y != (width - 2):
                        if self.swipe_scan(self.scan_fort, self.swipe_up):
                            return

            if randomization == 1:
                for y in range(height - 1):
                    if time_to_beat < time(): return
                    self.check_if_kill()

                    for _ in range(height):
                        if time_to_beat < time(): return

                        if self.swipe_scan(self.scan_fort, self.swipe_down):
                            return

                    self.check_resolve(False)
                    self.check_if_kill()
                    if time_to_beat < time(): return

                    if self.swipe_scan(self.scan_fort, self.swipe_left):
                        return
                    # self.better_sleep((0.525, 0.795))

                    for _ in range(height):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_fort, self.swipe_up):
                            return
                        # self.better_sleep((0.125, 0.195))

                    self.check_resolve(False)
                    self.check_if_kill()
                    if y != (height - 2):
                        if self.swipe_scan(self.scan_fort, self.swipe_left):
                            return
                    # self.better_sleep((0.125, 0.195))

            if randomization == 3:
                for y in range(height - 1):
                    if time_to_beat < time(): return
                    self.check_if_kill()

                    for _ in range(height):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_fort, self.swipe_up):
                            return
                        # self.better_sleep((0.125, 0.195))

                    if self.swipe_scan(self.scan_fort, self.swipe_right):
                        return
                    # self.better_sleep((0.125, 0.195))
                    if time_to_beat < time(): return
                    self.check_if_kill()
                    self.check_resolve(False)

                    for _ in range(height):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_fort, self.swipe_down):
                            return
                        # self.better_sleep((0.125, 0.195))
                    self.check_resolve(False)
                    if y != (height - 2):
                        if self.swipe_scan(self.scan_fort, self.swipe_right):
                            return
                    # self.better_sleep((0.125, 0.195))

            self.better_sleep((1.525, 2.795))
            # self.leave_city()
            # print("second leave cit")
            randomization = self.go_to(self.data[str(self.sel)]['schedules'][self.current_profile].get('city_x', 500),
                                       self.data[str(self.sel)]['schedules'][self.current_profile].get('city_y', 500),
                                       randomization)
            self.print(f"Current path n°{randomization}")
            self.better_sleep((0.525, 0.795))
            self.zoom_out_city()
            # self.better_sleep((0.525, 0.795))

    @get_name
    def leave_kd_buff(self, Source = None):

        co = self.adb.find_img(target="kingdom_buff", source=Source)
        if co is not None:
            self.click(uniform(70, 270), uniform(100, 542))
            self.better_sleep((1.8, 3))

    @get_name
    def gather_gem(self):
        """
        Gather gems
        """
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO,
                            format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
        self.random_macro()
        # print(f'[ {current_time()} ] [ {self.name} ] Script starting !')
        # logging.info(f"[{self.name}] Script starting !")
        self.run_game()
        self.check_resolve()
        self.leave_city()
        # print("premier leave city")
        self.better_sleep((1.5, 2))
        self.zoom_out_city()
        self.better_sleep((1.5, 2))
        self.scan_gem()
        self.better_sleep((0.125, 0.195))
        randomization = self.go_to(self.data[str(self.sel)]['schedules'][self.current_profile].get('city_x', 500),
                                   self.data[str(self.sel)]['schedules'][self.current_profile].get('city_y', 500))
        # print(f"{randomization = }")
        self.check_if_kill()
        radius = (self.data[str(self.sel)]['schedules'][self.current_profile].get('radius', 50) // 10)
        width = radius + 1
        height = radius + 1
        starting_time = time()
        time_restart = time()
        # print(self.data[str(self.sel)]['schedules'][self.current_profile].get('gather_gem_duration1'))
        if self.data[str(self.sel)]['schedules'][self.current_profile].get('gather_gem_duration1') > self.data[str(self.sel)]['schedules'][
            self.current_profile].get('gather_gem_duration2'):
            self.data[self.sel]['schedules'][self.current_profile]['gather_gem_duration1'], \
                self.data[self.sel]['schedules'][self.current_profile]['gather_gem_duration2'] = \
                self.data[self.sel]['schedules'][self.current_profile]['gather_gem_duration2'], \
                    self.data[self.sel]['schedules'][self.current_profile]['gather_gem_duration1']

        time_to_beat = starting_time + (
                randint(
                    self.data[str(self.sel)]['schedules'][self.current_profile].get('gather_gem_duration1'),
                    self.data[str(self.sel)]['schedules'][self.current_profile].get('gather_gem_duration2')
                ) * 60
        )
        # print(f'starting_time : {datetime.fromtimestamp(starting_time).strftime("%H:%M:%S")} , time to beat : {datetime.fromtimestamp(time_to_beat).strftime("%H:%M:%S")} , {starting_time>time_to_beat = }')
        self.print(f"Gathering gems till around : {datetime.fromtimestamp(time_to_beat).strftime('%H:%M:%S')}")
        while time_to_beat > time():
            self.run_game()
            # print(
            #     f'time to beat : {datetime.fromtimestamp(time_to_beat).strftime("%H:%M:%S")}\nCurrent time : {current_time()}\nTime to beat > current time : {time_to_beat > time()}')
            # logging.info(
            #     f"[{self.name}]time to beat : {datetime.fromtimestamp(time_to_beat).strftime('%H:%M:%S')}\nCurrent time : {current_time()}\nTime to beat > current time : {time_to_beat > time()}")
            # self.set_text(
            #     f"[{current_time()}] time to beat : {datetime.fromtimestamp(time_to_beat).strftime('%H:%M:%S')}\nCurrent time : {current_time()}\nTime to beat > current time : {time_to_beat > time()}")
            if self.data[str(self.sel)]['schedules'][self.current_profile].get("restart_game", True):
                random_time = uniform(4000, 5800)
                if time() > time_restart + random_time:
                    self.leave_game(force = True)
                    self.print(f"Game is stopped, game starting in about 7sec")
                    self.better_sleep((5, 10))
                    self.run_game()
                    self.print("Function is going to restart")
                    self.check_resolve()
                    self.leave_city()
                    # print("premier leave city")
                    self.better_sleep((1.5, 2))
                    self.zoom_out_city()
                    self.better_sleep((1.5, 2))
                    self.scan_gem()
                    self.better_sleep((0.125, 0.195))
                    randomization = self.go_to(
                        self.data[str(self.sel)]['schedules'][self.current_profile].get('city_x', 500),
                        self.data[str(self.sel)]['schedules'][self.current_profile].get('city_y', 500))
                    time_restart = time()

            pil_image = self.adb.get_curr_device_screen_img()
            cv_image = np.array(pil_image)
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            cropped_image = cv_image[0:100, 0:800]
            if self.adb.find_img(target="block_icon", source=cropped_image, confidence=0.90) is not None:
                self.print("Block icon detected. Cancelling the function !")
                return
            self.check_if_kill()
            self.scan_gem()
            self.check_reconnect(cv_image)
            self.check_log_back()
            self.check_resolve(False)
            self.leave_kd_buff()

            # print("test")
            if randomization == 0:
                for y in range(width - 1):
                    self.check_if_kill()
                    for i in range(width):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_gem, self.swipe_right) == False:
                            return
                        # self.better_sleep((0.125, 0.195))

                    if self.swipe_scan(self.scan_gem, self.swipe_down) == False:
                        return
                    # self.better_sleep((0.525, 0.795))
                    if time_to_beat < time(): return
                    self.leave_kd_buff()
                    self.check_resolve(False)
                    self.check_if_kill()

                    for i in range(width):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_gem, self.swipe_left) == False:
                            return
                        # self.better_sleep((0.125, 0.195))
                    self.check_resolve(False)
                    self.leave_kd_buff()
                    if time_to_beat < time(): return

                    if y != (width - 2):
                        if self.swipe_scan(self.scan_gem, self.swipe_down) == False:
                            return
                    # self.better_sleep((0.125, 0.195))

            if randomization == 2:
                for y in range(width - 1):
                    if time_to_beat < time(): return
                    self.check_if_kill()
                    for i in range(width):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_gem, self.swipe_left) == False:
                            return
                        # self.better_sleep((0.125, 0.195))
                    if self.swipe_scan(self.scan_gem, self.swipe_up) == False:
                        return
                    # self.better_sleep((0.125, 0.195))
                    if time_to_beat < time(): return
                    self.check_resolve(False)
                    self.leave_kd_buff()
                    self.check_if_kill()

                    for i in range(width):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_gem, self.swipe_right) == False:
                            return
                        # self.better_sleep((0.125, 0.195))
                    self.check_resolve(False)
                    self.leave_kd_buff()
                    if y != (width - 2):
                        if self.swipe_scan(self.scan_gem, self.swipe_up) == False:
                            return

            if randomization == 1:
                for y in range(height - 1):
                    if time_to_beat < time(): return
                    self.check_if_kill()

                    for i in range(height):
                        if time_to_beat < time(): return

                        if self.swipe_scan(self.scan_gem, self.swipe_down) == False:
                            return

                    self.check_resolve(False)
                    self.leave_kd_buff()
                    self.check_if_kill()
                    if time_to_beat < time(): return

                    if self.swipe_scan(self.scan_gem, self.swipe_left) == False:
                        return
                    # self.better_sleep((0.525, 0.795))

                    for i in range(height):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_gem, self.swipe_up) == False:
                            return
                        # self.better_sleep((0.125, 0.195))

                    self.check_resolve(False)
                    self.leave_kd_buff()
                    self.check_if_kill()
                    if y != (height - 2):
                        if self.swipe_scan(self.scan_gem, self.swipe_left) == False:
                            return
                    # self.better_sleep((0.125, 0.195))

            if randomization == 3:
                for y in range(height - 1):
                    if time_to_beat < time(): return
                    self.check_if_kill()

                    for i in range(height):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_gem, self.swipe_up) == False:
                            return
                        # self.better_sleep((0.125, 0.195))

                    if self.swipe_scan(self.scan_gem, self.swipe_right) == False:
                        return
                    # self.better_sleep((0.125, 0.195))
                    if time_to_beat < time(): return
                    self.check_if_kill()
                    self.check_resolve(False)
                    self.leave_kd_buff()

                    for i in range(height):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_gem, self.swipe_down) == False:
                            return
                        # self.better_sleep((0.125, 0.195))
                    self.check_resolve(False)
                    self.leave_kd_buff()
                    if y != (height - 2):
                        if self.swipe_scan(self.scan_gem, self.swipe_right) == False:
                            return
                    # self.better_sleep((0.125, 0.195))

            self.better_sleep((1.525, 2.795))
            # self.leave_city()
            # print("second leave cit")
            randomization = self.go_to(self.data[str(self.sel)]['schedules'][self.current_profile].get('city_x', 500),
                                       self.data[str(self.sel)]['schedules'][self.current_profile].get('city_y', 500),
                                       randomization)
            self.print(f"Current path n°{randomization}")
            self.better_sleep((0.525, 0.795))
            self.zoom_out_city()
            # self.better_sleep((0.525, 0.795))
        self.print("Gathering gem time elapsed !")

    # def gather_rss1(self, resources=None, resolved=False):
    #     if not resolved:
    #         resolved = self.check_resolve()
    #     if resources == "Done":
    #         return "Done"
    #     if resources is None:
    #         resources = self.data[str(self.sel)]['schedules'][self.current_profile].get("First"]
    #     nbminus = 0
    #     nbsearch = 0
    #     clickedMinus = False
    #     self.leave_city()
    #     self.better_sleep((2, 3.5))
    #     ###Vérifie si y'a une troupe
    #     while self.free_troop():
    #         self.click_loop()
    #         x, y = self.change_x_y_by_resource_type(resources)
    #         self.better_sleep((1.325, 1.795))
    #         self.click(x, y)
    #         self.better_sleep((1.325, 1.795))
    #         ###Click sur la bonne resources + le bon niveau de resources
    #         self.click_search_node(resources)
    #         self.better_sleep((1.325, 1.795))
    #         self.set_search_level(self.data[str(self.sel)]['schedules'][self.current_profile].get(self.get_key_by_rss(resources) + "_level"])
    #
    #         while not self.minable():
    #             print(f'[ {current_time()} ] [ {self.data[str(self.sel)]['schedules'][self.current_profile].get("name","Name not found")} ] Not minable')
    #             self.better_sleep((1.325, 1.795))
    #             if not self.node_found():
    #                 print(f'[ {current_time()} ] [ {self.data[str(self.sel)]['schedules'][self.current_profile].get("name","Name not found")} ] Node not found')
    #                 if nbminus == 0:
    #                     print(f'[ {current_time()} ] [ {self.data[str(self.sel)]['schedules'][self.current_profile].get("name","Name not found")} ] nbminus == 0')
    #                     self.click(uniform((1280 // 2) - 20, (1280 // 2) + 20),
    #                                    uniform((720 // 3) - 20, (720 // 3) + 20))
    #                     self.better_sleep((0.025, 0.295))
    #                     nbminus += 1
    #                     # self.leave_city()
    #                     # self.better_sleep((1,1.5))
    #                     self.click_loop()
    #                     self.better_sleep((1.325, 1.795))
    #                     self.click_minus()
    #                     self.better_sleep((1.325, 1.795))
    #                     clickedMinus = True
    #                     self.click_search_node(resources)
    #                     self.better_sleep((1.325, 1.795))
    #
    #                 else:
    #                     print(f'[ {current_time()} ] [ {self.data[str(self.sel)]['schedules'][self.current_profile].get("name","Name not found")} ] nbminus != 0')
    #                     nbminus = 0
    #                     self.click(uniform((1280 // 2) - 20, (1280 // 2) + 20),
    #                                    uniform((720 // 3) - 20, (720 // 3) + 20))
    #                     self.better_sleep((0.025, 0.295))
    #                     self.click_loop()
    #                     self.better_sleep((0.325, 0.695))
    #                     self.click_plus()
    #                     self.better_sleep((0.725, 0.995))
    #                     self.click(1280 // 2, 720 // 3)
    #                     self.better_sleep((0.725, 0.995))
    #                     change_rss = self.change_resource_type(resources)
    #                     return self.gather_rss(change_rss, resolved)
    #
    #             if self.find_cross():
    #                 print(f'[ {current_time()} ] [ {self.data[str(self.sel)]['schedules'][self.current_profile].get("name","Name not found")} ] Node occupied')
    #                 if nbsearch == 2:
    #                     print(f'[ {current_time()} ] [ {self.data[str(self.sel)]['schedules'][self.current_profile].get("name","Name not found")} ] nbsearch == 2')
    #                     if nbminus == 0:
    #                         print(f'[ {current_time()} ] [ {self.data[str(self.sel)]['schedules'][self.current_profile].get("name","Name not found")} ] nnbminus= 0')
    #                         nbminus += 1
    #                         nbsearch = 0
    #                         self.click_loop()
    #                         self.better_sleep((1.325, 1.795))
    #                         self.click_minus()
    #                         self.better_sleep((1.325, 1.795))
    #                         clickedMinus = True
    #                         self.click_search_node(resources)
    #                     else:
    #                         print(f'[ {current_time()} ] [ {self.data[str(self.sel)]['schedules'][self.current_profile].get("name","Name not found")} ] nbminus !=0')
    #                         nbminus = 0
    #                         nbsearch = 0
    #                         if self.node_found():
    #                             self.click_loop()
    #                             self.better_sleep((0.425, 0.795))
    #                         self.click_plus()
    #                         self.better_sleep((0.425, 0.795))
    #                         self.click(1280 // 2, 720 // 3)
    #                         self.better_sleep((0.425, 0.795))
    #                         change_rss = self.change_resource_type(resources)
    #                         return self.gather_rss(change_rss, resolved)
    #                 else:
    #                     print(f'[ {current_time()} ] [ {self.data[str(self.sel)]['schedules'][self.current_profile].get("name","Name not found")} ] nbsearch != 2')
    #                     nbsearch += 1
    #                     self.better_sleep((0.5, 0.957))
    #                     self.click_loop()
    #                     self.better_sleep((0.425, 0.795))
    #                     x, y = self.change_x_y_by_resource_type(resources)
    #                     self.click(x, y)
    #                     self.better_sleep((0.725, 1.195))
    #                     self.click_search_node(resources)
    #                     self.better_sleep((0.625, 0.995))
    #         print(f'[ {current_time()} ] [ {self.data[str(self.sel)]['schedules'][self.current_profile].get("name","Name not found")} ] Clicking on node')
    #         if self.click_on_node():
    #             if not self.send_troop():
    #                 self.click(uniform(200, 900), uniform(300, 500))
    #                 self.better_sleep((2.325, 4.795))
    #                 return
    #
    #         # try:
    #         #     if self.free_troop():
    #         #         self.send_troop()
    #         #     else:
    #         #         x, y = uniform(22, 90), uniform(625, 675)
    #         #         self.click(x, y)
    #         #         print("DOne")
    #         #         return "Done"
    #         # except :
    #         #     print("Failed")
    #         #     return self.gather_rss(resources)
    #         self.better_sleep((1, 1.895))
    #         if not resolved:
    #             resolved = self.check_resolve()
    #     if clickedMinus:
    #         self.click_loop()
    #         self.better_sleep((1.325, 1.795))
    #         self.click_plus()
    #         self.better_sleep((1.325, 1.795))
    #         self.click(1280 // 2 + uniform(-10, 10), 720 // 3 + uniform(-10, 10))
    #
    #     x, y = uniform(22, 90), uniform(625, 675)
    #     self.click(x, y)
    #     return "Done"

    # def gather_rss(self, node_type=None, resolved=False, level_decrease=0):
    #     logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO,
    #                         format="%(asctime)s %(message)s",
    #                         datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
    #     if not resolved:
    #         resolved = self.check_resolve()
    #     if node_type is None:
    #         node_type = "First"
    #     if node_type == "Done":
    #         print(
    #             f'[ {current_time()} ] [ {self.name} ] No node matched the requirements, now reducing the node level..')
    #         logging.info(f"[{self.name}] No node matched the requirements, now reducing the node level..")
    #         self.set_text(f"[{current_time()}] No nore matched the requirements, now reducing the node level..")
    #         print(f"{level_decrease = }, {node_type = }")
    #         return self.gather_rss(node_type="First", resolved=resolved, level_decrease=level_decrease - 2)
    #     nbsearch = 0
    #     clickedMinus = False
    #     self.check_reconnect()
    #     self.leave_city_simple()
    #     self.better_sleep((2, 3.5))
    #     # Vérifie si y'a une troupe
    #     level_verified = False
    #     while self.free_troop():
    #         self.check_log_back()
    #         self.check_reconnect()
    #         self.click_loop()
    #         self.better_sleep((1.325, 1.795))
    #         x, y = self.change_x_y_by_resource_type(node_type)
    #         # self.better_sleep((1.325, 1.795))
    #         self.click(x, y)
    #         self.better_sleep((1.325, 1.795))
    #         # Click sur la bonne resources + le bon niveau de resources
    #         if self.data.get(self.sel).get('schedules').get(self.current_profile).get(
    #                 f"{node_type}_level") - level_decrease <= 0:
    #             return
    #         if level_verified is False:
    #             self.set_search_level(self.data.get(self.sel).get('schedules').get(self.current_profile).get(
    #                 f"{node_type}_level") - level_decrease)
    #             self.better_sleep((0.325, 0.795))
    #             level_verified = True
    #         print(f'[ {current_time()} ] [ {self.name} ] Looking for : {node_type}')
    #         logging.info(f"[{self.name}] Looking for : {node_type}")
    #         self.set_text(f"[{current_time()}] Looking for : {node_type}")
    #
    #         self.click_search_node(node_type)
    #         # self.better_sleep((1.325, 1.795))
    #         self.better_sleep((3, 6))
    #         # Tant que la node trouvée n'est pas minable
    #         while not self.minable():
    #             self.check_reconnect()
    #             print(f'[ {current_time()} ] [ {self.name} ] Not minable')
    #             logging.info(f"[{self.name}]  Node is not minable")
    #             self.set_text(f"[{current_time()}] Node is not minable")
    #             self.better_sleep((1.325, 1.795))
    #             # Si y'a plus de node on return le prochain rss
    #             if self.node_found() is False:
    #                 print(f'[ {current_time()} ] [ {self.name} ] Node not found')
    #                 logging.info(f"[{self.name}]  Node not found")
    #                 self.set_text(f"[{current_time()}] Node not found")
    #                 self.click(uniform((1280 // 2) - 20, (1280 // 2) + 20),
    #                            uniform((720 // 3) - 20, (720 // 3) + 20))
    #                 self.better_sleep((0.125, 0.495))
    #                 print(
    #                     f'[ {current_time()} ] [ {self.name} ] No node matched the requirements, switching to the next type..')
    #                 logging.info(f"[{self.name}] No node matched the requirements, switching to the next type..")
    #                 self.set_text(f"[{current_time()}] No node matched the requirements, switching to the next type..")
    #                 node_type = change_resource_type(node_type)
    #                 print(f"{level_decrease = }, {node_type = }")
    #                 return self.gather_rss(node_type, resolved, level_decrease)
    #
    #             # Si y'a une cross
    #             self.better_sleep((1, 2.5))
    #             if self.find_cross() is True:
    #                 # print(f'[ {current_time()} ] [ {self.name} ] Node occupied')
    #                 # logging.info(f"[{self.name}] Node occupied")
    #                 # self.set_text(f"[{current_time()}] Node occupied")
    #                 # Au bout de deux search ca va au charbon avec le prochain rss
    #                 if nbsearch == 2:
    #                     print(
    #                         f'[ {current_time()} ] [ {self.data.get(self.sel).get("name", "Name not found")} ] nbsearch == 2')
    #                     self.click(uniform((1280 // 2) - 20, (1280 // 2) + 20),
    #                                uniform((720 // 3) - 20, (720 // 3) + 20))
    #                     self.better_sleep((0.025, 0.295))
    #
    #                     print(
    #                         f'[ {current_time()} ] [ {self.name} ] No node matched the requirements, switching to the next type..')
    #                     logging.info(f"[{self.name}] No node matched the requirements, switching to the next type..")
    #                     self.set_text(
    #                         f"[{current_time()}] No node matched the requirements, switching to the next type..")
    #
    #                     node_type = change_resource_type(node_type)
    #                     print(f"{level_decrease = }, {node_type = }")
    #                     return self.gather_rss(node_type, resolved, level_decrease)
    #                 else:
    #                     print(
    #                         f'[ {current_time()} ] [ {self.data.get(self.sel).get("name", "Name not found")} ] nbsearch != 2')
    #                     logging.info(f"[{self.name}] nbsearch != 2")
    #                     self.set_text(f"[{current_time()}] Looking for a new node..")
    #                     nbsearch += 1
    #                     self.better_sleep((0.5, 0.957))
    #                     self.click_loop()
    #                     self.better_sleep((0.425, 0.795))
    #                     # x, y = self.change_x_y_by_resource_type(resources)
    #                     # self.click(x, y)
    #                     # self.better_sleep((0.725, 1.195))
    #                     # self.set_search_level(self.data.get(self.sel).get(self.get_key_by_rss(resources) + "_level"])
    #                     # self.better_sleep((1.325, 1.795))
    #                     self.click_search_node(node_type)
    #                     self.better_sleep((1.325, 1.795))
    #         self.check_reconnect()
    #         # print(f'[ {current_time()} ] [ {self.name} ] Clicking on node')
    #         # logging.info(f"[{self.name}]  Clicking on node")
    #         # self.set_text(f"[{current_time()}] Clicking on node")
    #         if self.click_on_node() and not self.send_troop():
    #             self.click(x=uniform(200, 900), y=uniform(300, 500))
    #             self.better_sleep((2.325, 4.795))
    #             return "Done"
    #
    #         self.better_sleep((1, 1.895))
    #         resolved = self.check_resolve()
    #     self.click(x=uniform(22, 90), y=uniform(625, 675))
    #     return "Done"
    @get_name
    def gather_rss2(self, node_type=None, resolved=False, level_decrease=0):
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO,
                            format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
        if not resolved:
            resolved = self.check_resolve()
        if node_type is None:
            node_type = "First"
        # if node_type == "Done":
        #     print(f'[ {current_time()} ] [ {self.name} ] No node matched the requirements, now reducing the node level..')
        #     logging.info(f"[{self.name}] No node matched the requirements, now reducing the node level..")
        #     self.set_text(f"[{current_time()}] No nore matched the requirements, now reducing the node level..")
        #     print(f"{level_decrease = }, {node_type = }")
        #     return self.gather_rss(node_type="First", resolved=resolved, level_decrease=level_decrease - 2)
        if node_type == "Done":
            return
        nbsearch = 0
        self.check_reconnect()
        self.leave_city_simple()
        self.better_sleep((2, 3.5))
        # Vérifie si y'a une troupe
        level_verified = False
        while self.free_troop():
            self.check_log_back()
            self.check_reconnect()
            self.click_loop()
            self.better_sleep((1.325, 2.195))
            x, y = self.change_x_y_by_resource_type(node_type)
            # self.better_sleep((1.325, 1.795))
            self.click(x, y)
            self.better_sleep((1.325, 1.795))

            # Click sur la bonne resources + le bon niveau de resources
            if self.data.get(self.sel).get('schedules').get(self.current_profile).get(
                    f"{node_type}_level") - level_decrease <= 0:
                node_type = change_resource_type(node_type)
                print(f"{level_decrease = }, {node_type = }")
                return self.gather_rss2(node_type, resolved, level_decrease)

            if level_verified is False:
                self.set_search_level(self.data.get(self.sel).get('schedules').get(self.current_profile).get(
                    f"{node_type}_level") - level_decrease)
                self.better_sleep((0.325, 0.795))
                level_verified = True
            print(f"{node_type =}")
            self.click_search_node(node_type)
            self.better_sleep((4, 6))
            # self.better_sleep((1.325, 1.795))
            # Tant que la node trouvée n'est pas minable

            while not self.minable():
                self.check_reconnect()
                self.better_sleep((1.325, 1.795))
                # Si y'a plus de node on return le prochain rss

                if self.node_found() is False:
                    # print(f'[ {current_time()} ] [ {self.name} ] Node not found')
                    # logging.info(f"[{self.name}] Node not found")
                    # self.set_text(f"[{current_time()}] Node not found")
                    # node_type = self.change_resource_type(node_type)
                    self.click(uniform((1280 // 2) - 20, (1280 // 2) + 20), uniform((720 // 3) - 20, (720 // 3) + 20))
                    self.better_sleep((0.125, 0.495))
                    self.print("No node matched the requirements, reducing the level..")
                    self.print(f"{level_decrease+1 = }, {node_type = }")
                    return self.gather_rss2(node_type, resolved, level_decrease + 1)

                # Si y'a une cross
                self.better_sleep((2, 3.5))
                if self.find_cross() is True:
                    # print(f'[ {current_time()} ] [ {self.name} ] Node occupied')
                    # logging.info(f"[{self.name}] Node occupied")
                    # self.set_text(f"[{current_time()}] Node occupied")
                    # Au bout de deux search ca va au charbon avec le prochain rss
                    if nbsearch == 2:
                        self.print("nbsearch == 2")
                        self.click(uniform((1280 // 2) - 20, (1280 // 2) + 20),
                                   uniform((720 // 3) - 20, (720 // 3) + 20))
                        self.better_sleep((0.025, 0.295))

                        self.print("No node matched the requirements, reducing the level..")
                        self.print(f"{level_decrease+1 = }, {node_type = }")
                        return self.gather_rss2(node_type, resolved, level_decrease + 1)
                    else:
                        self.print("nbsearch != 2")
                        self.print("Looking for a new node")
                        nbsearch += 1
                        self.better_sleep((0.5, 0.957))
                        self.click_loop()
                        self.better_sleep((0.425, 0.795))
                        # x, y = self.change_x_y_by_resource_type(resources)
                        # self.click(x, y)
                        # self.better_sleep((0.725, 1.195))
                        # self.set_search_level(self.data.get(self.sel).get(self.get_key_by_rss(resources) + "_level"])
                        # self.better_sleep((1.325, 1.795))
                        self.click_search_node(node_type)
                        self.better_sleep((3, 5))
                self.better_sleep((2, 3.5))
            self.check_reconnect()
            if self.click_on_node() and not self.send_troop():
                self.click(x=uniform(200, 900), y=uniform(300, 500))
                self.better_sleep((2.325, 4.795))
                return "Done"
            self.better_sleep((1, 1.895))
            resolved = self.check_resolve()
            node_type = self.change_resource_type2(node_type)
        self.click(x=uniform(22, 90), y=uniform(625, 675))
        return "Done"

    @get_name
    def leave_game(self, force = False) -> None:
        """
        Send adb signal to leave application
        """
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO,
                            format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
        self.print(f"Leaving the game..")

        if not force:
            self.adb.home_button()
        else:
            self.adb.get_device().shell("am force-stop com.lilithgame.roc.gp")
            self.adb.get_device().shell("am force-stop com.rok.gp.vn")
            self.adb.get_device().shell("am force-stop com.lilithgame.rok.gpkr")
            self.adb.get_device().shell("am force-stop com.lilithgames.rok.gpkr")


    @get_name
    def kill_game(self) -> None:
        self.adb.get_device().shell("am force-stop com.lilithgame.roc.gp")
        self.adb.get_device().shell("am force-stop com.rok.gp.vn")
        self.adb.get_device().shell("am force-stop com.lilithgame.rok.gpkr")
        self.adb.get_device().shell("am force-stop com.lilithgames.rok.gpkr")

    @get_name
    def enough_action_points(self) -> bool:
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = np.array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv_image)
        print(img.getpixel((33, 73)))
        if (
                (10 < img.getpixel((33, 73))[0] < 20) and
                (225 < img.getpixel((33, 73))[1] < 240) and
                (120 < img.getpixel((33, 73))[2] < 135)
        ) \
                or \
                (
                        (10 < img.getpixel((33, 73))[2] < 20) and
                        (225 < img.getpixel((33, 73))[1] < 240) and
                        (120 < img.getpixel((33, 73))[0] < 135)
                ) \
                or \
                (
                        img.getpixel((33, 73)) == (0, 255, 142)
                ):

            return True
        else:
            return False

    def join_rally(self):
        co = self.adb.find_img(target='menu_opened')
        if co is None:
            x, y = uniform(1200, 1250), uniform(650, 690)
            self.click(x, y)
            self.better_sleep((1.725, 1.995))
        # Open alliance menu
        x, y = uniform(1010, 1050), uniform(650, 690)
        self.click(x, y)
        self.better_sleep((1.725, 2.295))
        x, y = uniform(597, 647), uniform(378, 436)
        self.click(x, y)
        self.better_sleep((1.725, 2.295))
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = np.array(pil_image)
        cropped_image = cv_image[110:130, 178:247]
        radius = pytesseract.image_to_string(cropped_image,
                                             config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=12345670KM')
        if "KM" not in radius:
            print(f'[ {current_time()} ] [ {self.name} ] Cannot join a fort, no fort started')
            self.click(uniform(1104, 1127), uniform(33, 54))
            return self.better_sleep((1.725, 2.295))

    @get_name
    def set_search_level(self, level: int = 10) -> None:
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO,
                            format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = np.array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        co = self.adb.find_img(source=cv_image, target="button_level", confidence=0.8)
        if co is None:
            print(f'[ {current_time()} ] [ {self.name} ] Cannot find the button_level')
            logging.info('Cannot find the button_level')
            # self.set_text(f"[{current_time()}] Cannot find the level button")
            self.click_loop()
            self.better_sleep((1, 1.2))
        else:
            # x,y = uniform(225,285) , uniform(607,667)
            # self.click(x,y)
            self.better_sleep((1, 1.3))
            cv_image = cv_image[co[1] - 30:co[1], co[0] - 40:co[0] + 40]
            # cv2.imwrite("level.png", cv_image)
            string = pytesseract.image_to_string(cv_image,
                                                 config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=level:1234567890')
            string = string.replace("\n", "")
            string = string.split(":")
            print(
                f'[ {current_time()} ] [ {self.name} ] Current level : {string[1]}')
            logging.info(f"[{self.name}] Current level : {string[1]}")
            # self.set_text(f"[{current_time()}] Current level : {string[1]}")
            level_to_go = level - int(string[1])
            if level_to_go > 0:
                word = "Increasing"
                x, y = self.adb.find_img(target='plus_button')
            else:
                word = "Decreasing"
                x, y = self.adb.find_img(target='minus_button')
            print(f'[ {current_time()} ] [ {self.name} ] {word} the level by : {abs(level_to_go)}')
            logging.info(f"[{self.name}] {word} the level by : {abs(level_to_go)}")
            # self.set_text(f"[{current_time()}] {word} the level by : {abs(level_to_go)}")
            for _ in range(abs(level_to_go)):
                x2 = x + uniform(0, 30)
                y2 = y + uniform(0, 27)
                self.click(x2, y2)
                self.better_sleep((0.115, 0.300))
            return

    @get_name
    def check_ap_box(self) -> bool:
        print(f'[ {current_time()} ] [ {self.name} ] Check if AP pop-op box is detected')
        if self.adb.find_img(target="ap_bottle"):
            co = self.adb.find_img(target="daily_ap_claim")
            if co is None:
                co = self.adb.find_img(target="close_window")
                self.click(co[0], co[1])
                self.better_sleep((1.325, 1.795))
            else:
                x, y = co[0] + uniform(0, 30), co[1] + uniform(0, 20)
                self.click(x, y)
            self.better_sleep((1.325, 1.795))
            co = self.adb.find_img(target="close_window")
            if co is not None:
                self.click(co[0], co[1])
                self.better_sleep((1.325, 1.795))
            print(f'[ {current_time()} ] [ {self.name} ] Detected')
            return True
        print(f'[ {current_time()} ] [ {self.name} ] Not detected')
        return False

    @get_name
    def deploy_hunter(self):
        # top_left = (415,202)
        # top_right = (840,202)
        # bottom_left =(415,530)
        # top_left = (840,530)
        # list = []
        full_area = [(i, y) for i in range(420, 840, 5) for y in range(200, 530, 5) if not (795 > i > 490 and 210 < y < 490)]
        # forbidden_area = [(i, y) for i in range(490, 795,5) for y in range(230, 490,5)]
        # for element in forbidden_area:
        #     try:
        #         full_area.remove(element)
        #     except:
        #         pass
        # print("done")

        full_sent = False
        hunters = 0
        while not full_sent:
            co = choice(full_area)
            print("done", co)
            self.swipe_arg(co[0], co[1], co[0], co[1], randint(2500, 3475))
            self.better_sleep((1.325, 1.795))
            co = self.adb.find_img(target="deploy_march_button")
            if co is not None:
                self.click(co[0] + uniform(0, 140), co[1] + uniform(0, 4))
                self.better_sleep((1.325, 1.795))
                if self.adb.find_img(target="new_troops_button"):
                    self.send_new_troop(color='red')
                    hunters += 1
                else:
                    self.click(uniform(150, 500), uniform(150, 500))
                    full_sent = True
                self.better_sleep((1.325, 1.795))
        return hunters

    @get_name
    def hunt_barbarians(self):
        wanted_level = self.data.get(self.sel).get('schedules').get(self.current_profile).get("barbarians_level", 10)
        hunter_selection = False
        self.leave_city()
        self.better_sleep((1, 1.3))
        nb_hunter = self.deploy_hunter()
        if nb_hunter == 0:
            return
        while self.enough_action_points():
            self.better_sleep((1.5, 3))

            self.click_loop()  # Clicking on the loop
            self.better_sleep((1, 2))
            x, y = uniform(225, 285), uniform(607, 667)

            self.click(x, y)  # Selecting the barbarian section
            self.better_sleep((1, 1.3))
            self.set_search_level(wanted_level)  # Setting the barbarian level to the desired level

            x, y = uniform(200, 330), uniform(466, 506)
            self.click(x, y)  # Searching the barbarian
            self.better_sleep((1, 2))

            reduced_level = wanted_level
            while self.adb.find_img(target="search_button") is not None:
                reduced_level = reduced_level - 1
                self.set_search_level(reduced_level)

                x, y = uniform(200, 330), uniform(466, 506)
                self.click(x, y)  # Searching the barbarian

                self.better_sleep((1, 2))
            wanted_level = reduced_level
            self.click(1280 // 2 + uniform(-10, 10), 720 // 2 + uniform(-10, 10))  # Selecting the barbarian
            self.better_sleep((1, 1.4))
            button_attack = self.adb.find_img(target="attack_button")
            if button_attack is None:
                continue  # Skipping all the code bellow to re-execute the barbarian search
            self.click(button_attack[0] + uniform(0, 170), button_attack[1] + uniform(0, 40))
            self.better_sleep((1.5, 2))

            if not hunter_selection:
                print(f'[ {current_time()} ] [ {self.name} ] Selecting the whole troops from scratch')
                self.better_sleep((2, 3))
                x, y = uniform(1163, 1180), uniform(670, 685)
                print(f'[ {current_time()} ] [ {self.name} ] {x} {y}')
                self.click(x, y)
                self.better_sleep((2.2, 3.5))
                tab = self.adb.find_multiple_img("selected_icon")
                tab = tab[nb_hunter:-1]
                for element in tab:
                    x, y = element[0] + uniform(0, 5), element[1] + uniform(0, 5)
                    self.click(x, y)
                    self.better_sleep((0.3, 0.5))
                hunter_selection = True
                self.click(uniform(1163, 1183), uniform(665, 685))
                self.better_sleep((1.2, 1.5))

            print(f'[ {current_time()} ] [ {self.name} ] Selecting the whole troops')
            self.better_sleep((2, 3))
            self.click(uniform(1163, 1183), uniform(665, 685))
            self.better_sleep((1.2, 1.5))

            self.click(uniform(940, 1075), uniform(640, 670))
            self.better_sleep((1.2, 1.5))
            print(f'[ {current_time()} ] [ {self.name} ] Check if AP pop-op box is detected')
            if self.check_ap_box():
                print(f'[ {current_time()} ] [ {self.name} ] Pop-up found, recalling troops')
                break

            self.check_resolve()
            self.wait_until_kill()
        self.check_ap_box()
        self.recall(nb_troop=nb_hunter)

    @get_name
    def wait_until_kill(self):
        self.print(f"[ {current_time()} ] [ {self.name} ] Waiting for the troops to kill the barbarian..")
        while self.adb.find_img(target="troop_idle") is None or self.adb.find_img(target="troop_walking") is not None:
            self.script_pause()
            self.check_log_back()
            self.check_reconnect()
            self.check_if_kill()
            self.check_resolve()
            self.better_sleep((3, 5))
            print(f"[ {current_time()} ] [ {self.name} ] Waiting for the troops to kill the barbarian..")


    @get_name
    def get_first_character(self) -> tuple[float, float]:
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO,
                            format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
        self.print("Switching Character")
        self.set_status(f"Switching Character")
        x, y = uniform(15, 80), uniform(10, 60)
        self.click(x, y)
        self.better_sleep((1.925, 2.795))
        x, y = uniform(950, 1015), uniform(510, 560)
        self.click(x, y)
        self.better_sleep((1.925, 2.795))
        x, y = uniform(315, 380), uniform(330, 400)
        self.click(x, y)
        self.better_sleep((4, 5.795))
        trigger_stop = 0
        while self.adb.find_img(target="logged_icon") is None:
            self.check_resolve()
            print(
                f'[ {current_time()} ] [ {self.name} ] while get_first_character')
            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)
            self.swipe(x, y, x2, y2)
            self.better_sleep((1.925, 2.795))
            trigger_stop += 1
            if trigger_stop > 4:
                self.print("Error in character switch. Bot is now stopped")
                self.set_status("Error.")
                while True:
                    self.script_pause()
                    sleep(1)
        x, y = self.adb.find_img(target="logged_icon")
        co = self.adb.find_img(target="logged_icon")
        self.print("Current character detected.")
        if x < 1280 // 2:
            x2 = x + uniform(480, 780)
            y2 = y + uniform(-20, 0)
            self.click(x2, y2)
            self.better_sleep((2.425, 2.795))
        elif y > 520 and x > 1280 // 2:
            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)
            self.swipe(x, y, x2, y2)
            self.better_sleep((2.425, 2.795))
            x, y = self.adb.find_img(target="logged_icon")
            self.better_sleep((2.025, 2.795))
            x2 = x - uniform(100, 320)
            y2 = y + uniform(80, 100)
            self.click(x2, y2)
            self.better_sleep((2.425, 2.795))
        elif x > 1280 // 2:
            x2 = x - uniform(100, 320)
            y2 = y + uniform(80, 100)
            self.click(x2, y2)
            self.better_sleep((2.425, 2.795))
            # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] test login" + str(
            #     self.adb.find_img(target="character_login_confirm")))
            # print(f'[ {current_time()} ] [ {self.name} ] TEST Login')
        self.better_sleep((2.425, 2.795))
        # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] character login" + str(
        #     self.adb.find_img(target="character_login_confirm")))
        if self.adb.find_img(target="character_login_confirm") is not None:
            self.print("Switching between character")
            x, y = uniform(700, 900), uniform(490, 527)
            self.click(x, y)
            # self.better_sleep((10, 15))
            # self.check_crash()
            # self.run_game()
            return co[0] + uniform(0, 5), co[1] + uniform(0, 5),
        else:
            self.print("No more characters, going back to the first character")
            x, y = uniform(400, 800), uniform(200, 250)
            x2, y2 = x + uniform(-20, 20), uniform(580, 645)
            self.swipe(x, y, x2, y2)
            self.better_sleep((3.5, 4.7))
            x, y = uniform(660, 1000), uniform(215, 280)
            self.click(x, y)
            self.better_sleep((1.8, 2.7))
            x, y = uniform(700, 910), uniform(491, 522)
            self.click(x, y)
            return uniform(660, 1000), uniform(215, 280)

    @get_name
    def change_character(self) -> bool:
        self.print("Switching Character.")
        self.set_status(f" Switching Character")
        x, y = uniform(15, 70), uniform(10, 60)
        self.click(x, y)
        self.better_sleep((1.925, 2.795))
        x, y = uniform(950, 1015), uniform(510, 560)
        self.click(x, y)
        self.better_sleep((1.925, 2.795))
        x, y = uniform(315, 380), uniform(330, 400)
        self.click(x, y)
        self.better_sleep((4, 5.795))
        i = 0
        while self.adb.find_img(target="logged_icon") is None:
            print(
                f'[ {current_time()} ] [ {self.name} ] while in change character')
            self.check_resolve()
            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)
            self.swipe(x, y, x2, y2)
            self.better_sleep((1.925, 2.795))
            i = i + 1
            if i == 3:
                self.print("Error in character switch. Bot is now stopped")
                self.set_status("Error.")
                while True:
                    self.script_pause()
                    sleep(1)
        x, y = self.adb.find_img(target="logged_icon")
        self.print("Current character detected.")
        if x < 1280 // 2:
            x2 = x + uniform(480, 780)
            y2 = y + uniform(-20, 0)
            self.click(x2, y2)
            self.better_sleep((2.425, 2.795))
        elif y > 520 and x > 1280 // 2:
            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)
            self.swipe(x, y, x2, y2)
            self.better_sleep((2.425, 2.795))
            x, y = self.adb.find_img(target="logged_icon")
            self.better_sleep((2.025, 2.795))
            x2 = x - uniform(100, 320)
            y2 = y + uniform(80, 100)
            self.click(x2, y2)
            self.better_sleep((2.425, 2.795))
        elif x > 1280 // 2:
            x2 = x - uniform(100, 320)
            y2 = y + uniform(80, 100)
            self.click(x2, y2)
            self.better_sleep((2.425, 2.795))
            # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] test login" + str(
            #     self.adb.find_img(target="character_login_confirm")))
            print(f'[ {current_time()} ] [ {self.name} ] tag change_character')
        self.better_sleep((2.425, 2.795))
        # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] character login" + str(
        #     self.adb.find_img(target="character_login_confirm")))
        if self.adb.find_img(target="character_login_confirm") is not None:
            self.print("Logging in..")
            x, y = uniform(700, 900), uniform(490, 527)
            self.click(x, y)
            # self.better_sleep((10, 15))
            # self.check_crash()
            # self.run_game()
            return True
        else:
            self.print("no more characters, going back to the first character")
            for _ in range(2):
                x, y = uniform(400, 800), uniform(200, 250)
                x2, y2 = x + uniform(-20, 20), uniform(580, 645)
                self.swipe(x, y, x2, y2)
                self.better_sleep((1.5, 2.7))
            x, y = uniform(660, 1000), uniform(215, 280)
            self.click(x, y)
            self.better_sleep((1.8, 2.7))
            x, y = uniform(700, 910), uniform(491, 522)
            self.click(x, y)
            return False

    @get_name
    def start_emulator(self) -> None:
        self.data = self.update_data()
        cmd = f'{path["HD-Player"]} --instance {self.data.get(self.sel).get("instance")}'
        subprocess.Popen(cmd)
        # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] {cmd}')
        # os.system(cmd)

    @get_name
    def get_dic_instances(self):
        try:
            with open('path.json', encoding='utf-8') as config_file:
                path = json.load(config_file)
            string = path["bluestacks"][:-5] + ".txt"
            if exists(rf'{path["bluestacks"]}'):
                string = path["bluestacks"][:-5] + ".txt"
                shutil.copy(rf'{path["bluestacks"]}', rf'{string}')
            with open(rf'{string}', 'r', encoding='utf-8') as file:
                data_instance = file.read().split('\n')
        except:
            raise OSError(
                "The path you provided is wrong ! We are looking for something like : \n 'C:\\ProgramData\\BlueStacks_nxt\\bluestacks.conf'")

        def sort_by_instance(tab):
            for _ in range(len(tab)):
                for y in range(len(tab) - 1):
                    if len(tab[y]['instance']) == len(tab[y + 1]['instance']):
                        if tab[y]['instance'] > tab[y + 1]['instance']:
                            tab[y], tab[y + 1] = tab[y + 1], tab[y]
                    else:
                        if len(tab[y]['instance']) > len(tab[y + 1]['instance']):
                            tab[y], tab[y + 1] = tab[y + 1], tab[y]
            dic = {}
            for i in range(len(tab)):
                dic[str(i)] = tab[i]
            return dic

        liste_info = []
        # for element in data_instance:
        #     if ((('bst.instance.Nougat64' in element or 'bst.instance.Nougat32' in element) and (
        #             'adb_port' in element)) and 'status' in element) or (
        #             ('bst.instance.Nougat64' in element or 'bst.instance.Nougat32' in element) and (
        #             'display_name' in element)):
        #         liste_info.append(element)
        for element in data_instance:
            if ((('bst.instance.Nougat64' in element) and (
                    'adb_port' in element)) and 'status' in element) or (
                    ('bst.instance.Nougat64' in element) and (
                    'display_name' in element)):
                liste_info.append(element)
        # for element in liste_info: print(element)
        tab_instance = []
        for i in range(0, len(liste_info), 2):
            string = liste_info[i + 1].split('.status.adb_port=')
            # print(f"{string=} ,  {liste_info[i]=}")

            string[1] = string[1].replace('"', "")
            string[0] = string[0][13:]

            string2 = liste_info[i].split('.display_name=')
            string2[1] = string2[1].replace('"', "")

            dico_instance = {
                'instance': str(string[0]),
                'port': string[1],
                'name': string2[1]
            }

            tab_instance.append(dico_instance)
        dico_instance = sort_by_instance(tab_instance)
        # print(tab_instance)
        return dico_instance

    @get_name
    def restart_emulator(self) -> None:
        self.data = self.update_data()
        self.pid = get_window_pid(self.adb.name)

        with open('path.json') as config_file: path = json.load(config_file)
        # adb_path = f"{path['HD-Player'].replace('Player', 'Adb')}"
        # cmd = f'"{adb_path}" -s 127.0.0.1:{self.data.get(self.sel).get("port")} reboot'
        cmd = f"taskkill /PID {self.pid} /F"
        print(f'[ {current_time()} ] [ {self.name} ] Executing {cmd}')
        logging.info(f"[{self.name}] Executing {cmd}")
        subprocess.Popen(cmd)
        # print("["+current_time()+"]" + " " +"Shutdown the emulator, waiting for 15seconds")
        sleep(15)

        cmd = f'{path["HD-Player"]} --instance {self.data.get(self.sel).get("instance")}'

        print(f'[ {current_time()} ] [ {self.name} ] Executing {cmd}')
        logging.info(f"[{self.name}] Executing {cmd}")
        process = multiprocessing.Process(target=subprocess.Popen, args=(cmd,))
        process.start()

        print(f'[ {current_time()} ] [ {self.name} ] Bot will wait 30 secs from now.')
        sleep(30)

        dico_instance = self.get_dic_instances()
        self.adb.port = dico_instance[self.sel]['port']
        self.data = self.update_data()
        self.data[self.sel]["port"] = int(dico_instance[self.sel]['port'])
        with open('user_settings.json', 'w') as config_file:
            config_file.write(json.dumps(self.data))
        self.data = self.update_data()
        # adb_path = f"{path['HD-Player'].replace('Player', 'Adb')}"
        # cmd = f'"{adb_path}" connect 127.0.0.1:{self.data.get(self.sel).get("port")}'
        print(f'[ {current_time()} ] [ {self.name} ] f"{cmd = } \nConnect from the device')
        self.adb.connect_to_device()

        # cmd = f'"{adb_path}" -s 127.0.0.1:{self.data.get(self.sel).get("port")}'
        # subprocess.Popen(cmd)

    @get_name
    def check_download_page(self, screen = None):
        if screen is None:
            if self.adb.find_img(target ="download_page", confidence=0.9):
                self.adb.click(uniform(1018,1041), uniform(127,146))
                self.better_sleep((1.925, 2.795))
        else:
            if self.adb.find_img(target ="download_page", source=screen, confidence=0.9):
                self.adb.click(uniform(1018,1041), uniform(127,146))
                self.better_sleep((1.925, 2.795))

    @get_name
    def change_character_param(self, co_first, nb_chars=0):
        self.print("Switching Character")
        self.set_status(f"Switching Character")
        deadstop = 0
        self.better_sleep((1.925, 2.795))
        x, y = uniform(15, 80), uniform(10, 60)
        self.click(x, y)
        self.better_sleep((1.925, 2.795))
        x, y = uniform(950, 1015), uniform(510, 560)
        self.click(x, y)
        self.better_sleep((1.925, 2.795))
        x, y = uniform(315, 380), uniform(330, 400)
        self.click(x, y)
        self.better_sleep((4, 5.795))
        while self.adb.find_img(target="logged_icon") is None:
            if deadstop == 5:
                self.print(f"Error in character switch. Bot is now stopped")

                self.set_status("Error.")
                while True:
                    self.script_pause()
                    sleep(1)
            self.check_resolve()
            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)
            self.swipe(x, y, x2, y2)
            self.better_sleep((1.925, 2.795))
            deadstop = deadstop + 1
        x, y = self.adb.find_img(target="logged_icon")
        self.print('Current character detected.')
        if x < 1280 // 2:
            x2 = x + uniform(480, 780)
            y2 = y + uniform(-20, 0)
            self.click(x2, y2)
            self.better_sleep((2.425, 2.795))
        elif y > 520 and x > 1280 // 2:
            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)
            self.swipe(x, y, x2, y2)
            self.better_sleep((2.425, 2.795))
            x, y = self.adb.find_img(target="logged_icon")
            self.better_sleep((2.025, 2.795))
            x2 = x - uniform(100, 320)
            y2 = y + uniform(80, 100)
            self.click(x2, y2)
            self.better_sleep((2.425, 2.795))
        elif x > 1280 // 2:
            x2 = x - uniform(100, 320)
            y2 = y + uniform(80, 100)
            self.click(x2, y2)
            self.better_sleep((2.425, 2.795))
            # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] test login" + str(
            #     self.adb.find_img("character_login_confirm")))
            self.print("Switching to the next character")
        self.better_sleep((2.425, 2.795))
        # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] character login" + str(
        #     self.adb.find_img("character_login_confirm")))
        if self.adb.find_img(target="character_login_confirm") is not None:
            self.print("Switching to the next character")
            x, y = uniform(700, 900), uniform(490, 527)
            self.click(x, y)
            # self.better_sleep((10, 15))
            # self.check_crash()
            # self.run_game()
            return True
        else:
            self.print("No more characters, going back to the first character")
            x, y = uniform(400, 800), uniform(200, 250)
            if nb_chars // 6 == 0:
                rounds = 1
            else:
                rounds = nb_chars // 6
            for _ in range(rounds):
                x2, y2 = x + uniform(-20, 20), uniform(580, 645)
                self.swipe(x, y, x2, y2)
                self.better_sleep((3.5, 4.7))
            x, y = co_first[0] + uniform(30, 300), co_first[1] + uniform(-30, 0)
            self.click(x, y)
            self.better_sleep((1.8, 2.7))
            x, y = uniform(700, 910), uniform(491, 522)
            self.click(x, y)
            return False
        # self.better_sleep((1.925, 2.795))
        # y,x=uniform(490,527),uniform(700,900)
        # self.click(x,y)
        # self.better_sleep((10, 15))
        # self.check_crash()
        # self.run_game()
        # self.better_sleep((1.925, 2.795))
        # self.check_crash()

    def collect_gold(self):
        co = self.adb.find_multiple_img(target="gold_max", confidence=0.8)
        co2 = self.adb.find_multiple_img(target="gold_min", confidence=0.8)
        co.extend(co2)
        co = list(filter(filter_coordinate, co))
        return choice(co) if co != [] else None

    def collect_food(self):
        co = self.adb.find_multiple_img(target="food_max", confidence=0.8)
        co2 = self.adb.find_multiple_img(target="food_min", confidence=0.8)
        co.extend(co2)
        co = list(filter(filter_coordinate, co))
        return choice(co) if co != [] else None

    def collect_wood(self):
        co = self.adb.find_multiple_img(target="wood_max", confidence=0.8)
        co2 = self.adb.find_multiple_img(target="wood_min", confidence=0.8)
        co.extend(co2)
        co = list(filter(filter_coordinate, co))
        return choice(co) if co != [] else None

    def collect_stone(self):
        co = self.adb.find_multiple_img(target="stone_max", confidence=0.8)
        co2 = self.adb.find_multiple_img(target="stone_min", confidence=0.8)
        co.extend(co2)
        co = list(filter(filter_coordinate, co))
        return choice(co) if co != [] else None

    @get_name
    def collect_resource(self):
        tasks = [self.collect_food, self.collect_wood, self.collect_stone, self.collect_gold]
        shuffle(tasks)
        tab = []
        for task in tasks:
            result = task()
            self.print(f"{task.__name__} {result = }")
            if result is not None:
                tab.append(result)
            else:
                self.print(f"{task.__name__} not found")
        for cords in tab:
            self.click(cords[0] + uniform(10,20), cords[1] + uniform(20,30))
            self.better_sleep((0.695, 1))

    @get_name
    def buy_merchant(self):
        co = self.adb.find_img(target="merchant_icon", confidence=0.7)
        if co is None:
            return
        if not filter_coordinate(co):
            return
        x, y = co[0] + uniform(0, 10), co[1] + uniform(0, 10)
        print(f'[ {current_time()} ] [ {self.name} ] Merchant icon : {x=} {y=}')
        self.click(x, y)
        for y in range(2):
            for _ in range(4):
                self.better_sleep((1.8, 2.2))
                food = self.adb.find_multiple_img("merchant_buy_with_food", 0.8)
                wood = self.adb.find_multiple_img("merchant_buy_with_wood", 0.8)
                # for element in wood:
                #     food.append(element)
                food.extend(wood)
                shuffle(food)
                for element in food:
                    self.click(element[0] + uniform(0, 30), element[1] + uniform(-2, 8))
                    self.better_sleep((0.45, 0.7))
                x1, y1 = uniform(586, 870), uniform(457, 487)
                x2, y2 = x1 + uniform(-10, 10), y1 - uniform(120, 150)
                self.swipe(x1, y1, x2, y2)
            if y != 0:
                break
            co = self.adb.find_img(target="free")
            if co is None:
                break
            x, y = co[0] + uniform(0, 50), co[1] + uniform(0, 20)
            self.click(x, y)
        x, y = uniform(1077, 1100), uniform(64, 95)
        self.click(x, y)

    @get_name
    def check_if_kill(self):
        return
        """
        Kill the process if his ppid is dead
        :exemple: leave python would kill the process
        """
        if not pid_exists(self.ppid):
            sys.exit(0)


    def get_available_task(self, profile=None):
        self.data = self.update_data()
        if profile is None:
            profile = self.data.get(self.sel)
        else:
            profile = self.data.get(self.sel).get('schedules').get(profile)
        # print(profile)
        lib_tasks = []
        if profile.get('claim_campaign', False):
            lib_tasks.append(self.claim_campaign)
        if profile.get('collect_ressource', False):
            lib_tasks.append(self.collect_resource)
        if profile.get('buy_merchant', False):
            lib_tasks.append(self.buy_merchant)
        if profile.get('gather_rss', False):
            lib_tasks.append(self.gather_rss2)
        if profile.get('use_enhanced_buff', False):
            lib_tasks.append(self.use_enhanced_buff)
        if profile.get('check_donation', False):
            lib_tasks.append(self.alliance_donation)
        if profile.get('defeat_barbarians', False):
            lib_tasks.append(self.hunt_barbarians)
        if profile.get('gather_gem', False):
            lib_tasks.append(self.gather_gem)
        if profile.get('scout_fog', False):
            lib_tasks.append(self.clear_fog)
        if profile.get('claim_daily_vip', False):
            lib_tasks.append(self.claim_daily_vip)
        if profile.get('start_fort', False):
            lib_tasks.append(self.start_fort)
        if profile.get('heal_troop', False):
            lib_tasks.append(self.heal_troops)
        if profile.get('material_production', False):
            lib_tasks.append(self.produce_materials)
        if profile.get('claim_daily_chest', False):
            lib_tasks.append(self.claim_daily_chest)
        shuffle(lib_tasks)
        if self.hunt_barbarians in lib_tasks and self.gather_rss2 in lib_tasks:
            a = lib_tasks.index(self.hunt_barbarians)
            b = lib_tasks.index(self.gather_rss2)
            if a > b:
                lib_tasks[a], lib_tasks[b] = lib_tasks[b], lib_tasks[a]

        if self.start_fort in lib_tasks:
            for element in [self.gather_rss2, self.gather_gem, self.hunt_barbarians]:
                if element in lib_tasks:
                    a = lib_tasks.index(self.start_fort)
                    b = lib_tasks.index(element)
                    if a > b:
                        lib_tasks[a], lib_tasks[b] = lib_tasks[b], lib_tasks[a]
        return lib_tasks

    def set_current_task(self, name):
        if name == 'claim_campaign':
            return self.set_status("Claiming campaign rewards")
        if name == 'collect_resource':
            return self.set_status("Collecting city rss")
        if name == 'buy_merchant':
            return self.set_status("Buying merchant..")
        if name == 'gather_rss2':
            return self.set_status("Gathering rss")
        if name == 'use_enhanced_buff':
            return self.set_status("Enabling enhanced buffs")
        if name == 'alliance_donation':
            return self.set_status("Donating to alliance")
        if name == 'hunt_barbarians':
            return self.set_status("Killing barbarians")
        if name == 'gather_gem':
            return self.set_status("Gathering gems")
        if name == 'scout_fog':
            return self.set_status("Exploring fog")
        if name == 'claim_daily_vip':
            return self.set_status("Daily VIP rewards")
        if name == 'claim_daily_chest':
            return self.set_status("Daily Chest rewards")
        if name == 'start_fort':
            return self.set_status("Launching fort")
        if name == 'heal_troops':
            return self.set_status("Healing troops")
        if name == 'produce_materials':
            return self.set_status("Producing materials")

    def get_current_task(self, name):
        if name == 'claim_campaign':
            return "Claiming campaign rewards"
        if name == 'collect_resource':
            return "Collecting city rss"
        if name == 'buy_merchant':
            return "Buying merchant.."
        if name == 'gather_rss2':
            return "Gathering rss"
        if name == 'use_enhanced_buff':
            return "Enabling enhanced buffs"
        if name == 'alliance_donation':
            return "Donating to alliance"
        if name == 'hunt_barbarians':
            return "Killing barbarians"
        if name == 'gather_gem':
            return "Gathering gems"
        if name == 'scout_fog':
            return "Exploring fog"
        if name == 'claim_daily_vip':
            return "Daily VIP rewards"
        if name == 'claim_daily_chest':
            return "Daily Chest rewards"
        if name == 'start_fort':
            return "Launching fort"
        if name == 'heal_troops':
            return "Healing troops"
        if name == 'produce_materials':
            return "Producing materials"

    def click_default_hut(self):
        x, y = uniform(710, 769), uniform(220, 265)
        self.click(x, y)

        sleep(uniform(1.5, 2))
        co = self.adb.find_img(target='hut_hammer')
        x, y = co[0] + uniform(0, 15), co[1] + uniform(0, 10)
        self.click(x, y)
        sleep(uniform(1.5, 2))

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
        if max_val > 0.98:
            print("Upgrade icon found")
            return max_loc[0], max_loc[1]
        else:
            img_to_find = cv2.imread('resources\\upgrade_age.png')
            result = cv2.matchTemplate(cv_image, img_to_find, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > 0.9:
                print("Upgrade age icon found")
                return max_loc[0], max_loc[1]
            return

    def click_help(self):
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = np.array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img_to_find = cv2.imread('resources\\help.png')
        result = cv2.matchTemplate(cv_image, img_to_find, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.7:
            print("Click help found")
            self.set_text(f"[{current_time()}] Clicking on helps..")
            print(max_loc)
            return self.click(max_loc[0] + uniform(5, 20), max_loc[1] + uniform(5, 20))
        else:
            return

    @get_name
    def enter_city(self):
        if self.in_city():
            x = uniform(24, 91)
            y = uniform(625, 680)
            self.click(x, y)
            self.better_sleep((1, 1.35))
            x = uniform(24, 91)
            y = uniform(625, 680)
            self.click(x, y)
            self.better_sleep((1, 1.35))
        else:
            x = uniform(24, 91)
            y = uniform(625, 680)
            self.click(x, y)
            self.better_sleep((1, 1.35))

    def is_in_builder(self):
        co = self.adb.find_img(target='builder', confidence=0.8)
        return co is not None

    def find_image_cv(self, image, confidence=0.8):
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = array(pil_image)
        result = cv2.matchTemplate(cv_image, image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > confidence:
            print(max_loc)
            return self.click(max_loc[0] + uniform(0, 5), max_loc[1] + uniform(0, 5))
        else:
            return

    def new_build(self):
        if not self.is_in_builder():
            return False
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv_image)
        print(img.getpixel((8, 355)))
        if img.getpixel((8, 355))[2] > 210 and img.getpixel((8, 355))[1] < 10:
            self.click(uniform(170, 360), uniform(400, 600))
            sleep(uniform(1, 1.2))
            co = self.adb.find_img(target='validate_building')
            if co is not None:
                self.click(uniform(-5, 5) + co[0], uniform(-10, 5) + co[1])
                sleep(uniform(1, 1.2))
                return True
        if img.getpixel((8, 472))[2] > 210 and img.getpixel((8, 472))[1] < 10:
            self.click(uniform(170, 360), uniform(400, 600))
            sleep(uniform(1, 1.2))
            co = self.adb.find_img(target='validate_building')
            if co is not None:
                self.click(uniform(-5, 5) + co[0], uniform(-10, 5) + co[1])
                sleep(uniform(1, 1.2))
                return True

    def is_tutorial(self):
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv_image)
        while img.getpixel((630, 610)) == (255, 255, 255) and img.getpixel((800, 610)) == (255, 255, 255):
            self.click(uniform(630, 800), uniform(500, 610))
            sleep(uniform(1.2, 1.7))

    def click_hdv(self):
        self.click(uniform(390, 500), uniform(200, 280))
        sleep(uniform(1.5, 2))

    @get_name
    def check_chest(self):
        for _ in range(2):
            pil_image = self.adb.get_curr_device_screen_img()
            cv_image = array(pil_image)
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            cropped_image = cv_image[30:170, 770:1225]
            for i in range(1, 4):
                chest = self.adb.find_img(target=f"verification_chest{i}", source=cropped_image, confidence=0.6)
                if chest is None:
                    break
            if chest is not None:
                if self.data.get(self.sel).get('schedules').get(self.current_profile).get('auto_captcha', False):
                    # print(co)
                    self.check_if_kill()
                    self.click(chest[0] + uniform(775, 795), chest[1] + uniform(35, 50))
                    self.better_sleep((3, 4))
                    return True
                else:
                    self.set_text("Captcha is Off")
                    self.set_status("Captcha is Off")
                    while True:
                        self.script_pause()
                        sleep(1)
            sleep(0.3)
        return False

    @get_time
    def check_resolve(self, chest=True) -> bool:
        """
        Check and resolve verification
        """
        self.data = self.update_data()
        self.print(f"Scanning the screen for verification..")
        solver = self.getSolver()

        if chest:
            self.check_chest()

        co = self.adb.find_img(target="verification_button")
        if co is not None:
            self.click(co[0] + uniform(0, 80), co[1] + uniform(0, 20))
            self.better_sleep((5, 6))

        i = 0
        resolved = False

        while self.adb.find_img(target="close_refresh_ok", confidence=0.75) is not None:
            if i == 0:
                self.print("Verification detected")
            captchaId = self.resolve_captcha()
            self.better_sleep((3, 4))
            resolved = self.report_feedback(captchaId, resolved, solver)
            if i == 5:
                self.print("Error, unable to resolve the captcha for 5 times in a row !")
                return False
            i = i + 1
        return resolved

    @get_name
    def report_feedback(self, captchaId, resolved, solver):
        co = self.adb.find_img(target="refresh_resolve")
        if co is not None:
            self.print("Captcha failed !")
            if captchaId is not None:
                solver.report(captchaId, False)
        else:
            resolved = True
            solver.report(captchaId, True)
            self.print("Captcha successfully solved !")
        return resolved

    @get_name
    def getSolver(self):
        if self.data[self.sel]['API_KEY'] != "":
            key = self.data[self.sel]['API_KEY']
        else:
            key = '4805a29997857b110ef26530c7f39db1'
        api_key = os.getenv('APIKEY_2CAPTCHA', key)
        solver = TwoCaptcha(api_key)
        return solver

    def check_log_back(self, cv_image=None):
        self.data = self.update_data()
        # print(f'{self.data.get(self.sel).get("auto_log_back"] =}')
        if cv_image is None:
            co = self.adb.find_img(target="already_connected")
            # print(f'{co}')
        else:
            co = self.adb.find_img(source=cv_image, target="already_connected", confidence=0.9)
            if co is not None:
                if cv_image is None:
                    co = self.adb.find_img(target="reconnect")
                else:
                    co = self.adb.find_img(source=cv_image, target="reconnect", confidence=0.9)
        if co is not None:
            if self.data.get(self.sel).get('schedules').get(self.current_profile).get('auto_log_back', False):

                if self.data.get(self.sel).get('schedules').get(self.current_profile).get('log_back1') > self.data.get(
                        self.sel).get('schedules').get(self.current_profile).get('log_back2'):
                    self.data[self.sel]['schedules'][self.current_profile]['log_back1'], \
                        self.data[self.sel]['schedules'][self.current_profile]['log_back2'] = \
                        self.data[self.sel]['schedules'][self.current_profile]['log_back2'], \
                            self.data[self.sel]['schedules'][self.current_profile]['log_back1']

                value = randint(self.data.get(self.sel).get('schedules').get(self.current_profile).get('log_back1'),
                                self.data.get(self.sel).get('schedules').get(self.current_profile).get(
                                    'log_back2') * 60)
                self.print(f"Waiting for the timer to end.. {value} minutes")
                sleep(value)
                self.click(co[0] + uniform(0, 50), co[1] + uniform(-10, 20))
                self.print("Reconnection..")
                sleep(uniform(5, 10))
                self.run_game()
                return True
            else:
                self.set_text("Auto Log-back off")
                while True:
                    self.script_pause()
                    sleep(1)
        else:
            return False

    @get_name
    def check_mge(self):
        co = self.adb.find_img(target="mightiest_gov")
        if co is not None:
            self.click(co[0] + uniform(10, 30), co[1] + uniform(10, 30))
            self.better_sleep((1.3, 2))

    @get_name
    def check_reconnect(self, cv_image=None):
        """
        Check and reconnect
        """
        self.data = self.update_data()
        if cv_image is None:
            co = self.adb.find_img(target="reconnect")
        else:
            co = self.adb.find_img(source=cv_image, target="reconnect", confidence=0.85)
        if co is not None:
            if self.data.get(self.sel).get('schedules').get(self.current_profile).get('auto_reconnect', False):
                print(co)
                if cv_image is not None:
                    a = (co[0] + uniform(0, 100) + 480, 420 + co[1] + uniform(0, 20))
                    print(a)
                    self.click(a[0], a[1])
                else:
                    a = (co[0] + uniform(0, 100), co[1] + uniform(0, 20))
                    print(a)
                    self.click(a[0], a[1])
                self.wait_until_connected()
                return True
            else:
                self.set_text("Reconnection disabled")
                while True:
                    self.script_pause()
                    sleep(1)

    @get_name
    def go_city(self):
        if not self.in_city():
            x = uniform(24, 91)
            y = uniform(625, 680)
            self.click(x, y)
            self.better_sleep((1.5, 2))

    def execute_tasks(self, lib_tasks):
        co = self.adb.find_img(target="hide_quests")
        if co is not None:
            self.click(co[0] + uniform(0, 20), co[1] + uniform(0, 20))
        self.check_download_page()
        current_task = 1
        for func in lib_tasks:
            self.check_download_page()
            self.leave_kd_buff()
            self.print(f"----- Task {current_task}/{len(lib_tasks)} -----".center(60))
            self.print(f"Currently executing : {self.get_current_task(func.__name__)}")
            self.set_current_task(func.__name__)
            self.run_game()
            self.check_log_back()
            self.check_reconnect()
            self.check_resolve()
            # self.set_status()
            if func.__name__ in ["alliance_donation", "collect_resource", "buy_merchant", "scout_fog", "heal_troop",
                                 "claim_daily_chest"]:
                self.go_city()
            try:
                # print(f"{ func.__name__ in ['gather_rss','gather_gem'] =}")
                if func.__name__ in ["gather_rss2", "gather_gem"]:
                    pil_image = self.adb.get_curr_device_screen_img()
                    cv_image = np.array(pil_image)
                    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
                    cv_image = cv_image[0:100, 0:800]
                    # print(f'{self.adb.find_img_src_conf(cv_image,"block_icon",0.90)=}')
                    if self.adb.find_img(target="block_icon", source=cv_image, confidence=0.90) is None:
                        func()
                else:
                    func()
                self.better_sleep((1, 2))
            except Exception as e:
                print(e)
                logging.exception(f" [{self.name}] Exception during {func.__name__}")
                self.leave_game()
                # logging.info(f"[{self.name}] Game is stopped, game starting in about 7sec")
                self.better_sleep((5, 10))
                self.run_game()
            self.better_sleep((0.795, 1.2))
            current_task += 1
            if ('buy_merchant' in func.__name__) or ('gather_rss2' in func.__name__):
                self.check_resolve()
                self.better_sleep((0.795, 1.2))

    # def routine(self):
    #     # self.set_text("Starting..")
    #     self.adb.connect_to_device()
    #     self.set_status("Starting..")
    #     self.data = self.update_data()
    #     logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s",
    #                         datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
    #
    #     while self.data.get(self.sel).get("loop_task", False):
    #         print(f'[ {current_time()} ] [ {self.name} ] Script is starting')
    #         self.set_text(f"[{current_time()}] Script is starting")
    #         logging.info(f"[{self.name}] Script is starting")
    #
    #         # First character
    #         self.run_game()
    #         self.check_log_back()
    #         self.check_reconnect()
    #         starting_time = time()
    #         self.check_mge()
    #         self.check_resolve()
    #         # rss_total = []
    #         # total = [0, 0, 0, 0]
    #         # rss_total.append(self.adb.resource_amount_image_to_string())
    #         self.execute_tasks(self.get_available_task())
    #
    #         if self.data.get(self.sel).get('schedules').get(self.current_profile).get("switch_character", False):
    #             co_first = self.get_first_character()
    #             boolean = True
    #             self.wait_until_connected()
    #             # while self.adb.find_img(target="menu_button") is None:
    #             #     self.better_sleep((10, 15))
    #             self.run_game()
    #             # Characters remaining
    #             while boolean:
    #                 # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] Premier check_resolve dans le while')
    #                 self.run_game()
    #                 self.check_mge()
    #                 self.check_resolve()
    #                 # rss_total.append(self.adb.resource_amount_image_to_string())
    #
    #                 self.execute_tasks(self.get_available_task())
    #                 self.better_sleep((2.2, 4))
    #
    #                 boolean = self.change_character_param(co_first)
    #                 # self.better_sleep((50, 70))
    #                 self.wait_until_connected()
    #                 # while self.adb.find_img(target="menu_button") is None:
    #                 #     self.better_sleep((10, 15))
    #                 #     self.check_reconnect()
    #         # Rss total
    #         # for i in range(len(rss_total)):
    #         #     for y in range(4):
    #         #         total[y] = total[y] + rss_total[i][y]
    #         # print(total)
    #         # for i in range(4):
    #         #     total[i] = total[i] // 1000000
    #         # print(total)
    #         print(f'[ {current_time()} ] [ {self.name} ] Script ran for {(time() - starting_time) / 60:0.1f} minutes. ')
    #         logging.info(f"[{self.name}] Script ran for {(time() - starting_time) / 60:0.1f} minutes.")
    #         self.set_text(f"[{current_time()}] Script ran for {(time() - starting_time) / 60:0.1f} minutes.")
    #         ttw1, ttw2 = self.data.get(self.sel).get("time_to_wait_loop1", 60), self.data.get(self.sel).get(
    #             "time_to_wait_loop2",
    #             90)
    #
    #         if ttw1 > ttw2:
    #             ttw1, ttw2 = ttw2, ttw1
    #         time_before_redo_tasks = int(randint(ttw1, ttw2) * 60) + randint(0, 60)
    #         # print(time_before_redo_tasks, type(time_before_redo_tasks))
    #         print(
    #             f'[ {current_time()} ] [ {self.name} ] Script is paused for {time_before_redo_tasks / 60:0.1f} minutes')
    #         logging.info(f"[{self.name}] Script is paused for {time_before_redo_tasks / 60:0.1f} minutes")
    #         self.set_text(f"[{current_time()}] Script is paused for {time_before_redo_tasks / 60:0.1f} minutes")
    #         self.set_status((datetime.fromtimestamp(time_before_redo_tasks) - timedelta(hours=1)).strftime("%H:%M:%S"))
    #         # print((datetime.fromtimestamp(time_before_redo_tasks)-timedelta(hours=1)).strftime("%H:%M:%S"))
    #         # print(time_before_redo_tasks,datetime.fromtimestamp(time_before_redo_tasks))
    #         if self.data.get(self.sel).get("leave_game_loop", False):
    #             self.leave_game()
    #         sleep(time_before_redo_tasks)
    #
    #         # self.better_sleep(((ttw -3)*60,((ttw +3)*60)))
    #     if self.data.get(self.sel).get("loop_task", False):
    #         return
    #
    #     print(f'[ {current_time()} ] [ {self.name} ] Script is starting')
    #     logging.info(f"[{self.name}] Script is starting")
    #     self.set_text(f"[{current_time()}] Script is starting")
    #     self.set_status("Script is starting")
    #     self.run_game()
    #     self.check_log_back()
    #     self.check_reconnect()
    #     starting_time = time()
    #     self.check_mge()
    #     self.check_resolve()
    #     # First character
    #     self.execute_tasks(self.get_available_task())
    #     if self.data.get(self.sel).get('schedules').get(self.current_profile).get("switch_character", False):
    #         co_first = self.get_first_character()
    #         boolean = True
    #         self.wait_until_connected()
    #         self.run_game()
    #         # Characters remaining
    #         while boolean:
    #             self.run_game()
    #             self.check_resolve()
    #             self.check_mge()
    #
    #             self.execute_tasks(self.get_available_task())
    #             self.better_sleep((2.2, 4))
    #
    #             boolean = self.change_character_param(co_first)
    #             self.wait_until_connected()
    #     print(
    #         f'[ {current_time()} ] [ {self.name} ] The bot took {(time() - starting_time) // 60} minutes to complete all the tasks, bot is waiting for your instructions.')
    #     logging.info(
    #         f"[{self.name}] The bot took {(time() - starting_time) // 60} minutes to complete all the tasks, bot is waiting for your instructions")
    #     self.set_text(f"[{current_time()}] minutes to complete all the tasks, bot is waiting for your instructions")
    #     return

    def routine_scheduled(self):
        self.adb.connect_to_device()
        self.data = self.update_data()
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")

        loop_task = 1 if not self.data.get(self.sel).get("loop_task") else 9999999999999

        starting_time = time()
        for i in range(loop_task):
            loop_time = time()
            self.print(" Script is starting ! ".center(56,"-"))
            self.data = self.update_data()
            for profile in self.data[self.sel]['schedules']:
                if self.data[self.sel]['schedules'][profile]['enabled']:
                    self.current_profile = profile
                    self.print(f" Profile n°{profile} enabled ! ".center(60))
                    if self.data.get(self.sel).get('schedules').get(self.current_profile).get("switch_character"):
                        self.print(f"---- Character n°1 ----".center(60))
                    self.run_game()
                    self.check_log_back()
                    self.check_reconnect()
                    self.leave_kd_buff()
                    self.check_mge()
                    self.check_resolve()
                    # First character
                    self.execute_tasks(self.get_available_task(profile))
                    if self.data.get(self.sel).get('schedules').get(self.current_profile).get("switch_character",
                                                                                              False):
                        co_first = self.get_first_character()
                        boolean = True
                        self.wait_until_connected()

                        self.run_game()
                        # Characters remaining
                        nb_characters = 2
                        while boolean:
                            self.print(f"---- Character n°{nb_characters} ----".center(60))
                            self.run_game()
                            self.check_resolve()
                            self.check_mge()

                            self.execute_tasks(self.get_available_task(profile))
                            self.better_sleep((2.2, 4))

                            nb_characters += 1
                            boolean = self.change_character_param(co_first, nb_characters)
                            self.wait_until_connected()
                    if not self.data[self.sel]['scheduler']:
                        break


            if self.data.get(self.sel).get("loop_task"):
                ttw1, ttw2 = self.data.get(self.sel).get("time_to_wait_loop1", 60), self.data.get(self.sel).get(
                    "time_to_wait_loop2", 90)
                self.print(f"Run nb°{i} took {(time() - loop_time) / 60:0.1f} minutes to complete.")
                if ttw1 > ttw2:
                    ttw1, ttw2 = ttw2, ttw1
                time_before_redo_tasks = int(randint(ttw1, ttw2) * 60) + randint(0, 60)
                self.print(f"Script is paused for {time_before_redo_tasks / 60:0.1f} minutes")
                self.set_status((datetime.fromtimestamp(time_before_redo_tasks) - timedelta(hours=1)).strftime("%H:%M:%S"))
                if self.data.get(self.sel).get("leave_game_loop", False):
                    if time_before_redo_tasks< 600:
                        self.leave_game(force=True)
                    else:
                        self.leave_game(force=False)

                for _ in range(time_before_redo_tasks):
                    self.script_pause()
                    sleep(1)

        self.print(f"The bot took {(time() - starting_time) // 60} minutes to complete all the tasks, bot is waiting for your instructions.")
        return
