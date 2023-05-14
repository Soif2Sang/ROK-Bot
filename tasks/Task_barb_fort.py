import json
import os
import shutil
from datetime import datetime
from time import sleep, time

import win32api
import win32con
import win32gui
from PIL import Image
from random import uniform, randint

import cv2
from pytesseract import pytesseract

from tasks.Task import Task, get_name, current_time
from tasks.Task_heal_troop import HealTroop
from utils.Task_utils import get_class, get_data, get_path

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class BarbFort(Task):
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
        return "BarbarianFort"

    @get_name
    def random_macro(self) -> None:
        try:
            path_json = get_path()
            for name in ["com.lilithgame.roc.gp.cfg", "com.rok.gp.vn.cfg", "com.lilithgame.rok.gpkr.cfg", "com.lilithgames.rok.gp.jp.cfg",
                         "com.lilithgames.rok.gpkr.cfg"]:
                path = path_json['bluestacks'][:-15] + "Engine\\UserData\\InputMapper\\UserFiles\\" + name
                if os.path.isfile(path):
                    break
            path2 = path.replace("cfg", "json")
            # print(f"{path = }")
            # print(f"{path2 = }")
            shutil.copy(path, path2)
            # print("test")
            path_json = get_path()
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
                self.print("/!\ FIX IT !! /!\ ","red")
            print(
                f"[ {current_time()} ] [ {self.name} ] Wrong macro location, cannot randomise it.. Please import the file com.lilithgame.roc.gp.cfg \nIf you don't know how to do it please watch the video in the #tutorial\n{e}")
            self.print(
                "Wrong macro location, cannot randomise it.. Please import the file com.lilithgame.roc.gp.cfg \nIf you don't know how to do it please watch the video in the #tutorial","red")
            for _ in range(5):
                self.print("/!\ FIX IT !! /!\ ","red")

    @get_name
    def zoom_out_city(self) -> None:
        """
        Leave the city by sending 'F5' key signal to the emulator
        """

        self.script_pause()
        try:
            self.print("Zooming out..")
            co = self.find_img(target='gem_search_button')
            if co is not None:
                hwnd = win32gui.FindWindow(None, self.adb.name)
                hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)
                for _ in range(4):
                    self.script_pause()
                    boolean = self.find_img(target="gem_search_button")
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
    def enough_action_points(self) -> bool:
        cv_image = self.adb.get_cv2_img()
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
    def already_mining(self, x, y, image) -> bool:
        """
        :param: x -> int - x location of the node
        :param: y -> int - y location of the node
        :param: image -> image - device screenshot
        :return: True if node is not free
        :return: False if node is free to gather
        """
        cv_image = self.pil_to_array(image)
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
    def find_cross(self) -> bool:
        """
        :return: True if node is occupied or someone is coming to the node
        :return: False if node is free to gather
        """
        self.print("Scanning the node..")
        cv_image = self.adb.get_cv2_img()
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
    def click_on_fort(self) -> bool:
        i = 0
        while (co := self.find_img(target="fort_rally_button1")) is None:
            x, y = uniform(610, 650), uniform(340, 388)
            self.click(x, y)
            self.better_sleep((0.725, 0.995))
            i = i + 1
            if i == 4:
                return False
        self.better_sleep((1.0, 1.395))
        # co = self.find_img(target="fort_rally_button1")
        if co is not None:
            x, y = co[0], co[1]
            x, y = x + uniform(0, 144), y + uniform(0, 30)
            self.click(x, y)
            self.better_sleep((1.325, 1.795))
            return True
        else:
            return False

    @get_name
    def select_lineup_color(self, color: str) -> None:
        """
        Change the line-up until the yellow line-up is selected.
        """
        deadstop = 0
        while self.find_img(target=f'{color}_icon', confidence=0.95) is None and self.find_img(target=
                                                                                                       "troops_march_button") is not None:
            if deadstop == 5:
                self.click(uniform(700, 800), uniform(271, 300))
                self.better_sleep((0.557, 0.796))
                self.print("Error in line-up selection")
                self.set_text("Error in line-up selection")
                self.send_discord_message("Error in line-up selection, human interaction required.")

                while True:
                    self.script_pause()
                    sleep(1)
            self.click(uniform(1092, 1114), uniform(260, 282))
            self.better_sleep((0.557, 0.796))
            deadstop = deadstop + 1
            self.print("Switching between line-up..")

    @get_name
    def scan_fort(self):
        """
        Scan device screenshot to find gem node,          not 100% working need improvement
        :return: None
        """
        screen = self.adb.get_curr_device_screen_img()
        info_screen = self.pil_to_array(screen)
        info_screen = cv2.cvtColor(info_screen, cv2.COLOR_BGR2RGB)
        info_screen = info_screen[470:700, 0:115]

        if self.find_img(source=info_screen, target="gem_search_button", confidence=0.8) is not None:
            self.zoom_out_city()
            self.better_sleep((2, 3))
            screen = self.adb.get_curr_device_screen_img()

        if self.find_img(source=info_screen, target="hammer", confidence=0.8) is not None:
            self.click(uniform(24, 91), uniform(625, 680))
            self.better_sleep((1.5, 2))
            self.zoom_out_city()
            self.better_sleep((2, 3))
            screen = self.adb.get_curr_device_screen_img()

        screen = self.pil_to_array(screen)
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

        if not self.data[self.sel]['schedules'][self.current_profile]["mauraudeurs_forts"]:
            for second_string in ["left", "mid", "right"]:
                for first_string in ["up", "mid", "down"]:
                    self.check_if_kill()
                    # f"{screen}fort_icon_day_{first_string}_{second_string}"
                    co = self.find_img(source=screen, target=f"fort_icon_day_{first_string}_{second_string}", confidence=0.8)
                    co = self.validate_co(co)
                    if co is None:
                        co = self.find_img(source=screen, target=f"fort_icon_night_{first_string}_{second_string}", confidence=0.8)
                        co = self.validate_co(co)
                    if co is not None:
                        self.print(f"Fort Found - x: {co[0]} y:{co[1]}")
                        self.check_if_kill()
                        if self.already_mining(co[0], co[1], screen):
                            self.print("Someone is already rallying it")
                            continue
                        self.click(co[0], co[1])
                        x_click = co[0]
                        y_click = co[1]
                        self.better_sleep((2, 2.5))
                        self.check_if_kill()
                        self.check_captcha()
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
                                co = self.find_img(target="fort_rally_button2")
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
                                    # if self.data[str(self.sel)]['schedules'][self.current_profile].get(
                                    #         'rally_type') == 'inf':
                                    #     # self.click(uniform(982,998),uniform(280,298))
                                    #     # self.better_sleep((0.7, 1.2))
                                    #     self.click(uniform(657, 680), uniform(96, 117))
                                    #     self.better_sleep((0.7, 1.2))
                                    # if self.data[str(self.sel)]['schedules'][self.current_profile].get(
                                    #         'rally_type') == 'cav':
                                    #     # self.click(uniform(982,998),uniform(390,405))
                                    #     # self.better_sleep((0.7, 1.2))
                                    #     self.click(uniform(770, 795), uniform(96, 117))
                                    #     self.better_sleep((0.7, 1.2))
                                    # if self.data[str(self.sel)]['schedules'][self.current_profile].get(
                                    #         'rally_type') == 'archers':
                                    #     # self.click(uniform(982,998),uniform(330,350))
                                    #     # self.better_sleep((0.7, 1.2))
                                    #     self.click(uniform(886, 906), uniform(96, 117))
                                    #     self.better_sleep((0.7, 1.2))
                                    self.click(uniform(657, 680), uniform(96, 117))
                                    self.better_sleep((0.7, 1.2))
                                    self.click(uniform(1092, 1112), uniform(330, 350))
                                    self.better_sleep((2,3))
                                    pil_image = self.adb.get_curr_device_screen_img()
                                    cv_image =self.pil_to_array(pil_image)
                                    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
                                    x, y = self.find_img(target="troops_march_button", confidence=0.8)
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
                                    self.better_sleep((2,3))
                                    self.go_city()
                                    self.better_sleep((2,3))
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
                                    HealTroop(self).run()
                                    return True
        else:
            self.check_if_kill()
            co = self.find_img(source=screen, target="maraudeurs_forts_icon", confidence=0.8)
            co = self.validate_co(co)
            if co is not None:
                self.print(f"Fort Found - x: {co[0]} y:{co[1]}")
                self.check_if_kill()
                if self.already_mining(co[0], co[1], screen):
                    self.print("Someone is already rallying it")
                self.click(co[0], co[1])
                self.print(f"x = {co[0]} y = {co[1]}")
                x_click = co[0]
                y_click = co[1]
                self.better_sleep((2, 2.5))
                self.check_if_kill()

                self.check_captcha()
                if self.find_cross():
                    self.print(f'Someone is already rallying it..')
                    return self.adjusted_leave_city(x_click, y_click)
                else:
                    self.check_if_kill()
                    bo1 = self.click_on_fort()
                    if not bo1:
                        self.print(f'Unable to click on the fort, leaving the fort !')
                        # return self.adjusted_leave_city(x_click, y_click)
                        return False
                    else:

                        self.better_sleep((1, 1.5))
                        co = self.find_img(target="fort_rally_button2")
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
                            cv_image =self.pil_to_array(pil_image)
                            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
                            x, y = self.find_img(source=cv_image, target="troops_march_button", confidence=0.8)
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
    def swipe_scan(self, scan, direction):
        self.check_if_kill()
        self.script_pause()
        # print(f'[ {current_time()} ] [ {self.name} ] {direction = } {scan = }')
        direction()
        self.better_sleep((1, 1.25))
        return scan()

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

        self.print(f'The bot selected the path nº{randomization}.')

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

    @get_class
    def run(self):
        self.random_macro()
        if not self.enough_action_points():
            self.print("Bot detected you are low in action point, bot prefers to not start a rally !")
            return
        self.run_game()
        self.check_captcha()
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
            cv_image =self.pil_to_array(pil_image)
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            cropped_image = cv_image[0:100, :800]
            if self.find_img(target="block_icon", source=cropped_image, confidence=0.90) is not None:
                return
            self.check_if_kill()
            if self.scan_fort(): return
            self.check_reconnect(cv_image)
            self.check_log_back()
            self.check_captcha(False)

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
                    self.check_captcha(False)
                    self.check_if_kill()

                    for _ in range(width):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_fort, self.swipe_left):
                            return
                        # self.better_sleep((0.125, 0.195))
                    self.check_captcha(False)
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
                    self.check_captcha(False)
                    self.check_if_kill()

                    for _ in range(width):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_fort, self.swipe_right):
                            return
                        # self.better_sleep((0.125, 0.195))
                    self.check_captcha(False)
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

                    self.check_captcha(False)
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

                    self.check_captcha(False)
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
                    self.check_captcha(False)

                    for _ in range(height):
                        if time_to_beat < time(): return
                        if self.swipe_scan(self.scan_fort, self.swipe_down):
                            return
                        # self.better_sleep((0.125, 0.195))
                    self.check_captcha(False)
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
