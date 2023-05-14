import json
import math
import os
import shutil
import traceback
from datetime import datetime
from time import sleep, time

import win32api
import win32con
import win32gui
from PIL import Image
from random import uniform, randint, random, choice

import cv2
from pytesseract import pytesseract

from tasks.Task import Task
from tasks.Task_alliance_help import AllianceHelp
from utils.Task_utils import get_name, get_class, current_time, get_data, get_path

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class Maraudeurs(Task):
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
        self.end_time = None
        self.block = False
        self.nb_hunter = 0
        self.hunter_selection = False

    def task_name(self):
        return "GatherGem"

    # @get_name
    # def run_game(self, count=0) -> None:
    #     if not self.adb.is_game_alive():
    #         super().run_game()
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
            shutil.copy(path, path2)

            with open(path2,encoding='utf-8') as config_file:
                macro_json = json.load(config_file)
            for element in macro_json['ControlSchemes']:
                if element["Selected"]:
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
                json.dump(macro_json, outfile, ensure_ascii=False)
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

    def validate_co(self, co: tuple[int, int]) -> None | tuple[int, int]:
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
                self.send_discord_message("Error in line-up selection, please fix the game")
                while True:
                    self.script_pause()
                    sleep(1)
            self.click(uniform(1092, 1114), uniform(225, 248))
            self.better_sleep((0.557, 0.796))
            deadstop = deadstop + 1
            self.print("Switching between line-up..")

    @get_name
    def free_troop_gem(self) -> bool:
        """
        :return: True if there's a empty queue
        :return: False if queues are occupied
        """

        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = self.pil_to_array(pil_image)
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
    def send_new_troop(self, deadstop: int = 0, preset: str = "1") -> bool:
        """
        Send a new troop to gather the gem node
        :return: True is successfully
        :return: False is not successfully
        """

        self.print(f"Trying to send new troop.. {preset=}")
        if deadstop != 0:
            self.print(f"Send new troop count : {deadstop}")
        if deadstop == 5:
            self.click(uniform(700, 800), uniform(300, 500))
            self.better_sleep((1.325, 1.795))
            return False
        co = self.find_img(target="new_troops_button")
        if co is not None:
            self.click(co[0] + uniform(0, 20), co[1] + uniform(0, 20))
            self.better_sleep((1.825, 2.495))
            self.select_lineup_color(color="red")
            presets = {
                "1": 290,
                "2": 346,
                "3": 402,
                "4": 458,
                "5": 517,
                "6": 570,
                "7": 626
            }
            self.click(uniform(1096, 1118), presets[preset])
            self.better_sleep((0.5, 1))
            co = self.find_img(target="troops_march_button")
            if co is None:
                return self.send_new_troop(deadstop=deadstop + 1, preset=preset)
            self.click(co[0] + uniform(0, 20), co[1] + uniform(0, 20))
            self.better_sleep((0.5, 0.7))
            if self.find_img(target="troops_march_button"):
                self.print("Unable to send a new troop")
                self.close_windows()
                return False
            self.print("New Troop sent !")
            return True
        co = self.find_img(target="march_bar")
        if co is not None and self.free_troop_gem():
            self.close_windows()
            self.better_sleep((0.5, 0.7))
            return self.send_new_troop(deadstop=deadstop + 1, preset=preset)
        self.print("Unable to send a new troop")
        return False

    @get_name
    def deploy_hunter(self):
        full_area = [(i, y) for i in range(420, 840, 5) for y in range(200, 530, 5) if
                     not (795 > i > 490 and 210 < y < 490)]
        hunters = 0
        breakloop = False
        for preset in self.data[str(self.sel)]['schedules'][str(self.current_profile)]["barbarians_preset"]:
            if not self.data[str(self.sel)]['schedules'][str(self.current_profile)]["barbarians_preset"][preset]:
                continue
            sent = False
            if breakloop:
                break
            while not sent:
                self.print(f"{hunters =}, {preset =}")
                if not full_area:
                    breakloop = True
                    break
                co = choice(full_area)
                self.print(f"Choice {co}")
                for i in range(-65, 80, 5):
                    for y in range(-65, 70, 5):
                        if (co[0] + i, co[1] + y) in full_area:
                            full_area.remove((co[0] + i, co[1] + y))
                self.swipe_arg(co[0], co[1], co[0], co[1], randint(2500, 3475))
                self.better_sleep((1.325, 1.795))
                co = self.find_img(target="deploy_march_button")
                if co is not None:
                    self.click(co[0] + uniform(0, 140), co[1] + uniform(0, 4))
                    self.better_sleep((1.325, 1.795))
                    if self.find_img(target="new_troops_button"):
                        if not self.send_new_troop(preset=preset):
                            breakloop = True
                            break
                        else:
                            sent = True
                            hunters += 1
                    else:
                        self.click(uniform(150, 500), uniform(150, 500))
                    self.better_sleep((1.325, 1.795))

                if self.find_img(target="new_troops_button"):
                    self.close_windows()
        return hunters

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
    def recall(self, nb_troop: int, wait=True) -> bool:
        self.print('Recalling troops')
        # print(nb_troop)
        x, y = uniform(1170, 1183), uniform(160, 175)
        self.click(x, y)
        self.better_sleep((1.595, 2))
        nb_to_go = nb_troop
        breakint = 0
        while nb_to_go > 0:
            co = self.adb.find_multiple_img(target="return_button")
            # print(co)
            while (co is None and co != []) and breakint != 4:
                print(
                    f'[ {current_time()} ] [ {self.name} ] Return button not found')

                y, x = uniform(290, 480), uniform(460, 560)
                x2, y2 = x + uniform(-30, 30), y + uniform(-200, -100)
                self.swipe(x, y, x2, y2)
                self.better_sleep((2, 3))
                co = self.adb.find_multiple_img(target="return_button")
                breakint += 1
            if (co is not None and co != []):
                co = co[0]
                self.click(co[0] + uniform(0, 10), co[1] + uniform(0, 10))
                self.better_sleep((1.695, 2))
                nb_to_go = nb_to_go - 1
            self.better_sleep((1.695, 2))
        sleep(0.5)
        x, y = uniform(1080, 1093), uniform(72, 88)
        self.click(x, y)
        self.better_sleep((1.595, 2))
        if wait:
            said = False
            while self.find_img(target="back_normal_view", confidence=0.9):
                if not said:
                    said = True
                    self.print("Waiting for the troop to come back..")
                sleep(10)

    @get_name
    def nearest_point(self,points):
        dist_min = points[0]
        plus_proche_point = None
        for point in points:
            dist = math.sqrt((point[0] - 200) ** 2 + (point[1] - 200) ** 2)
            if dist < dist_min:
                dist_min = dist
                plus_proche_point = point
        return plus_proche_point
    
    @get_name
    def check_ap_box(self) -> bool:
        self.print(f'Check if AP pop-op box is detected')
        if self.find_img(target="ap_bottle"):
            self.print(f'AP pop-op box Detected')
            if (co:=self.find_img(target="daily_ap_claim")):
                x, y = co[0] + uniform(0, 30), co[1] + uniform(0, 20)
                self.click(x, y)
                self.print("Claiming Free AP","green")
                self.better_sleep((1.325, 1.795))
                self.close_windows()
                if (co := self.find_img('march_bar')):
                    self.click(co[0] + uniform(0, 30), co[1] + uniform(0, 10))
                    self.better_sleep((2, 3))
                return False
            self.close_windows()
            self.click(uniform(700,800),uniform(300,400))
            return True
        self.print(f'AP pop-op box Not detected')
        return False

    @get_name
    def wait_until_kill(self):
        self.print(f"Waiting for the troops to kill the barbarian..")
        while self.find_img(target="troop_idle") is None or self.find_img(target="troop_walking") is not None:
            if not self.adb.is_game_alive():
                self.run_game()
                return self.run(self.end_time)
            if self.check_log_back():
                self.print(
                    "You interrupted killing maraudeurs by connecting from an other device, bot is restarting it")
                return self.run(self.end_time)
            self.script_pause()
            self.check_reconnect()
            self.check_captcha()
            self.better_sleep((8,15))
            print(f"[ {current_time()} ] [ {self.name} ] Waiting for the troops to kill the barbarian..")

    @get_name
    def scan_maraudeur(self):
        """
        Scan device screenshot to find gem node,          not 100% working need improvement
        :return: None
        """
        cos = self.adb.find_multiple_img(target=f"maraudeur_icon", confidence=0.82)
        cos = filter(self.validate_co, cos)
        if not cos:
            return
        co = self.nearest_point(cos)
        default = co
        self.print(f"Maraudeur Found - x: {co[0]} y:{co[1]}")

        self.click(co[0], co[1])
        self.better_sleep((1.3, 2.5))

        self.click(1280 // 2 + uniform(-10, 10), 720 // 2 + uniform(-10, 10))  # Selecting the barbarian
        self.better_sleep((1, 1.4))

        button_attack = self.find_img(target="attack_button")
        if button_attack is None:
            return self.adjusted_leave_city(co[0], co[1])
        self.click(button_attack[0] + uniform(0, 170), button_attack[1] + uniform(0, 40))
        self.better_sleep((1.5, 2))

        self.select_troops()

        co = self.find_img('march_bar')
        self.click(co[0] + uniform(0, 30), co[1] + uniform(0, 10))
        self.better_sleep((2, 3))

        self.print(f'Check if AP pop-op box is detected')
        if self.check_ap_box():
            self.print('Pop-up found, recalling troops')
            self.recall()
            self.block = True
            self.end_time = 0

        self.better_sleep((1, 1.895))
        self.check_captcha()
        return self.adjusted_leave_city(default[0], default[1])

    def select_troops(self):
        if not self.hunter_selection:
            self.print(f'Selecting the whole troops from scratch')
            self.better_sleep((2, 3))
            self.click(uniform(1163, 1180), uniform(670, 685))
            self.better_sleep((2.2, 3.5))
            tab = self.adb.find_multiple_img("selected_icon")
            if tab:
                tab = tab[self.nb_hunter:-1]
                for element in tab:
                    x, y = element[0] + uniform(0, 5), element[1] + uniform(0, 5)
                    self.click(x, y)
                    self.better_sleep((0.3, 0.5))
                self.hunter_selection = True
                self.click(uniform(1163, 1183), uniform(665, 685))
                self.better_sleep((1.2, 1.5))
            else:
                self.hunter_selection = True
        if self.nb_hunter != 1:
            self.print('Selecting all the troops')
            self.click(uniform(1163, 1183), uniform(665, 685))
            self.better_sleep((2, 3))
        else:
            self.print("Selecting the single march..")
            self.click(uniform(1200, 1220), uniform(210, 230))
            self.better_sleep((2, 3))

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
                self.script_pause()
                # string = "input keyevent --longpress 67 67 67 67 67"
                string = "input keyevent 67 67 67 67 67 67"
                self.adb.shell(string)
                self.script_pause()
                self.better_sleep((0.3, 0.5))
                self.adb.shell(
                    f"input text {self.data[str(self.sel)]['schedules'][self.current_profile].get('kingdom')}")
                self.better_sleep((0.3, 0.5))
                self.script_pause()
        self.better_sleep((0.3, 0.5))
        for i in range(2):
            self.click(uniform(590, 685), uniform(130, 150))
            self.better_sleep((0.3, 0.5))
            if i == 0:
                string = f'input text {x2}'
                self.script_pause()
                self.adb.shell(string)
                self.better_sleep((0.3, 0.5))
        self.better_sleep((0.3, 0.5))
        for i in range(2):
            self.click(uniform(750, 830), uniform(130, 150))
            self.better_sleep((0.3, 0.5))
            if i == 0:
                self.script_pause()
                string = f'input text {y2}'
                self.adb.shell(string)
                self.better_sleep((0.3, 0.5))
        self.better_sleep((0.3, 0.5))
        for _ in range(2):
            self.click(uniform(860, 900), uniform(123, 158))
        self.better_sleep((1, 2))
        return randomization

    @get_name
    def swipe_scan(self, scan, direction):
        self.script_pause()
        # print(f'[ {current_time()} ] [ {self.name} ] {direction = } {scan = }')
        direction()
        screen = self.adb.get_cv2_img()

        info_screen = screen[470:700, 0:115]
        cropped_image = screen[420:540, 480:810]

        if random() > 0.7:
            co = self.find_img(source=screen, target="verification_button", confidence=0.8)
            if co is not None:
                self.check_captcha()
            self.check_reconnect(cropped_image)

        if random() > 0.4:
            self.check_download_page(screen)
            self.leave_kd_buff(screen)

        if random() > 0.9:
            self.close_windows()

        cropped_image = screen[616:710, 1168:1270]

        if self.find_img(source=cropped_image, target="map_icon", confidence=0.8) is not None:
            self.click(uniform(500, 700), uniform(250, 450))
            self.better_sleep((1, 2))
            return self.zoom_out_city()

        if self.find_img(source=info_screen, target="hammer", confidence=0.8) is not None:
            self.click(uniform(24, 91), uniform(625, 680))
            self.better_sleep((1.5, 2))
            self.zoom_out_city()
            self.better_sleep((2, 3))

        if self.find_img(source=info_screen, target="gem_search_button", confidence=0.8) is not None:
            self.zoom_out_city()
            self.better_sleep((2, 3))

        self.better_sleep((0.5,0.7))
        return scan()

    @get_name
    def free_troop(self) -> bool:
        """
        :return: True if there's a empty queue
        :return: False if queues are occupied
        """
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image =self.pil_to_array(pil_image)
        cropped_image3 = cv_image[162:179, 1210:1242]
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        # cropped_image1 = cv_image[162:179, 1212:1224]
        # cropped_image2 = cv_image[162:178, 1228:1241]
        # cropped_image3 = cv_image[162:179, 1210:1242]
        # cv_image1 = cv2.cvtColor(cropped_image1, cv2.COLOR_BGR2GRAY)
        # cv_image2 = cv2.cvtColor(cropped_image2, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite("test1.png", cropped_image1)
        # cv2.imwrite("test2.png", cropped_image2)
        # cv2.imwrite("test3.png", cropped_image3)
        native_text = pytesseract.image_to_string(cropped_image3,
                                                  config=r'--oem 1 --psm 13 -c tessedit_char_whitelist=12345670/')
        # text1 = pytesseract.image_to_string(cropped_image1,
        #                                     config=r'--oem 1 --psm 13 -c tessedit_char_whitelist=12345670/')
        # text2 = pytesseract.image_to_string(cropped_image2,
        #                                     config=r'--oem 1 --psm 13 -c tessedit_char_whitelist=12345670/')
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

    @get_class
    def run(self, end_time = None ):
        """
                   Gather gems
                   """
        self.random_macro()
        self.run_game()
        self.check_captcha()
        self.leave_city()
        # print("premier leave city")
        self.better_sleep((1.5, 2))
        self.nb_hunter = self.deploy_hunter()
        self.better_sleep((1.5, 2))
        self.zoom_out_city()
        self.better_sleep((1.5, 2))
        self.scan_maraudeur()
        self.better_sleep((0.125, 0.195))
        randomization = self.go_to(self.data[str(self.sel)]['schedules'][self.current_profile].get('city_x', 500),
                                   self.data[str(self.sel)]['schedules'][self.current_profile].get('city_y', 500))
        # print(f"{randomization = }")
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


        if self.end_time is None:
            self.end_time = starting_time + (
                    randint(
                        self.data[str(self.sel)]['schedules'][self.current_profile].get('gather_gem_duration1'),
                        self.data[str(self.sel)]['schedules'][self.current_profile].get('gather_gem_duration2')
                    ) * 60
            )

        # print(f'starting_time : {datetime.fromtimestamp(starting_time).strftime("%H:%M:%S")} , time to beat : {datetime.fromtimestamp(end_time).strftime("%H:%M:%S")} , {starting_time>end_time = }')
        self.print(f"Killing marauders till around : {datetime.fromtimestamp(self.end_time).strftime('%H:%M:%S')}")
        while self.end_time > time():
            self.run_game()
            self.scan_maraudeur()
            self.check_reconnect()
            self.check_log_back()
            self.check_captcha(False)
            self.leave_kd_buff()

            # print("test")
            if randomization == 0:
                for y in range(width - 1):

                    for i in range(width):
                        if self.end_time < time(): return self.recall()
                        if self.block: return self.recall()
                        self.swipe_scan(self.scan_maraudeur, self.swipe_right)

                    self.swipe_scan(self.scan_maraudeur, self.swipe_down)
                    self.check_captcha(False)
                    self.leave_kd_buff()

                    for i in range(width):
                        if self.end_time < time(): return self.recall()
                        if self.block: return self.recall()
                        self.swipe_scan(self.scan_maraudeur, self.swipe_left)

                    self.check_captcha(False)
                    self.leave_kd_buff()

                    if y != (width - 2):
                        if self.end_time < time(): return self.recall()
                        if self.block: return self.recall()
                        self.swipe_scan(self.scan_maraudeur, self.swipe_down)

            if randomization == 2:
                for y in range(width - 1):

                    for i in range(width):
                        if self.end_time < time(): return self.recall()
                        if self.block: return self.recall()
                        self.swipe_scan(self.scan_maraudeur, self.swipe_left)

                    self.swipe_scan(self.scan_maraudeur, self.swipe_up)
                    self.check_captcha(False)
                    self.leave_kd_buff()

                    for i in range(width):
                        if self.end_time < time(): return self.recall()
                        if self.block: return self.recall()
                        self.swipe_scan(self.scan_maraudeur, self.swipe_right)

                    self.check_captcha(False)
                    self.leave_kd_buff()

                    if y != (width - 2):
                        if self.end_time < time(): return self.recall()
                        if self.block: return self.recall()
                        self.swipe_scan(self.scan_maraudeur, self.swipe_up)

            if randomization == 1:
                for y in range(height - 1):

                    for i in range(height):
                        if self.end_time < time(): return self.recall()
                        if self.block: return self.recall()
                        self.swipe_scan(self.scan_maraudeur, self.swipe_down)

                    self.swipe_scan(self.scan_maraudeur, self.swipe_left)
                    self.check_captcha(False)
                    self.leave_kd_buff()
                    if self.end_time < time():return self.recall()

                    for i in range(height):
                        if self.end_time < time(): return self.recall()
                        if self.block: return self.recall()
                        self.swipe_scan(self.scan_maraudeur, self.swipe_up)

                    self.check_captcha(False)
                    self.leave_kd_buff()

                    if y != (height - 2):
                        self.swipe_scan(self.scan_maraudeur, self.swipe_left)

            if randomization == 3:
                for y in range(height - 1):
                    for i in range(height):
                        if self.end_time < time(): return self.recall()
                        if self.block: return self.recall()
                        self.swipe_scan(self.scan_maraudeur, self.swipe_up)

                    self.swipe_scan(self.scan_maraudeur, self.swipe_right)
                    if self.end_time < time(): return self.recall()
                    self.check_captcha(False)
                    self.leave_kd_buff()

                    for i in range(height):
                        if self.end_time < time(): return self.recall()
                        if self.block: return self.recall()
                        self.swipe_scan(self.scan_maraudeur, self.swipe_down)
                    self.check_captcha(False)
                    self.leave_kd_buff()
                    if y != (height - 2):
                        self.swipe_scan(self.scan_maraudeur, self.swipe_right)

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
        self.print("Maraudeurs time elapsed !")
