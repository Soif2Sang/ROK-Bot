import os
import sys
import traceback
from datetime import date
from random import uniform, randint
from time import sleep
from psutil import pid_exists
import cv2
from PIL import Image, ImageFile
from numpy import array, ndarray

from utils import discord_bot
from utils.Task_utils import get_window_pid, get_name, current_time, get_time, get_data, write, string_to_co
from utils.bot_adb import Adb
from utils.twocaptcha import TwoCaptcha
ImageFile.LOAD_TRUNCATED_IMAGES = True


class Task:
    def __init__(self, tile):
        self.data = get_data()
        self.current_profile = '1'
        self.tile = tile
        self.sel = tile.number
        # print(self.sel)
        self.adb = Adb(self.sel)
        # print(self.sel)
        self.ppid = os.getppid()
        self.pid = get_window_pid(self.adb.name)
        self.language = None
        self.name = self.adb.name

    def set_text(self, text, color=None):
        return self.tile.add_text(text,color)

    def set_status(self, text):
        return self.tile.set_text(text)

    def set_timer(self, seconds:int):
        condition = True
        while seconds and condition:
            self.script_pause()
            hours, mins = divmod(seconds, 3600)
            mins, secs = divmod(mins, 60)
            self.set_status(f"{hours:02d}:{mins:02d}:{secs:02d}")
            sleep(1)
            seconds -= 1
            condition = ":" in self.tile.text_status.value and self.tile.text_status.value != "00:00:01"

    @get_name
    def update_data(self):
        self.data = get_data()
        return self.data

    def set_sel(self, sel) -> None:
        self.data = self.update_data()
        self.sel = sel
        self.name = self.data.get(self.sel).get('name', "Name not found")

    @get_name
    def print(self, text: str, color=None) -> None:
        # print(f'[ {current_time()} ] [ {self.name} ] {text}')
        if text != "":
            self.set_text(f"[{current_time()}] {text}",color)
        else:
            self.set_text("")

    @get_name
    def send_discord_message(self, message):
        if self.data["discord"]["user_id"] and self.data["discord"]["enabled"]:
            return discord_bot.send_message(self.data["discord"]["user_id"], f"[{current_time()}] {message}")

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
    def find_img(self,target:str, source:  ndarray = None, confidence=0.9):
        # self.print(f"Loading {target}")
        # print(f"[ {date.today()} {current_time()} ] [ {self.name} ] Loading {target}")
        result = self.adb.find_img(target=target,source=source,confidence=confidence)
        # self.print(f"Successfully loaded {target}")
        # print(f"[ {date.today()} {current_time()} ] [ {self.name} ] Successfully loaded {target}")

        return result 
    
    @get_name
    def run_game(self, count=0) -> None:
        # print(self.adb.is_game_alive())
        a = self.adb.is_game_alive()
        if not a:
            self.print(f"Looks like game is not running")
            co = self.find_img(target="rokicon", confidence=0.8)
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
                            string = self.adb.shell("am start -n com.lilithgame.roc.gp/com.harry.engine.MainActivity")
                            write(self.name,f"INFO : [{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }\n")
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
                            string = self.adb.shell("am start -n com.rok.gp.vn/com.harry.engine.MainActivity")
                            write(self.name,f"INFO : [{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }\n")
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
                            string = self.adb.shell(
                                "am start -n com.lilithgame.rok.gpkr/com.harry.engine.MainActivity")
                            write(self.name,f"INFO : [{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }\n")
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
                self.send_discord_message("ERROR CANNOT START THE GAME.")
                while True:
                    self.set_status("ERROR CANNOT START GAME")
                    self.script_pause()
                    sleep(1)

    @get_name
    def better_sleep(self, limits: tuple[float, float]):
        a = limits[0]
        b = limits[1]
        if self.data[str(self.sel)]['schedules'][self.current_profile]["slow_mode"]:
            # self.set_text(tuple,tuple[0])
            a = a * self.data[str(self.sel)]['schedules'][self.current_profile]["sleep_multiplicator"]
            b = b * self.data[str(self.sel)]['schedules'][self.current_profile]["sleep_multiplicator"]
        sleep(uniform(a, b))

    @get_name
    def solve(self,path, sel, defaultApiKey=True):
        # print(sel, type(sel))
        if defaultApiKey:
            api_key = '4805a29997857b110ef26530c7f39db1'
        else:
            api_key = self.data[sel]['API_KEY']
            if api_key == "":
                return self.print("This feature require a custom ApiKey")

        solver = TwoCaptcha(api_key, defaultTimeout=120, pollingInterval=5)
        try:
            self.print("Trying to resolve the captcha")
            result = solver.coordinates(path, lang='en')
            self.print(f"{result = }\n")
            return result
        except Exception as e:
            if e == 'ERROR_CAPTCHA_UNSOLVABLE':
                if self.refresh_captcha():
                    return self.check_captcha()

            self.print(f"EXCEPTION : Exception raised during the resolving of the captcha :\n{e}\n","red")
            return {'error':e}

    @get_name
    def resolve_captcha(self, compteur=0 , defaultApiKey=True):
        """
        Resolve verification
        """
        self.print(f"Resolve count = {compteur}")
        if compteur > 5:
            self.print("Error in resolving the captcha, human action needed.")
            self.set_status("Error")
            self.send_discord_message("Error in resolving the captcha, human action required.")
            while True:
                self.script_pause()
                sleep(1)
        try:
            if defaultApiKey:
                api_key = '4805a29997857b110ef26530c7f39db1'
            else:
                api_key = self.data[self.sel]['API_KEY']
                if api_key == "":
                    return self.print("This feature require a custom ApiKey")

            self.print("Trying to resolve the captcha")

            captcha = self.save_captcha()
            solver = TwoCaptcha(api_key, defaultTimeout=120, pollingInterval=5)

            result = solver.coordinates(f"captcha{self.sel}.jpg", lang='en')

            print(result)

            co = string_to_co(result['code'])
            if self.adb.find_img_cv(captcha) is not None:
                for x, y in co:
                    self.click(x, y)
                    self.better_sleep((0.4, 0.795))
                self.click(uniform(700, 830), uniform(570, 600))
                self.better_sleep((1, 1.795))

            return result['captchaId']
        except Exception as e:
            traceback.print_exc()
            print(f"[ {current_time()} ] [ {self.name} ] Exception raised during the resolving of the captcha (task.py related) :\n{e}")
            write(self.name,f"EXCEPTION : Exception raised during the resolving of the captcha (task.py related) :\n{e}\n")

            if e == 'ERROR_CAPTCHA_UNSOLVABLE':
                if self.refresh_captcha():
                    return self.resolve_captcha()
                else:
                    return None
            self.refresh_captcha()
            self.print("Refreshing the captcha.","red")
            self.better_sleep((4, 7))
            return self.resolve_captcha(compteur=compteur + 1)

    def save_captcha(self):
        pil_image = self.adb.get_curr_device_screen_img()
        try:
            cv_image = array(pil_image)
        except OSError:
            sleep(1)

            return self.save_captcha()
        cropped_image = cv_image[100:560, 440:840]
        cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(cropped_image)
        im_pil.save(f"captcha{self.sel}.jpg", optimize=True, quality=80)
        sleep(0.5)
        size = os.path.getsize(rf"{os.getcwd()}\captcha{self.sel}.jpg")
        if size > 99999:
            self.print(f"Captcha is too big ({size}), refreshing it..")
            self.refresh_captcha()
            return self.save_captcha()
        return cropped_image


    def refresh_captcha(self):
        co = self.find_img(target="refresh_resolve", confidence=0.9)
        # print(f"{co = }")
        if co is not None:
            x, y = co[0] + 3, co[1] + 3
            self.click(x, y)
            self.better_sleep((2, 3))
            return True
        return False


    def script_pause(self):
        said = False

        if self.tile.stopped:
            self.tile.stopped = False
            self.set_text(f"[{current_time()}] You stopped the bot","Red")
            print(f"[ {date.today()} {current_time()} ] [ {self.name} ] You stopped the bot")
            sys.exit(1)

        while not self.tile.started:
            if not said:
                # self.print(f"You is paused.","Yellow")
                self.set_text(f"[{current_time()}] Script is paused.","orange")
                print(f"[ {date.today()} {current_time()} ] [ {self.name} ] Script is paused.")
                said = True
                # self.set_text("Script paused.")
        if said:
            self.set_text(f"[{current_time()}] You resumed the script.","Green")
            print(f"[ {date.today()} {current_time()} ] [ {self.name} ] You resumed the script.")

    @get_name
    def check_log_back(self, cv_image=None):
        # self.data = self.update_data()
        # print(f'{self.data.get(self.sel).get("auto_log_back"] =}')
        if cv_image is None:
            cv_image = self.adb.get_cv2_img()
            # print(f'{co}')
        co = self.find_img(source=cv_image, target="already_connected", confidence=0.9)
        if co is not None:
            co = self.find_img(source=cv_image, target="reconnect", confidence=0.9)
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
                                    'log_back2') * 60) + randint(0,59)
                self.print(f"Waiting for the timer to end.. {value / 60:0.1f} minutes")
                for i in range(value):
                    self.script_pause()
                    sleep(1)
                self.click(co[0] + uniform(0, 50), co[1] + uniform(-10, 20))
                self.print("Reconnection..")
                sleep(uniform(5, 10))
                self.run_game()
                return True
            else:
                self.set_text("Auto Log-back off","red")
                self.send_discord_message("The game got disconnected, Log-back off.")
                while True:
                    self.script_pause()
                    sleep(1)
        else:
            return False

    @get_name
    def check_mge(self, cv_image = None):
        if cv_image is None:
            cv_image = self.adb.get_cv2_img()
        co = self.find_img(target="mightiest_gov",source=cv_image)
        if co is not None:
            self.click(co[0] + uniform(10, 30), co[1] + uniform(10, 30))
            self.better_sleep((1.3, 2))
            cv_image = self.adb.get_cv2_img()
        return cv_image

    @get_name
    def check_reconnect(self, cv_image=None):
        """
        Check and reconnect
        """
        if cv_image is None:
            cv_image = self.adb.get_cv2_img()
        co = self.find_img(source=cv_image, target="reconnect", confidence=0.85)

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
                sleep(10)
                self.wait_until_connected()
                return self.adb.get_cv2_img()
            else:
                self.print("Reconnection disabled","red")
                self.send_discord_message("The game got disconnected, auto-Reconnection off.")
                while True:
                    self.script_pause()
                    sleep(1)
        else:
            return cv_image

    @get_name
    def wait_until_connected(self) -> None:
        self.print("Script is paused until game is fully loaded..")
        condition = True
        while condition:
            self.run_game()
            if self.find_img(target="menu_button", confidence=0.8) or \
                    self.find_img(target="map_icon", confidence=0.8) or \
                    self.find_img(target="hammer", confidence=0.8) or \
                    self.find_img(target="inbox", confidence=0.8):
                condition = False
            co = self.find_img(target="mightiest_gov", confidence=0.8)
            if co is not None:
                self.click(uniform(co[0] + 5, co[0] + 20), uniform(co[1] + 5, co[1] + 20))
                condition = False
            self.better_sleep((10, 15))
            self.check_reconnect()
            self.check_log_back()
            self.check_captcha()
            self.close_windows()
            self.close_upgrade_popup()

    @get_name
    def close_upgrade_popup(self):
        for i in range(3):
            co = self.find_img(f"upgrade_popup_{i}")
            if co is not None:
                self.click(uniform(1102, 1030), uniform(92, 118))
                self.better_sleep((2, 4))

    @get_name
    def leave_kd_buff(self, Source=None):

        co = self.find_img(target="kingdom_buff", source=Source)
        if co is not None:
            self.click(uniform(70, 270), uniform(100, 542))
            self.better_sleep((1.8, 3))
            Source = self.adb.get_cv2_img()
        return Source

    def pil_to_array(self,image):
        try:
            cv_image = array(image)
            return cv_image
        except OSError:
            self.print("Cannot load the image..")
            sleep(1)
            return self.pil_to_array(image)
    # @get_name
    def check_if_kill(self):
        """
        Kill the process if his ppid is dead
        :exemple: leave python would kill the process
        """
        if not pid_exists(self.ppid):
            self.print("pPid not found, killing the thread")
            sys.exit(1)
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
            self.script_pause()
            # pil_image = self.adb.get_curr_device_screen_img()
            # cv_image = array(pil_image)
            # cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            cv_image = self.adb.get_cv2_img()
            cropped_image = cv_image[30:170, 770:1225]
            chest = None
            for i in range(1, 4):
                self.script_pause()
                chest = self.find_img(target=f"verification_chest{i}", source=cropped_image, confidence=0.6)
                if chest is None:
                    break
            if chest is not None:
                if self.data[self.sel]['schedules'][self.current_profile]['auto_captcha']:
                    # print(co)
                    self.check_if_kill()
                    self.click(chest[0] + uniform(775, 795), chest[1] + uniform(35, 50))
                    self.better_sleep((3, 4))
                    return True
                else:
                    self.set_text(f"[{current_time()}] Captcha verification is Off")
                    self.set_status("Captcha is Off")
                    self.send_discord_message("Captcha detected, Captcha verification off.")
                    while True:
                        self.script_pause()
                        sleep(1)
            sleep(0.3)
        return False

    @get_time
    def check_captcha(self, chest=True, DefaultApiKey=True) -> bool:
        """
        Check and resolve verification
        """
        self.print(f"Scanning the screen for verification..")
        if chest:
            self.check_chest()
            sleep(1)

        co = self.find_img(target="verification_button")
        if co is not None:
            self.click(co[0] + uniform(0, 80), co[1] + uniform(0, 20))
            while self.find_img(target="close_refresh_ok", confidence=0.75) is None:
                co = self.find_img(target="verification_button")
                if co is not None:
                    self.click(co[0] + uniform(0, 80), co[1] + uniform(0, 20))
                sleep(uniform(1,3))
        i = 0
        resolved = False
        previous_text = self.get_text()

        while self.find_img(target="close_refresh_ok", confidence=0.75) is not None:
            self.solve_captcha(i,DefaultApiKey)
            i+=1
            if i == 5:
                self.print("Error, unable to resolve the captcha for 5 times in a row !")
                self.set_status(previous_text)
                return False
            resolved = True
        self.set_status(previous_text)
        return resolved

    @get_name
    def solve_captcha(self,compteur:int=0, DefaultApiKey:bool=True):
        try:
            self.print("Verification detected")
            self.set_status("Resolving captcha")

            if DefaultApiKey:
                api_key = '4805a29997857b110ef26530c7f39db1'
            else:
                api_key = self.data[self.sel]['API_KEY']
                if api_key == "":
                    return self.print("This feature require a custom ApiKey")
            if self.data[self.sel]['API_KEY'] != "":
                api_key = self.data[self.sel]['API_KEY']
            self.print("Trying to resolve the captcha")

            captcha = self.save_captcha()
            solver = TwoCaptcha(api_key, defaultTimeout=120, pollingInterval=5)

            result = solver.coordinates(f"captcha{self.sel}.jpg", lang='en')

            print(result)

            co = string_to_co(result['code'])
            if self.adb.find_img_cv(captcha) is not None:
                for x, y in co:
                    self.click(x, y)
                    self.better_sleep((0.4, 0.795))
                self.click(uniform(700, 830), uniform(570, 600))
                self.better_sleep((1, 1.795))
            captchaId = result['captchaId']
            self.better_sleep((3, 4))

            if self.find_img(target="close_refresh_ok", confidence=0.75) is None:
                resolved = True
            else:
                resolved = False

            if captchaId is not None:
                self.report_feedback(captchaId, resolved, solver)
        except Exception as e:
            traceback.print_exc()
            self.print(f"Exception raised :\n{e}\n")
            if self.refresh_captcha():
                if compteur <5:
                    return self.solve_captcha(compteur +1)


    @get_name
    def report_feedback(self, captchaId, resolved, solver):
        co = self.find_img(target="refresh_resolve")
        if co is not None:
            self.print("Captcha failed !","red")
            if captchaId is not None:
                solver.report(captchaId, False)
        else:
            resolved = True
            solver.report(captchaId, True)
            self.print("Captcha successfully solved !","green")
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
        self.adb.shell("input keyevent KEYCODE_APP_SWITCH")
        sleep(2)
        self.click(920,62)
        sleep(2)

    @get_name
    def kill_game(self) -> None:
        self.adb.shell("am force-stop com.lilithgame.roc.gp")
        self.adb.shell("am force-stop com.rok.gp.vn")
        self.adb.shell("am force-stop com.lilithgame.rok.gpkr")
        self.adb.shell("am force-stop com.lilithgames.rok.gpkr")

    @get_name
    def check_download_page(self, screen=None):
        if screen is None:
            screen = self.adb.get_cv2_img()
        if self.find_img(target="download_page", source=screen, confidence=0.8):
            self.click(uniform(1018, 1041), uniform(127, 146))
            self.better_sleep((1.925, 2.795))
            screen = self.adb.get_cv2_img()
        elif self.find_img(target="download_icon", source=screen, confidence=0.8):
            self.click(uniform(1018, 1041), uniform(127, 146))
            self.better_sleep((1.925, 2.795))
            screen = self.adb.get_cv2_img()
        return screen
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
        return self.find_img(target='gem_search_button',confidence=0.93) is None

    @get_name
    def close_windows(self):
        image = self.adb.get_cv2_img()[0:322, 0:1280]
        while (cos :=self.adb.find_multiple_img(target="close_window",source=image)):
            co = cos[-1]
            self.adb.click(co[0]+uniform(3,9),co[1]+uniform(3,9))
            self.better_sleep((1.3,2.8))
            image = self.adb.get_cv2_img()[0:322, 0:1280]
        while (cos :=self.adb.find_multiple_img(target="close_window2",source=image, confidence=0.83)):
            co = cos[-1]
            self.adb.click(co[0]+uniform(3,9),co[1]+uniform(3,9))
            self.better_sleep((1.3,2.8))
            image = self.adb.get_cv2_img()[0:322, 0:1280]
        while (cos:=self.adb.find_multiple_img(target="close_chat", confidence=0.83)):
            co = cos[-1]
            self.adb.click(co[0]+uniform(3,9),co[1]+uniform(3,9))
            self.better_sleep((1.3,2.8))

    def get_text(self):
        return self.tile.get_text()
