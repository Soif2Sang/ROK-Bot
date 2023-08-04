import json
import os
import shutil
import sys
import traceback
from datetime import date
from random import uniform, randint
from time import sleep

import re
import cv2
import win32api
import win32con
import win32gui
from PIL import Image, ImageFile
from numpy import array, ndarray
from psutil import pid_exists
from pytesseract import pytesseract

# from paddleocr import PaddleOCR
pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'

# from utils import discord_bot
from utils.Task_utils import get_window_pid, get_name, current_time, get_time, string_to_co, FileSingleton
from utils.bot_adb import Adb
# from utils.easyOcr import Reader
from utils.twocaptcha import TwoCaptcha
ImageFile.LOAD_TRUNCATED_IMAGES = True


class Task():
    def __init__(self, tile):
        self.FileSingleton = FileSingleton()
        self.data = self.FileSingleton.get_data()
        self.current_profile: str = '1'
        self.tile = tile
        self.sel: int = tile.number
        # print(self.sel)
        self.adb: Adb = Adb(self.sel)
        # print(self.sel)
        self.ppid = os.getppid()
        self.pid = get_window_pid(self.adb.name)
        self.language: str | None = None
        self.name: str = self.adb.name

    def herite(self, MainTask):
        self.data = MainTask.data
        self.current_profile = MainTask.current_profile
        self.frame = MainTask.tile
        self.adb = MainTask.adb
        self.ppid = MainTask.ppid
        self.pid = MainTask.pid
        self.language = MainTask.language
        self.name = MainTask.name
        self.sel = MainTask.sel

    def script_pause(self):
        said = False

        while self.tile.paused and not self.tile.stopped:
            if not said:
                # self.print(f"You is paused.","Yellow")
                self.set_text(f"[{current_time()}] Script is paused.", "orange")
                print(f"[ {date.today()} {current_time()} ] [ {self.name} ] Script is paused.")
                said = True
                # self.set_text("Script paused.")

        if self.tile.stopped:
            self.tile.stopped = False
            self.set_text(f"[{current_time()}] You stopped the bot", "Red")
            print(f"[ {date.today()} {current_time()} ] [ {self.name} ] You stopped the bot")
            self.set_divider()
            sys.exit(1)

        if said:
            self.set_text(f"[{current_time()}] You resumed the script.", "Green")
            print(f"[ {date.today()} {current_time()} ] [ {self.name} ] You resumed the script.")


    def set_text(self, text, color=None):
        return self.tile.add_text(text, color)

    def set_divider(self):
        return self.tile.add_divider()

    def set_status(self, text):
        return self.tile.set_text(text)

    def set_timer(self, seconds: int):
        condition = True
        while seconds and condition:
            hours, mins = divmod(seconds, 3600)
            mins, secs = divmod(mins, 60)
            self.set_status(f"{hours:02d}:{mins:02d}:{secs:02d}")
            seconds -= 1
            condition = ":" in self.tile.text_status.value and self.tile.text_status.value != "00:00:01"
            self.better_sleep((1,1))

    @get_name
    def update_data(self):
        self.data = self.FileSingleton.get_data()
        return self.data

    def set_sel(self, sel) -> None:
        self.data = self.update_data()
        self.sel = sel
        self.name = self.data.get(self.sel).get('name', "Name not found")

    @get_name
    def get_city_position(self):
        image = self.adb.get_cv2_img()
        image = image[5:33, 260:430]
        return self.extract_text(image, '#XxYy:123456789')

    @get_name
    def extract_all_text(self, img, allowlist=None):
        return self.extract_text(img, allowlist)
        # ocr = PaddleOCR(use_angle_cls=True, lang='en')  # need to run only once to download and load model into memory
        # result = ocr.ocr(img, cls=False)
        # returning_values = []
        # for idx in range(len(result)):
        #     res = result[idx]
        #     for line in res:
        #         returning_values.append(line[-1][0])
        # return  returning_values

    @get_name
    def extract_text(self, img, allowlist=None):
        if allowlist is not None:
            config = fr'--oem 1 --psm 6 -c tessedit_char_whitelist={allowlist}'
        else:
            config = r'--oem 1 --psm 6'

        return pytesseract.image_to_string(img, config=config).replace("\n", "")

        # ocr = PaddleOCR(use_angle_cls=True, lang='en')  # need to run only once to download and load model into memory
        # result = ocr.ocr(img, cls=False)
        # for idx in range(len(result)):
        #     res = result[idx]
        #     for line in res:
        #         return line[-1][0] if line[-1][0] else ''
        # return ''
        # exit()
        # reader = Reader()
        # native_text, _ = reader.extract_text(img=img, allowlist=allowlist)
        # if native_text:
        #     return native_text[0]
        # return ''
        # reader_script_path = r'.\utils\easyOcr.py'
        #
        # # Paramètres pour la méthode extract_text
        # allowlist = None  # Liste des caractères autorisés (facultatif)
        # show_text = False  # Afficher le texte sur l'image (True ou False)
        # show_confidence = False  # Afficher la confiance de détection sur l'image (True ou False)
        # use_cuda = False  # Utiliser CUDA (GPU) pour EasyOCR (True ou False)
        #
        # # Construire la commande à exécuter
        # command = ['py', '-3.11', reader_script_path, img]
        # if allowlist:
        #     command.extend(['--allowlist'] + allowlist)
        # if show_text:
        #     command.append('--show_text')
        # if show_confidence:
        #     command.append('--show_confidence')
        # if use_cuda:
        #     command.append('--cuda')
        #
        # # Exécuter la commande et récupérer le résultat
        # output = subprocess.check_output(command, universal_newlines=True)
        #
        # # Afficher le résultat
        # print(output)

    @get_name
    def print(self, text: str, color=None) -> None:
        # print(f'[ {current_time()} ] [ {self.name} ] {text}')
        if text != "":
            self.set_text(f"[{current_time()}] {text}", color)
        else:
            self.set_text("")


    @get_name
    def send_discord_message(self, message):
        return
        # if self.data["discord"]["user_id"] and self.data["discord"]["enabled"]:
        #     return discord_bot.send_message(self.data["discord"]["user_id"], f"[{current_time()}] {message}")

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

    @get_name
    def free_troop_selection(self) -> bool:
        """
        :return: True if there's a empty queue
        :return: False if queues are occupied
        """

        cv_image = self.adb.get_cv2_img()
        cropped_image = cv_image[13:35, 1225:1254]
        text = self.extract_text(cropped_image, allowlist="01234567/")

        print(text)
        if len(text) == 3:
            if text[0] < text[2]:
                self.print("Empty queue found")
                return True
            else:
                return False
        else:
            return False

    @get_name
    def free_troop_commander_list(self) -> bool:
        """
        :return: True if there's a empty queue
        :return: False if queues are occupied
        """
        cropped_image = self.adb.get_cv2_img()[160:180, 1205:1247]
        cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2GRAY)

        # imwrite("commander_list.png",cropped_image)
        native_text = self.extract_text(img=cropped_image, allowlist="12345670/")

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

    @get_name
    def random_macro(self) -> None:
        try:
            path_json = self.FileSingleton.get_path()
            for name in ["com.lilithgame.roc.gp.cfg", "com.rok.gp.vn.cfg", "com.lilithgame.rok.gpkr.cfg",
                         "com.lilithgames.rok.gp.jp.cfg",
                         "com.lilithgames.rok.gpkr.cfg"]:
                path = path_json['bluestacks'][:-15] + "Engine\\UserData\\InputMapper\\UserFiles\\" + name
                if os.path.isfile(path):
                    break

            path2 = path.replace("cfg", "json")
            shutil.copy(path, path2)

            with open(path2, encoding='utf-8') as config_file:
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
            if self.find_img(target='gem_search_button'):
                hwnd = win32gui.FindWindow(None, self.adb.name)
                hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)
                for _ in range(4):
                    self.script_pause()
                    if self.find_img(target="gem_search_button"):
                        for _ in range(2):
                            self.script_pause()
                            win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
                            win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, win32con.VK_F6, 0)
                            self.better_sleep((0.2, 0.2))
                            win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
                            win32api.PostMessage(hwndChild, win32con.WM_KEYUP, win32con.VK_F6, 0)
                            self.better_sleep((1.4, 2))
                    else:
                        break
        except Exception as e:
            print(e)

    @get_name
    def click_loop(self) -> None:
        if not self.find_img(target="gem_search_button"):
            self.print(f'Loop icon not found, leaving the city')
            self.leave_city()
            self.better_sleep((2, 3))
        x = uniform(33, 76)
        y = uniform(517, 560)
        # print(x,y)
        self.click(x, y)
        self.better_sleep((0.3, 0.5))

    @get_name
    def set_search_level(self, level: int = 10) -> None:
        cv_image = self.adb.get_cv2_img()
        co = self.find_img(source=cv_image, target="button_level", confidence=0.8)
        if co is None:
            self.print(f'Cannot find the button_level')
            # self.set_text(f"[{current_time()}] Cannot find the level button")
            self.click_loop()
            self.better_sleep((1, 1.7))
        else:
            # x,y = uniform(225,285) , uniform(607,667)
            # self.click(x,y)
            cv_image = cv_image[co[1] - 30:co[1], co[0] - 60:co[0] + 60]
            # cv2.imwrite("level.png", cv_image)
            # string = pytesseract.image_to_string(cv_image,
            #                                      config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=level:1234567890')

            string = self.extract_text(img=cv_image, allowlist="level:1234567890")
            print(f"[ {self.name} ] {string =}")
            string = string.replace("\n", "")
            string = string.split(":")

            try:
                self.print(f'Current level : {string[1]}')
                # self.set_text(f"[{current_time()}] Current level : {string[1]}")
                level_to_go = level - int(string[1])
            except:
                x, y = self.find_img(target='minus_button')
                for i in range(6):
                    self.click(x + uniform(0, 20), y + uniform(0, 20))
                    self.better_sleep((0.450, 1))
                level_to_go = level
            if level_to_go > 0:
                word = "Increasing"
                x, y = self.find_img(target='plus_button')
            else:
                word = "Decreasing"
                x, y = self.find_img(target='minus_button')
            self.print(f'{word} the level by : {abs(level_to_go)}')
            # self.set_text(f"[{current_time()}] {word} the level by : {abs(level_to_go)}")
            for _ in range(abs(level_to_go)):
                x2 = x + uniform(0, 30)
                y2 = y + uniform(0, 27)
                self.click(x2, y2)
                self.better_sleep((0.450, 1))
            return

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
            self.better_sleep((2.5,3.5))
            self.click(uniform(24, 91), uniform(625, 680))
        return True

    @get_name
    def find_img(self, target: str, source: ndarray = None, confidence=0.9):
        # self.print(f"Loading {target}")
        # print(f"[ {date.today()} {current_time()} ] [ {self.name} ] Loading {target}")
        result = self.adb.find_img(target=target, source=source, confidence=confidence)
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
                self.better_sleep((3,3))
                return self.wait_until_connected()
            else:
                if count == 0:
                    self.adb.home_button()
                    self.better_sleep((3, 3))
                    return self.run_game(count=1)
                if count == 1:
                    if self.language is None or self.language == "eng":
                        for _ in range(2):
                            string = self.adb.shell("am start -n com.lilithgame.roc.gp/com.harry.engine.MainActivity")
                            self.FileSingleton.write(self.name,
                                                     f"INFO : [{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }\n")
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
                            self.FileSingleton.write(
                                self.name,
                                f"INFO : [{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }\n")
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
                            self.FileSingleton.write(
                                self.name,
                                f"INFO : [{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }\n")
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
            a *= self.data[str(self.sel)]['schedules'][self.current_profile]["sleep_multiplicator"]
            b *= self.data[str(self.sel)]['schedules'][self.current_profile]["sleep_multiplicator"]

        sleep_duration = uniform(a, b)
        interval_duration = 0.01  # Durée de chaque intervalle (en secondes)
        num_intervals = int(sleep_duration / interval_duration)

        for _ in range(num_intervals):
            sleep(interval_duration)
            self.script_pause()

    @get_name
    def solve(self, path, sel, defaultApiKey=True):
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
            if e == 'ERROR_NO_SLOT_AVAILABLE':
                self.print(
                    "Captcha service is out of capacity right now, waiting few minutes until the service is back again",
                    "yellow")
                self.better_sleep((4 * 60, 6 * 60))
                if self.refresh_captcha():
                    return self.check_captcha()
            self.print(f"EXCEPTION : Exception raised during the resolving of the captcha :\n{e}\n", "red")
            return {'error': e}

    @get_name
    def resolve_captcha(self, compteur=0, defaultApiKey=True):
        """
        Resolve verification
        """
        self.print(f"Resolve count = {compteur}")
        if compteur > 5:
            self.print("Error in resolving the captcha, human action needed.")
            self.set_status("Error")
            self.send_discord_message("Error in resolving the captcha, human action required.")
            while True:
                self.better_sleep((1,1))
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
            print(
                f"[ {current_time()} ] [ {self.name} ] Exception raised during the resolving of the captcha (task.py related) :\n{e}")
            self.FileSingleton.write(
                self.name,
                f"EXCEPTION : Exception raised during the resolving of the captcha (task.py related) :\n{e}\n")

            if e == 'ERROR_CAPTCHA_UNSOLVABLE':
                if self.refresh_captcha():
                    return self.resolve_captcha()
                else:
                    return None
            self.refresh_captcha()
            self.print("Refreshing the captcha.", "red")
            self.better_sleep((4, 7))
            return self.resolve_captcha(compteur=compteur + 1)

    def save_captcha(self):
        pil_image = self.adb.get_curr_device_screen_img()
        try:
            cv_image = array(pil_image)
        except OSError:
            self.better_sleep((1,1))

            return self.save_captcha()
        cropped_image = cv_image[100:560, 440:840]
        cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(cropped_image)
        im_pil.save(f"captcha{self.sel}.jpg", optimize=True, quality=80)
        self.better_sleep((0.5,0.5))
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
                                    'log_back2')) * 60 + randint(0, 59)
                self.print(f"Waiting for the timer to end.. {value / 60:0.1f} minutes")
                self.better_sleep((value,value))
                self.click(co[0] + uniform(0, 50), co[1] + uniform(-10, 20))
                self.print("Reconnection..")
                self.better_sleep((5, 10))
                self.run_game()
                return True
            else:
                self.set_text("Auto Log-back off", "red")
                self.send_discord_message("The game got disconnected, Log-back off.")
                while True:
                    self.script_pause()
                    sleep(1)
        else:
            return False

    @get_name
    def check_mge(self, cv_image=None):
        if cv_image is None:
            cv_image = self.adb.get_cv2_img()
        co = self.find_img(target="mightiest_gov", source=cv_image)
        if co is not None:
            self.click(co[0] + uniform(10, 30), co[1] + uniform(10, 30))
            self.better_sleep((1.3, 2))
            cv_image = self.adb.get_cv2_img()
        return cv_image

    @get_name
    def check_reconnect(self, cv_image=None, cropped=False):
        """
        Check and reconnect
        """
        if cv_image is None:
            cv_image = self.adb.get_cv2_img()
        co = self.find_img(source=cv_image, target="reconnect", confidence=0.85)

        if co is not None:

            if self.data.get(self.sel).get('schedules').get(self.current_profile).get('auto_reconnect', False):
                print("[ {current_time()} ] [ {self.name} ] You just got disconnected")
                print(co)
                if cropped:
                    a = (480 + co[0] + uniform(0, 100), 420 + co[1] + uniform(0, 20))
                    print(a)
                    self.click(a[0], a[1])
                else:
                    a = (co[0] + uniform(0, 100), co[1] + uniform(0, 20))
                    print(a)
                    self.click(a[0], a[1])
                self.better_sleep((10,10))
                self.wait_until_connected()
                return self.adb.get_cv2_img()
            else:
                self.print("Reconnection disabled", "red")
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
            if self.find_img(target="menu_button", confidence=0.6) or \
                    self.find_img(target="map_icon", confidence=0.6) or \
                    self.find_img(target="hammer", confidence=0.6) or \
                    self.find_img(target="inbox", confidence=0.6):
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

    def pil_to_array(self, image):
        try:
            cv_image = array(image)
            return cv_image
        except OSError:
            self.print("Cannot load the image..")
            self.better_sleep((1,1))

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
            cropped_image = cv_image[30:170, 0:1225]
            chest = None
            for i in range(1, 4):
                self.script_pause()
                chest = self.find_img(target=f"verification_chest{i}", source=cropped_image, confidence=0.6)
                if chest is None:
                    break
            if chest is not None:
                if self.data[self.sel]['schedules'][self.current_profile]['auto_captcha']:
                    # print(co)
                    self.click(chest[0] + uniform(0, 30), chest[1] + uniform(35, 50))
                    self.better_sleep((3,4))
                    return True
                else:
                    self.set_text(f"[{current_time()}] Captcha verification is Off")
                    self.set_status("Captcha is Off")
                    self.send_discord_message("Captcha detected, Captcha verification off.")
                    while True:
                        self.better_sleep((1,1.1))
                        
            self.better_sleep((0.3,0.3))
        return False

    @get_name
    def check_captcha(self, chest=True, DefaultApiKey=True) -> bool:
        """
        Check and resolve verification
        """
        # self.print(f"Scanning the screen for verification..")
        if chest:
            self.check_chest()
            self.better_sleep((1,1.1))
        co = self.find_img(target="verification_button")
        if co is not None:
            self.click(co[0] + uniform(0, 80), co[1] + uniform(0, 20))
            while self.find_img(target="close_refresh_ok", confidence=0.75) is None:
                co = self.find_img(target="verification_button")
                if co is not None:
                    self.click(co[0] + uniform(0, 80), co[1] + uniform(0, 20))
                self.better_sleep((1.4,3))
        i = 0
        resolved = False
        previous_text = self.get_text()

        while self.find_img(target="close_refresh_ok", confidence=0.75) is not None:
            self.solve_captcha(i, DefaultApiKey)
            i += 1
            if i == 5:
                self.print("Error, unable to resolve the captcha for 5 times in a row !")
                self.set_status(previous_text)
                return False
            resolved = True
        self.set_status(previous_text)
        return resolved

    @get_name
    def solve_captcha(self, compteur: int = 0, DefaultApiKey: bool = True):
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
                if compteur < 5:
                    return self.solve_captcha(compteur + 1)

    @get_name
    def report_feedback(self, captchaId, resolved, solver):
        co = self.find_img(target="refresh_resolve")
        if co is not None:
            self.print("Captcha failed !", "red")
            if captchaId is not None:
                solver.report(captchaId, False)
        else:
            resolved = True
            solver.report(captchaId, True)
            self.print("Captcha successfully solved !", "green")
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
        self.better_sleep((2,2.1))
        self.click(920, 62)
        self.better_sleep((2,2.1))

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
        return not self.find_img(target='gem_search_button', confidence=0.79)

    @get_name
    def close_windows(self):
        image = self.adb.get_cv2_img()[0:322, 0:1280]
        while (cos := self.adb.find_multiple_img(target="close_window", source=image)):
            co = cos[-1]
            self.adb.click(co[0] + uniform(3, 9), co[1] + uniform(3, 9))
            self.better_sleep((1.3, 2.8))
            image = self.adb.get_cv2_img()[0:322, 0:1280]
        while (cos := self.adb.find_multiple_img(target="close_window2", source=image, confidence=0.83)):
            co = cos[-1]
            self.adb.click(co[0] + uniform(3, 9), co[1] + uniform(3, 9))
            self.better_sleep((1.3, 2.8))
            image = self.adb.get_cv2_img()[0:322, 0:1280]
        while (cos := self.adb.find_multiple_img(target="close_chat", confidence=0.83)):
            co = cos[-1]
            self.adb.click(co[0] + uniform(3, 9), co[1] + uniform(3, 9))
            self.better_sleep((1.3, 2.8))

    def get_text(self):
        return self.tile.get_text()
    

    @get_name
    def recenter(self, deadstop = 0):
        image = self.adb.get_cv2_img()
        if (co := self.find_img(source=image, target="green_home_button")):
            # reader = Reader()
            if deadstop == 10:
                self.click(co[0],co[1])
                self.better_sleep((2,3))
                return
            x, y = co[0] - 10, co[1] - 10
            x2, y2 = co[0] + 50, co[1] + 50
            # Fill the specified region with dark gray color
            cv2.rectangle(image, (x, y), (x2, y2), (50, 50, 50), -1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = self.get_neighboring_image(image=image, center_point=co)
            first_try = image[0:35, :]
            second_try = image[-30:, :]

            word = ''

            first = self.extract_text(first_try, allowlist="0123456789KM")
            second = self.extract_text(second_try, allowlist="0123456789KM")

            if re.match(r'\d+KM', second):
                word = second
            if re.match(r'\d+KM', first):
                word = first
            if re.match(r'\d+KM', word):
                if word.split("KM")[0].isnumeric() and int(word.split("KM")[0]) > int(
                        self.data[str(self.sel)]['schedules'][self.current_profile].get('radius', 40)) * 1.5:
                    print(word)
                    if co[0] < 500 and co[1] < 220:
                        self.swipe(330, 160, 760, 530)
                    elif co[0] < 500 and co[1] > 550:
                        self.swipe(330, 530, 760, 160)
                    elif co[0] > 800 and co[1] > 550:
                        self.swipe(980, 530, 330, 160)
                    elif co[0] > 800 and co[1] < 220:
                        self.swipe(760, 160, 330, 530)
                    elif co[0] <= 500:
                        self.swipe_left()
                    elif co[0] >= 800:
                        self.swipe_right()
                    elif co[1] >= 360:
                        self.swipe_down()
                    else:
                        self.swipe_up()
                    self.better_sleep((1, 2))
                    return self.recenter(deadstop = deadstop +1)

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
    def adjusted_leave_city(self, x_click: int, y_click: int) -> None:

        self.zoom_out_city()

        self.better_sleep((1, 2))
        self.little_zoom_from_x_y(x_click, y_click)
        return self.better_sleep((0.7, 1.4))

    @get_name
    def find_cross_source(self, source) -> bool:
        """
        :param: pil_image or cv_image
        :return: True if node is occupied or someone is coming to the node
        :return: False if node is free to gather
        """
        return self.find_cross(source)
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
    def already_mining(self, x, y, image=None) -> bool:
        """
        :param: x -> int - x location of the node
        :param: y -> int - y location of the node
        :param: image -> image - device screenshot
        :return: True if node is not free
        :return: False if node is free to gather
        """
        if image is None:
            cv_image = self.adb.get_cv2_img()
        else:
            cv_image = image
        x_min = max(0, x - 40)
        x_max = min(cv_image.shape[1] - 1, x + 60)
        y_min = max(0, y - 40)
        y_max = min(cv_image.shape[0] - 1, y + 50)

        cropped_image = cv_image[y_min:y_max, x_min:x_max]

        # cv2.imwrite("gem_node.png", cropped_image)
        return self.find_cross_source(cropped_image)


    @get_name
    def leave_city_simple(self) -> bool:
        """
        -Enter and leave city if not in city
        -Leave city if in city
        """
        if self.in_city():
            self.click(uniform(24, 91), uniform(625, 680))
            self.better_sleep((1.5, 3))
        return True

    @get_name
    def node_found(self) -> bool:
        if self.find_img(target='search_button') is not None:
            self.print("Node not found")
            return False
        return True

    @get_name
    def find_cross(self, source=None, notify = True) -> bool:
        """
        :return: True if node is occupied or someone is coming to the node
        :return: False if node is free to gather
        """
        if notify:
            self.print("Scanning the node..")
        if source is None:
            source = self.adb.get_cv2_img()[230:480, 441:814]
        img = Image.fromarray(source)

        occupied_colors = [
            (2, 4, 183), (233, 233, 233), (247, 156, 47), (207, 131, 40), (248, 157, 48),
            (239, 205, 165), (0, 0, 178), (2, 204, 2), (195, 142, 0), (0, 154, 14),
            (0, 154, 13), (1, 186, 0), (0, 142, 193), (12, 154, 1), (1, 215, 0),
            (1, 216, 0), (253, 253, 253), (49, 161, 255), (2, 197, 2), (247, 210, 167),
            (255, 161, 49), (253, 253, 253), (167, 121, 28), (28, 121, 167)
        ]

        for i in range(img.size[0]):
            for y in range(img.size[1]):
                if (((img.getpixel((i, y))[0] < 5) and
                     (img.getpixel((i, y))[1] < 5) and
                     (img.getpixel((i, y))[2] > 175) and
                     (img.getpixel((i, y))[2] < 196) and
                     ((img.getpixel((i, y))[0] != 2) and
                      (img.getpixel((i, y))[1] != 4) and
                      (img.getpixel((i, y))[2] != 183))) or

                        ((img.getpixel((i, y))[2] < 179) and
                         (img.getpixel((i, y))[2] > 175) and
                         (img.getpixel((i, y))[1] > 116) and
                         (img.getpixel((i, y))[1] < 119) and
                         (img.getpixel((i, y))[0] < 2))
                        or
                        ((img.getpixel((i, y))[0] < 5) and
                         (img.getpixel((i, y))[1] > 142) and
                         (img.getpixel((i, y))[1] < 150) and
                         (img.getpixel((i, y))[2] < 200) and
                         (img.getpixel((i, y))[2] > 190))
                        or
                        (img.getpixel((i, y)) in occupied_colors)):
                    self.print(f"Node occupied {img.getpixel((i, y))}")
                    return True
        return False

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

    def run(self):
        pass

