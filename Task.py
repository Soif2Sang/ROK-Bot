import json
import logging
import os
import subprocess
import sys
import traceback
from datetime import date
from random import uniform, randint
from time import sleep

import cv2
from PIL import Image
from numpy import array

import verification

from Task_utils import get_window_pid, get_name, current_time, get_time
from bot_adb import Adb
from twocaptcha import TwoCaptcha



class Task:
    def __init__(self, frame):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.current_profile = '1'
        self.frame = frame
        self.sel = frame.sel
        self.adb = Adb(self.sel)
        # self.adb.connect_to_device()
        self.ppid = os.getppid()
        self.pid = get_window_pid(self.adb.name)
        self.language = None
        self.name = self.adb.name
        self.resource_type = None

    def set_text(self, text):
        self.frame.write(text)

    def set_status(self, text):
        self.frame.update_label2(self.sel, text)

    @get_name
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

    @get_name
    def print(self, text: str) -> None:
        # print(f'[ {current_time()} ] [ {self.name} ] {text}')
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
    def run_game(self, count=0) -> None:
        # self.adb.connect_to_device()
        a = self.adb.is_game_alive()
        if not a:
            self.print(f"Looks like game is not running ")
            co = self.adb.find_img(target="rokicon", confidence=0.8)
            print(f"{co =}")
            if co is not None:
                self.click(co[0] + 10, co[1] + 10)
                sleep(3)
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
                            with open(f"{self.name}_logs.txt", "a+", encoding="utf-8") as logger:
                                logger.write(f"[ {date.today()} ] [ {current_time()} ] [ {self.name} ] INFO : [{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }\n")
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
                            with open(f"{self.name}_logs.txt", "a+", encoding="utf-8") as logger:
                                logger.write(
                                    f"[ {date.today()} ] [ {current_time()} ] [ {self.name} ] INFO : [{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }\n")
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
                            with open(f"{self.name}_logs.txt", "a+", encoding="utf-8") as logger:
                                logger.write(
                                    f"[ {date.today()} ] [ {current_time()} ] [ {self.name} ] INFO : [{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }\n")
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
    def resolve_captcha(self, compteur=0):
        """
        Resolve verification
        """
        self.print(f"Resolve count = {compteur}")
        if compteur > 5:
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
            size = os.path.getsize(rf"{os.getcwd()}\captcha{self.sel}.jpg")
            if size > 99999:
                self.print(f"Captcha is too big ({size}), refreshing it..")
                self.adb.click(uniform(508, 532), uniform(580, 596))
                self.better_sleep((4, 7))
                return self.resolve_captcha(compteur + 1)
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
            traceback.print_exc()
            print(f"[ {current_time()} ] [ {self.name} ] Exception raised during the resolving of the captcha (task.py related) :\n{e}")
            with open(f"{self.name}_logs.txt", "a+", encoding="utf-8") as logger:
                logger.write(
                    f"[ {date.today()} ] [ {current_time()} ] [ {self.name} ] EXCEPTION : Exception raised during the resolving of the captcha (task.py related) :\n{e}\n")
            self.click(uniform(507, 533), uniform(573, 599))
            self.print("Refreshing the captcha.")
            self.better_sleep((4, 7))
            return self.resolve_captcha(compteur=compteur + 1)

    def script_pause(self):
        said = False
        while self.frame.pause and not self.frame.pr_tasks_button.cget("fg_color") == "white":
            if not said:
                print(f"[ {date.today()} ] [ {current_time()} ] [ {self.name} ] Script is paused.")
                self.set_text(f"[{current_time()}] Script is paused.")
                said = True
                # self.set_text("Script paused.")
            sleep(1)

        if self.frame.stop:
            print(self.frame.stop)
            print(self.frame.end_tasks_button.cget("state"))
            self.frame.stop = False
            sys.exit(1)
    @get_name
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
                for i in range(value):
                    self.script_pause()
                    sleep(1)
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
    def wait_until_connected(self) -> None:
        self.print("Script is paused until game is fully loaded..")
        condition = True
        while condition:
            self.run_game()
            if self.adb.find_img(target="menu_button", confidence=0.8) or \
                    self.adb.find_img(target="map_icon", confidence=0.8) or \
                    self.adb.find_img(target="hammer", confidence=0.8) or \
                    self.adb.find_img(target="inbox", confidence=0.8):
                condition = False
            co = self.adb.find_img(target="mightiest_gov", confidence=0.8)
            if co is not None:
                self.click(uniform(co[0] + 5, co[0] + 20), uniform(co[1] + 5, co[1] + 20))
                condition = False
            self.better_sleep((10, 15))
            self.check_reconnect()
            self.check_log_back()

    @get_name
    def leave_kd_buff(self, Source=None):

        co = self.adb.find_img(target="kingdom_buff", source=Source)
        if co is not None:
            self.click(uniform(70, 270), uniform(100, 542))
            self.better_sleep((1.8, 3))

    @get_name
    def check_if_kill(self):
        return
        """
        Kill the process if his ppid is dead
        :exemple: leave python would kill the process
        """
        if not pid_exists(self.ppid):
            self.print("pPid not found, killing the thread")
            sys.exit(0)
    #
    # @get_name
    # def start_emulator(self) -> None:
    #     with open('path.json', encoding='utf-8') as config_file:
    #         path = json.load(config_file)
    #     self.data = self.update_data()
    #     cmd = f'{path["HD-Player"]} --instance {self.data.get(self.sel).get("instance")}'
    #     self.print("cmd")
    #     subprocess.Popen(cmd)
    #     # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] {cmd}')
    #     # os.system(cmd)
    #
    # @get_name
    # def kill_emulator(self) -> None:
    #     self.data = self.update_data()
    #     print(self.adb.name)
    #     self.pid = get_window_pid(self.adb.name)
    #     cmd = f"taskkill /PID {self.pid} /F"
    #     subprocess.Popen(cmd)

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
            if self.adb.find_img(target="close_refresh_ok", confidence=0.75) is None:
                resolved = True
            if i == 5:
                self.print("Error, unable to resolve the captcha for 5 times in a row !")
                return False
            self.report_feedback(captchaId, resolved, solver)
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

    @get_name
    def leave_game(self, force=False) -> None:
        """
        Send adb signal to leave application
        """
        self.print(f"Leaving the game..")
        self.adb.get_device().shell("input keyevent KEYCODE_APP_SWITCH")
        sleep(2)
        self.click(920,62)
        sleep(2)

    @get_name
    def kill_game(self) -> None:
        self.adb.get_device().shell("am force-stop com.lilithgame.roc.gp")
        self.adb.get_device().shell("am force-stop com.rok.gp.vn")
        self.adb.get_device().shell("am force-stop com.lilithgame.rok.gpkr")
        self.adb.get_device().shell("am force-stop com.lilithgames.rok.gpkr")

    @get_name
    def check_download_page(self, screen=None):
        if screen is None:
            if self.adb.find_img(target="download_page", confidence=0.9):
                self.adb.click(uniform(1018, 1041), uniform(127, 146))
                self.better_sleep((1.925, 2.795))
        else:
            if self.adb.find_img(target="download_page", source=screen, confidence=0.9):
                self.adb.click(uniform(1018, 1041), uniform(127, 146))
                self.better_sleep((1.925, 2.795))

    @get_name
    def go_city(self):
        if not self.in_city():
            x = uniform(24, 91)
            y = uniform(625, 680)
            self.click(x, y)
            self.better_sleep((1.5, 2))

    @get_name
    def in_city(self) -> bool:
        """
        Check if the current view is set in the city
        :return: True if in city, False if not
        """
        return self.adb.find_img(target='gem_search_button') is None

    def status(self, text):
        self.frame.update_label2(self.sel, text)
