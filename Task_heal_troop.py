import json

import numpy as np
from numpy import array
from random import uniform, shuffle, choice, randint

import cv2
from pytesseract import pytesseract

from Task import Task
from Task_utils import get_name, get_class, filter_coordinate

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class HealTroop(Task):
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
        return "HealTroop"

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
    def click_help(self):
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = np.array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img_to_find = cv2.imread('resources\\help.png')
        result = cv2.matchTemplate(cv_image, img_to_find, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.7:
            self.print("Clicking on helps..")
            return self.click(max_loc[0] + uniform(5, 20), max_loc[1] + uniform(5, 20))
        else:
            return

    @get_class
    def run(self):
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
