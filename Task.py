import json
import logging
import os
import sys
import traceback
from random import uniform, randint
from time import sleep

import cv2
from PIL import Image
from numpy import array

import verification

from Task_utils import get_window_pid, get_name, current_time, get_time
from twocaptcha import TwoCaptcha



class Task:
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
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a", )
        # self.adb.connect_to_device()
        a = self.adb.is_game_alive()
        if a:
            self.print(f"Looks like game is running ")
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
        logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s",
                            datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
        print(f"[ {current_time()} ] [ {self.name} ] Resolve count = {compteur}")
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
            logging.info(f"[{self.name}] Exception raised during the resolving of the captcha (task.py related) :\n{e}")
            self.click(uniform(507, 533), uniform(573, 599))
            self.print("Refreshing the captcha.")
            self.better_sleep((4, 7))
            return self.resolve_captcha(compteur=compteur + 1)

    def script_pause(self):
        said = False
        while self.frame.pause and not self.frame.pr_tasks_button.cget("fg_color") == "white":
            if not said:
                print(f"[ {current_time()} ] [ {self.name} ] Script is paused.")
                logging.info(f"[{self.name}] Script is paused.")
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
            if self.adb.find_img(target="menu_button", confidence=0.8) or \
                    self.adb.find_img(target="map_icon", confidence=0.8) or \
                    self.adb.find_img(target="hammer", confidence=0.8):
                condition = False
            co = self.adb.find_img(target="mightiest_gov", confidence=0.8)
            if co is not None:
                self.click(uniform(co[0] + 5, co[0] + 20), uniform(co[1] + 5, co[1] + 20))
                condition = False
            self.better_sleep((10, 15))
            self.check_reconnect()

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
            sys.exit(0)

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

    @get_name
    def leave_game(self, force=False) -> None:
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
    def check_download_page(self, screen=None):
        if screen is None:
            if self.adb.find_img(target="download_page", confidence=0.9):
                self.adb.click(uniform(1018, 1041), uniform(127, 146))
                self.better_sleep((1.925, 2.795))
        else:
            if self.adb.find_img(target="download_page", source=screen, confidence=0.9):
                self.adb.click(uniform(1018, 1041), uniform(127, 146))
                self.better_sleep((1.925, 2.795))

    def set_current_task(self, name):
        if name == 'ClaimCampaign':
            return self.set_status("Claiming campaign rewards")
        if name == 'CollectResource':
            return self.set_status("Collecting city rss")
        if name == 'BuyMerchant':
            return self.set_status("Buying merchant..")
        if name == 'GatherRss':
            return self.set_status("Gathering rss")
        if name == 'UseEnhancedBuff':
            return self.set_status("Enabling enhanced buffs")
        if name == 'AllianceDonation':
            return self.set_status("Donating to alliance")
        if name == 'HuntBarbarians':
            return self.set_status("Killing barbarians")
        if name == 'GatherGem':
            return self.set_status("Gathering gems")
        if name == 'ClearFog':
            return self.set_status("Exploring fog")
        if name == 'DailyVip':
            return self.set_status("Daily VIP rewards")
        if name == 'DailyChest':
            return self.set_status("Daily Chest rewards")
        if name == 'BarbarianFort':
            return self.set_status("Launching fort")
        if name == 'HealTroop':
            return self.set_status("Healing troops")
        if name == 'ProduceMaterials':
            return self.set_status("Producing materials")

    def get_current_task(self, name):
        if name == 'ClaimCampaign':
            return "Claiming campaign rewards"
        if name == 'CollectResource':
            return "Collecting city rss"
        if name == 'BuyMerchant':
            return "Buying merchant.."
        if name == 'GatherRss':
            return "Gathering rss"
        if name == 'UseEnhancedBuff':
            return "Enabling enhanced buffs"
        if name == 'AllianceDonation':
            return "Donating to alliance"
        if name == 'HuntBarbarians':
            return "Killing barbarians"
        if name == 'GatherGem':
            return "Gathering gems"
        if name == 'ClearFog':
            return "Exploring fog"
        if name == 'DailyVip':
            return "Daily VIP rewards"
        if name == 'DailyChest':
            return "Daily Chest rewards"
        if name == 'BarbarianFort':
            return "Launching fort"
        if name == 'HealTroop':
            return "Healing troops"
        if name == 'ProduceMaterials':
            return "Producing materials"

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

    # def execute_tasks(self, lib_tasks):
    #     co = self.adb.find_img(target="hide_quests")
    #     if co is not None:
    #         self.click(co[0] + uniform(0, 20), co[1] + uniform(0, 20))
    #     self.check_download_page()
    #     current_task = 1
    #     for func in lib_tasks:
    #         self.check_download_page()
    #         self.leave_kd_buff()
    #         self.print(f"----- Task {current_task}/{len(lib_tasks)} -----".center(60))
    #         self.print(f"Currently executing : {self.get_current_task(func.task_name())}")
    #         self.set_current_task(func.task_name())
    #         self.run_game()
    #         self.check_log_back()
    #         self.check_reconnect()
    #         self.check_resolve()
    #         # self.set_status()
    #         if func.task_name() in ["AllianceDonation", "CollectResource", "BuyMerchant", "ClearFog", "HealTroop",
    #                              "DailyChest"]:
    #             self.go_city()
    #         try:
    #             # print(f"{ func.__name__ in ['gather_rss','gather_gem'] =}")
    #             if func.__name__ in ["GatherRss", "GatherGem"]:
    #                 pil_image = self.adb.get_curr_device_screen_img()
    #                 cv_image = np.array(pil_image)
    #                 cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    #                 cv_image = cv_image[0:100, 0:800]
    #                 # print(f'{self.adb.find_img_src_conf(cv_image,"block_icon",0.90)=}')
    #                 if self.adb.find_img(target="block_icon", source=cv_image, confidence=0.90) is None:
    #                     func.run()
    #             else:
    #                 func.run()
    #             self.better_sleep((1, 2))
    #         except Exception as e:
    #             self.print(f"Exception during {func.task_name()}")
    #             exception = traceback.format_exc()
    #             self.print(f"{exception}")
    #             self.leave_game()
    #             self.better_sleep((5, 10))
    #             self.run_game()
    #         self.better_sleep((0.795, 1.2))
    #         current_task += 1
    #         if ('BuyMerchant' in func.task_name()) or ('GatherRss' in func.task_name()):
    #             self.check_resolve()
    #             self.better_sleep((0.795, 1.2))

    # @get_name
    # def get_first_character(self) -> tuple[float, float]:
    #     logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO,
    #                         format="%(asctime)s %(message)s",
    #                         datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
    #     self.print("Switching Character")
    #     self.set_status(f"Switching Character")
    #     x, y = uniform(15, 80), uniform(10, 60)
    #     self.click(x, y)
    #     self.better_sleep((1.925, 2.795))
    #     x, y = uniform(950, 1015), uniform(510, 560)
    #     self.click(x, y)
    #     self.better_sleep((1.925, 2.795))
    #     x, y = uniform(315, 380), uniform(330, 400)
    #     self.click(x, y)
    #     self.better_sleep((4, 5.795))
    #     trigger_stop = 0
    #     while self.adb.find_img(target="logged_icon") is None:
    #         self.check_resolve()
    #         print(
    #             f'[ {current_time()} ] [ {self.name} ] while get_first_character')
    #         y, x = uniform(290, 480), uniform(460, 560)
    #         x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)
    #         self.swipe(x, y, x2, y2)
    #         self.better_sleep((1.925, 2.795))
    #         trigger_stop += 1
    #         if trigger_stop > 4:
    #             self.print("Error in character switch. Bot is now stopped")
    #             self.set_status("Error.")
    #             while True:
    #                 self.script_pause()
    #                 sleep(1)
    #     x, y = self.adb.find_img(target="logged_icon")
    #     co = self.adb.find_img(target="logged_icon")
    #     self.print("Current character detected.")
    #     if x < 1280 // 2:
    #         x2 = x + uniform(480, 780)
    #         y2 = y + uniform(-20, 0)
    #         self.click(x2, y2)
    #         self.better_sleep((2.425, 2.795))
    #     elif y > 520 and x > 1280 // 2:
    #         y, x = uniform(290, 480), uniform(460, 560)
    #         x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)
    #         self.swipe(x, y, x2, y2)
    #         self.better_sleep((2.425, 2.795))
    #         x, y = self.adb.find_img(target="logged_icon")
    #         self.better_sleep((2.025, 2.795))
    #         x2 = x - uniform(100, 320)
    #         y2 = y + uniform(80, 100)
    #         self.click(x2, y2)
    #         self.better_sleep((2.425, 2.795))
    #     elif x > 1280 // 2:
    #         x2 = x - uniform(100, 320)
    #         y2 = y + uniform(80, 100)
    #         self.click(x2, y2)
    #         self.better_sleep((2.425, 2.795))
    #         # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] test login" + str(
    #         #     self.adb.find_img(target="character_login_confirm")))
    #         # print(f'[ {current_time()} ] [ {self.name} ] TEST Login')
    #     self.better_sleep((2.425, 2.795))
    #     # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] character login" + str(
    #     #     self.adb.find_img(target="character_login_confirm")))
    #     if self.adb.find_img(target="character_login_confirm") is not None:
    #         self.print("Switching between character")
    #         x, y = uniform(700, 900), uniform(490, 527)
    #         self.click(x, y)
    #         # self.better_sleep((10, 15))
    #         # self.check_crash()
    #         # self.run_game()
    #         return co[0] + uniform(0, 5), co[1] + uniform(0, 5),
    #     else:
    #         self.print("No more characters, going back to the first character")
    #         x, y = uniform(400, 800), uniform(200, 250)
    #         x2, y2 = x + uniform(-20, 20), uniform(580, 645)
    #         self.swipe(x, y, x2, y2)
    #         self.better_sleep((3.5, 4.7))
    #         x, y = uniform(660, 1000), uniform(215, 280)
    #         self.click(x, y)
    #         self.better_sleep((1.8, 2.7))
    #         x, y = uniform(700, 910), uniform(491, 522)
    #         self.click(x, y)
    #         return uniform(660, 1000), uniform(215, 280)
    #
    # @get_name
    # def enter_profile(self):
    #     self.click(uniform(28, 64), uniform(24, 52))
    #     self.better_sleep((1.925, 2.795))
    #
    # @get_name
    # def enter_setting(self):
    #     self.click(uniform(957, 1000), uniform(511, 554))
    #     self.better_sleep((1.925, 2.795))
    #
    # @get_name
    # def enter_characters(self):
    #     self.click(uniform(312, 374), uniform(333, 400))
    #     self.better_sleep((4, 6))
    #
    # @get_name
    # def change_character_param(self, co_first, nb_chars=0):
    #     self.print("Switching Character")
    #     self.set_status(f"Switching Character")
    #     deadstop = 0
    #     self.enter_profile()
    #     self.enter_setting()
    #     self.enter_characters()
    #     while self.adb.find_img(target="logged_icon") is None:
    #         if deadstop == 5:
    #             self.print(f"Error in character switch. Bot is now stopped")
    #             self.set_status("Error.")
    #             while True:
    #                 self.script_pause()
    #                 sleep(1)
    #         self.check_resolve()
    #         y1, x1 = uniform(290, 480), uniform(460, 560)
    #         x2, y2 = x1 + uniform(-30, 30), y1 + uniform(-100, -50)
    #         self.swipe(x1, y1, x2, y2)
    #         self.better_sleep((1.925, 2.795))
    #         deadstop = deadstop + 1
    #     x, y = self.adb.find_img(target="logged_icon")
    #     self.print('Current character detected.')
    #     if x < 1280 // 2:
    #         self.print(f"x < 1280 // 2")
    #         self.click(x + uniform(480, 780), y + uniform(-20, 0))
    #         self.better_sleep((2.425, 2.795))
    #     elif y > 520 and x > 1280 // 2:
    #         self.print("y > 520 and x > 1280 // 2")
    #         y, x = uniform(290, 480), uniform(460, 560)
    #         x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)
    #         self.swipe(x, y, x2, y2)
    #         self.better_sleep((2.425, 2.795))
    #         x, y = self.adb.find_img(target="logged_icon")
    #         self.better_sleep((2.025, 2.795))
    #         self.click(x - uniform(100, 320), y + uniform(80, 100))
    #         self.better_sleep((2.425, 2.795))
    #     elif x > 1280 // 2:
    #         self.print("x > 1280 // 2")
    #         self.click(x - uniform(100, 320), y + uniform(80, 100))
    #         self.better_sleep((2.425, 2.795))
    #     self.better_sleep((3.425, 3.995))
    #     if self.adb.find_img(target="character_login_confirm") is not None:
    #         self.print("Switching to the next character")
    #         self.click(uniform(700, 900), uniform(490, 527))
    #         return True
    #     else:
    #         self.print("No more characters, going back to the first character")
    #         x, y = uniform(400, 800), uniform(200, 250)
    #         if nb_chars // 6 == 0:
    #             rounds = 1
    #         else:
    #             rounds = nb_chars // 6
    #         if rounds == 0:
    #             rounds = +1
    #         for _ in range(rounds):
    #             x2, y2 = x + uniform(-20, 20), uniform(580, 645)
    #             self.swipe(x, y, x2, y2)
    #             self.better_sleep((3.5, 4.7))
    #         self.click(co_first[0] + uniform(30, 300), co_first[1] + uniform(-30, 0))
    #         self.better_sleep((1.8, 2.7))
    #         x, y = uniform(700, 910), uniform(491, 522)
    #         self.click(x, y)
    #         return False
    #
    # @get_name
    # def routine_scheduled(self):
    #     self.adb.connect_to_device()
    #     self.data = self.update_data()
    #
    #     loop_task = 1 if not self.data.get(self.sel).get("loop_task") else 9999999999999
    #
    #     starting_time = time()
    #     for i in range(loop_task):
    #         loop_time = time()
    #         self.set_status("Starting..")
    #         self.print(" Script is starting ! ".center(56, "-"))
    #         self.data = self.update_data()
    #         for profile in self.data[self.sel]['schedules']:
    #             if self.data[self.sel]['schedules'][profile]['enabled']:
    #                 self.current_profile = profile
    #                 self.print(f" Profile n°{profile} enabled ! ".center(60))
    #                 if self.data.get(self.sel).get('schedules').get(self.current_profile).get("switch_character"):
    #                     self.print(f"---- Character n°1 ----".center(60))
    #                 self.run_game()
    #                 self.check_log_back()
    #                 self.check_reconnect()
    #                 self.leave_kd_buff()
    #                 self.check_mge()
    #                 self.check_resolve()
    #                 # First character
    #                 self.execute_tasks(self.get_available_task(profile))
    #                 if self.data.get(self.sel).get('schedules').get(self.current_profile).get("switch_character",
    #                                                                                           False):
    #                     co_first = self.get_first_character()
    #                     boolean = True
    #                     self.wait_until_connected()
    #
    #                     self.run_game()
    #                     # Characters remaining
    #                     nb_characters = 2
    #                     while boolean:
    #                         self.print(f"---- Character n°{nb_characters} ----".center(60))
    #                         self.run_game()
    #                         self.check_resolve()
    #                         self.check_mge()
    #
    #                         self.execute_tasks(self.get_available_task(profile))
    #                         self.better_sleep((2.2, 4))
    #
    #                         nb_characters += 1
    #                         boolean = self.change_character_param(co_first, nb_characters)
    #                         self.wait_until_connected()
    #                 if not self.data[self.sel]['scheduler']:
    #                     break
    #
    #         if self.data.get(self.sel).get("loop_task"):
    #             ttw1, ttw2 = self.data.get(self.sel).get("time_to_wait_loop1", 60), self.data.get(self.sel).get(
    #                 "time_to_wait_loop2", 90)
    #             self.print(f"Run nb°{i} took {(time() - loop_time) / 60:0.1f} minutes to complete.")
    #             if ttw1 > ttw2:
    #                 ttw1, ttw2 = ttw2, ttw1
    #             time_before_redo_tasks = int(randint(ttw1, ttw2) * 60) + randint(0, 60)
    #             self.print(f"Script is paused for {time_before_redo_tasks / 60:0.1f} minutes")
    #             self.set_status((datetime.fromtimestamp(time_before_redo_tasks) - timedelta(hours=1)).strftime("%H:%M:%S"))
    #             if self.data.get(self.sel).get("leave_game_loop", False):
    #                 if time_before_redo_tasks < 600:
    #                     self.leave_game(force=True)
    #                 else:
    #                     self.leave_game(force=False)
    #
    #             for _ in range(time_before_redo_tasks):
    #                 self.script_pause()
    #                 sleep(1)
    #
    #     self.print(f"The bot took {(time() - starting_time) // 60} minutes to complete all the tasks, bot is waiting for your instructions.")
    #     return

    def status(self, text):
        self.frame.update_label2(self.sel, text)
