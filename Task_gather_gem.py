import json
import os
import shutil
import traceback
from datetime import datetime
from time import sleep, time

import numpy as np
import win32api
import win32con
import win32gui
from PIL import Image
from numpy import array
from random import uniform, randint, random

import cv2
from pytesseract import pytesseract

from Task import Task
from Task_utils import get_name, get_class, current_time

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class GatherGem(Task):
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
        return "GatherGem"

    @get_name
    def random_macro(self) -> None:
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
    def select_lineup_color(self, color: str) -> None:
        """
        Change the line-up until the yellow line-up is selected.
        """
        deadstop = 0
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
    def send_new_troop(self, deadstop: int = 0, color: str = 'yellow') -> bool:
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
            traceback.print_exc()
            self.better_sleep((5, 10))
            if deadstop == 2:
                self.click(uniform(700, 720), uniform(300, 340))
                self.better_sleep((1, 3))
                return False
            return self.send_nearest_troop_gem(deadstop=deadstop + 1)

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
                            return self.run()
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

                        if self.send_new_troop():
                            self.check_if_kill()
                            break
                        self.print("Trying to send the nearest troop..")
                        if self.send_nearest_troop_gem():
                            if self.adb.find_img(target="new_troops_button"):
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
                                return self.run()
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

    @get_name
    def swipe_scan(self, scan, direction):
        self.check_if_kill()
        self.script_pause()
        # print(f'[ {current_time()} ] [ {self.name} ] {direction = } {scan = }')
        direction()
        self.better_sleep((1, 1.25))
        return scan()

    @get_class
    def run(self):
        """
                   Gather gems
                   """
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
                    self.print("Time to restart the game during gathering gems !")
                    self.leave_game(force=True)
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
