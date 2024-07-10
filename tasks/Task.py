from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import sys
import traceback
from datetime import datetime
from random import choice, randint, uniform
from time import sleep

import cv2
import deprecation
import flet as ft

from constants import INVENTORY_BUTTON, ALLIANCE_BUTTON, COMMANDER_BUTTON, CAMPAIGN_BUTTON
from utils.context import contextManager

try:
    import win32api
    import win32con
    import win32gui
except:
    pass
from numpy import array, ndarray
from PIL import Image, ImageFile
from pytesseract import pytesseract
from utils.schemas.emulator_schemas import EmulatorSettingsSchema, ProfileSchema

from utils.android_debug_bridge_bluestacks import AdbBluestacks
from utils.android_debug_bridge_ld_player import AdbLd
from utils.discord_utils import send_discord_message
from utils.functions import (
    colorize_name,
    colorize_output,
    current_time,
    get_name,
    rgetattr,
    string_to_co,
    string_to_co_slide,
)

from utils.singletons import ApiSingleton, EmulatorSingleton, ss, FileSingleton
from utils.supabase_auth import SupabaseClient
from utils.twocaptcha import TimeoutException, TwoCaptcha
from utils.twocaptcha.api import ApiException, NetworkException

ImageFile.LOAD_TRUNCATED_IMAGES = True
pytesseract.tesseract_cmd = r".\\tesseract\\tesseract.exe"


class Task:
    def __init__(self, tile, contextManager):
        self.current_profile: str = "1"
        self.sel: str = tile
        self.contextManager = contextManager
        self.tile = self.contextManager.get_slave(self.sel)

        self.context: EmulatorSettingsSchema = ss.emulator_settings.emulators[self.sel]
        self.context_profile: ProfileSchema = ss.emulator_settings.emulators[self.sel].schedules[self.current_profile]
        self.FileSingleton = FileSingleton()

        emulator = EmulatorSingleton().getEmulatorType()

        if emulator == "bluestacks":
            self.adb = AdbBluestacks(self.sel, task_reference=self)
        else:
            self.adb = AdbLd(self.sel, task_reference=self)

        self.name: str = self.context.name
        self.language: str | None = None
        self.DEV = False

        for workerId, worker in ss.worker_settings.worker_type[emulator].workers.items():
            for instance in worker.instances:
                if instance.instance == self.sel:
                    self.runner_number = workerId

    def herite(self, MainTask):
        self.context = MainTask.context
        self.current_profile = MainTask.current_profile
        self.tile = MainTask.tile
        self.sel = MainTask.sel
        self.adb = MainTask.adb
        self.language = MainTask.language
        self.name = MainTask.name
        self.DEV = MainTask.DEV
        self.FileSingleton = MainTask.FileSingleton
        self.context_profile = ss.emulator_settings.emulators[self.sel].schedules[self.current_profile]
        self.runner_number = MainTask.runner_number
        self.contextManager = MainTask.contextManager
        # self.data = MainTask.data

    def debug(self, arg):
        timestamp = f"[ \033[1;32m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m ]"
        message = f"[ {colorize_name(self.name)} ] {colorize_output(arg)}"

        print(f"{timestamp} {message}")

    def script_pause(self):
        said = False

        while self.contextManager.tasks.get(self.runner_number).status == "paused":
            if not said:
                self.add_log(f"[{current_time()}] Script is paused.", "orange")
                self.debug("Script is paused.")
                said = True
            sleep(0.001)

        if self.contextManager.tasks.get(self.runner_number).status == "stopped":
            self.add_log(f"[{current_time()}] You stopped the bot", "Red")
            self.set_divider()
            self.set_status("")
            self.debug("You stopped the bot")
            sys.exit(1)

        if said:
            self.add_log(f"[{current_time()}] You resumed the script.", "Green")
            self.debug("You resumed the script.")

    def add_log(self, text, color=None):
        return self.contextManager.get_slave(self.sel).add_text(text, color)


    def set_divider(self):
        return self.contextManager.get_slave(self.sel).add_divider()

    def set_status(self, text):
        return self.contextManager.get_slave(self.sel).set_status(text)

    @get_name
    def set_timer(self, seconds: int):
        condition = True
        while seconds and condition:
            hours, mins = divmod(seconds, 3600)
            mins, secs = divmod(mins, 60)
            self.set_status(f"{hours:02d}:{mins:02d}:{secs:02d}")
            seconds -= 1
            condition = ":" in self.tile.text_status.value and self.tile.text_status.value != "00:00:01"
            self.better_sleep((1, 1), reduce_speed=False)
        self.set_status("")

    @deprecation.deprecated(details="Use better_sleep instead")
    def update_data(self):
        self.data = self.FileSingleton.get_data()
        return self.data

    def set_sel(self, sel) -> None:
        # self.data = self.update_data()
        # self.name = self.data.get(self.sel).get("name", "Name not found")
        self.sel: str = sel
        self.context: EmulatorSettingsSchema = ss.emulator_settings.emulators[self.sel]
        self.context_profile: ProfileSchema = self.context.schedules[self.current_profile]
        self.name: str = self.context.name

    @get_name
    def get_city_position(self):
        image = self.adb.get_cv2_img()
        image = image[5:33, 260:430]
        return self.extract_text(image, "#XxYy:123456789")

    @get_name
    def extract_all_text(self, img, allowlist=None):
        return self.extract_text(img, allowlist)

    @get_name
    def extract_text(self, img, allowlist=None):
        if allowlist is not None:
            config = rf"--oem 3 --psm 10 -c tessedit_char_whitelist={allowlist}"
        else:
            config = r"--oem 3 --psm 10"

        enhanced_image = self.modify_image(img)
        # return pytesseract.image_to_string(img, config=config).replace("\n", "")

        return pytesseract.image_to_string(self.modify_image(enhanced_image), config=config).replace("\n", "")

    def print(self, text: str, color=None) -> None:
        if text != "":
            self.add_log(f"[{current_time()}] {text}", color)
        else:
            self.add_log("")

    @get_name
    def send_discord_message(self, message, image=True):
        if ss.application_settings.discord.user_id and ss.application_settings.discord.enabled:
            if image:
                self.adb.save_screen(f"{self.name}_error")
                asyncio.run(send_discord_message(self.name, message, f"{self.name}_error.png"))
            else:
                asyncio.run(send_discord_message(self.name, message))

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
        cropped_image = self.adb.get_cv2_img()[130:160, 1205:1247]
        cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2GRAY)
        native_text = self.extract_text(img=cropped_image, allowlist="12345670/")

        if "/" in native_text:
            enhanced_text = native_text.split("/")[0] + native_text.split("/")[1]
        else:
            enhanced_text = native_text
        enhanced_text = enhanced_text.replace("\n", "")
        if len(enhanced_text) < 2:
            return True
        if len(enhanced_text) == 2:
            return enhanced_text[0] < enhanced_text[1]

    @get_name
    def random_macro(self) -> bool:
        try:
            for name in [
                "com.lilithgame.roc.gp.cfg",
                "com.rok.gp.vn.cfg",
                "com.lilithgame.rok.gpkr.cfg",
                "com.lilithgames.rok.gp.jp.cfg",
                "com.lilithgames.rok.gpkr.cfg",
            ]:
                path = ss.application_settings.paths.bluestacks.config[:-15] + "Engine\\UserData\\InputMapper\\UserFiles\\" + name
                if os.path.isfile(path):
                    break

            path2 = path.replace("cfg", "json")
            shutil.copy(path, path2)

            with open(path2, encoding="utf-8") as config_file:
                macro_json = json.load(config_file)
            for element in macro_json["ControlSchemes"]:
                if element["Selected"]:
                    # print(element["Name"])
                    for macro in element["GameControls"]:
                        # print(macro)
                        if macro["KeyOut"] == "F6":
                            # print("True")
                            x1 = randint(40, 50)
                            randint(40, 50)
                            y = randint(25, 30)
                            macro["X1"] = x1
                            macro["X2"] = x1
                            macro["Y1"] = y + 0.64
                            macro["Y2"] = y + 43.42
            with open(path2, "w", encoding="UTF-8") as outfile:
                json.dump(macro_json, outfile, ensure_ascii=False)
            shutil.copy(path2, path)
            return True
        except Exception as e:
            self.generate_toast(
                "Error",
                "You did not import the config file, watch #tutorial to import it.",
            )

            for _ in range(5):
                self.print("/!\ FIX IT !! /!\ ", "red")
            print(
                f"[ {current_time()} ] [ {self.name} ] Wrong macro location, cannot randomise it.. Please import the file com.lilithgame.roc.gp.cfg \nIf you don't know how to do it please watch the video in the #tutorial\n{e}"
            )
            self.print(
                "Wrong macro location, cannot randomise it.. Please import the file com.lilithgame.roc.gp.cfg \nIf you don't know how to do it please watch the video in the #tutorial",
                "red",
            )
            for _ in range(5):
                self.print("/!\ FIX IT !! /!\ ", "red")
            return False

    def generate_toast(self, title, description, icon=ft.icons.INFO, bgcolor_title="RED"):
        ss.page.generate_toast(title, description, icon=icon, bgcolor_title=bgcolor_title)

    @get_name
    def open_menu(self):
        if self.find_img(target="menu_opened", confidence=0.8, source=self.adb.get_cv2_img()[720 // 6 :, 1280 // 2 :]) is None:
            x, y = uniform(1200, 1250), uniform(650, 690)
            self.click(x, y)
            self.better_sleep((1.725, 1.995))

    @get_name
    def open_inventory(self):
        self.click(INVENTORY_BUTTON[0] + uniform(-10, +10), INVENTORY_BUTTON[1] + uniform(-10, +10))
        self.better_sleep((1.725, 1.995))

    @get_name
    def open_any_inventory_tab(self):
        cords = [230, 400, 550, 705, 850, 1000]

        x, y = choice(cords) + uniform(-10, 10), 80 + uniform(-10, 10)

        self.click(x, y)
        self.better_sleep((1.725, 1.995))

    @get_name
    def open_commander_tab(self):
        self.click(COMMANDER_BUTTON[0] + uniform(-10, +10), COMMANDER_BUTTON[1] + uniform(-10, +10))
        self.better_sleep((1.725, 1.995))

    @get_name
    def open_alliance_menu(self):
        # Open du menu
        self.open_menu()
        # Open alliance menu
        self.click(ALLIANCE_BUTTON[0] + uniform(-10, +10), ALLIANCE_BUTTON[1] + uniform(-10, +10))
        self.better_sleep((1.725, 2.295))

    @get_name
    def click_any_commander_in_list(self):
        width = [90, 195]
        height = [190, 330, 470, 600]

        self.click(choice(width) + uniform(-10, 10), choice(height) + uniform(-10, 10))
        self.better_sleep((1.725, 1.995))

    def open_campaign(self):
        self.click(CAMPAIGN_BUTTON[0] + uniform(-10, 10), CAMPAIGN_BUTTON[1] + uniform(-10, 10))
        self.better_sleep((1.725, 1.995))

    def open_sunset_canyon(self):
        self.click(780 + uniform(-10, 10), 310 + uniform(-10, 10))
        self.better_sleep((1.725, 1.995))

    @get_name
    def zoom_out_city(self) -> None:
        """
        Leave the city by sending 'F5' key signal to the emulator
        """
        has_zoomed_out = False
        self.script_pause()
        try:
            if self.find_img(target="gem_search_button", source=self.adb.get_cv2_img()):
                self.print("Zooming out..")
                hwnd = win32gui.FindWindow(None, self.adb.name)
                hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)

                if self.adb.is_ld:
                    hwnd = hwndChild

                while self.find_img(target="gem_search_button", source=self.adb.get_cv2_img()):
                    has_zoomed_out = True
                    self.script_pause()
                    win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
                    win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, win32con.VK_F6, 0)
                    self.better_sleep((0.45, 0.45))
                    win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
                    win32api.PostMessage(hwndChild, win32con.WM_KEYUP, win32con.VK_F6, 0)
                    self.better_sleep((1.4, 2))
                    self.script_pause()
                    win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
                    win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, win32con.VK_F6, 0)
                    self.better_sleep((0.17, 0.17))
                    win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
                    win32api.PostMessage(hwndChild, win32con.WM_KEYUP, win32con.VK_F6, 0)
                    self.better_sleep((1.4, 2))

                if has_zoomed_out:
                    self.script_pause()
                    win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
                    win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, win32con.VK_F6, 0)
                    self.better_sleep((0.45, 0.45))
                    win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
                    win32api.PostMessage(hwndChild, win32con.WM_KEYUP, win32con.VK_F6, 0)
                    self.better_sleep((1.4, 2))

        except Exception as e:
            print(e)

    @get_name
    def click_loop(self) -> None:
        if not self.find_img(target="gem_search_button", source=self.adb.get_cv2_img()):
            self.print(f"Loop icon not found, leaving the city")
            self.close_windows()
            self.leave_city()
            self.better_sleep((2, 3))
        x = uniform(33, 76)
        y = uniform(517, 560)
        # print(x,y)
        self.click(x, y)
        self.better_sleep((0.9, 1.3))

    @get_name
    def set_search_level(self, level: int = 10) -> None:
        cv_image = self.adb.get_cv2_img()
        co = self.find_img(source=cv_image, target="button_level", confidence=0.8)
        if co is None:
            self.print(f"Cannot find the button_level")
            # self.add_log(f"[{current_time()}] Cannot find the level button")
            self.click_loop()
            self.better_sleep((1, 1.7))
        else:
            # x,y = uniform(225,285) , uniform(607,667)
            # self.click(x,y)
            cv_image = cv_image[co[1] - 30 : co[1], co[0] - 60 : co[0] + 60]
            # cv2.imwrite("level.png", cv_image)
            # string = pytesseract.image_to_string(cv_image,
            #                                      config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=level:1234567890')

            string = self.extract_text(img=cv_image, allowlist="level:1234567890")
            self.debug(string)
            string = string.replace("\n", "")
            string = string.split(":")

            try:
                if string[1] == "1l":
                    string[1] = "1"
                self.print(f"Current level : {string[1]}")
                # self.add_log(f"[{current_time()}] Current level : {string[1]}")
                level_to_go = level - int(string[1].replace("l", "1"))
            except:
                x, y = self.find_img(target="minus_button")
                for i in range(6):
                    self.click(x + uniform(0, 20), y + uniform(0, 20))
                    self.better_sleep((0.450, 1))
                level_to_go = level
            if level_to_go > 0:
                word = "Increasing"
                x, y = self.find_img(target="plus_button")
            else:
                word = "Decreasing"
                x, y = self.find_img(target="minus_button")

            self.print(f"{word} the level by : {abs(level_to_go)}")
            # self.add_log(f"[{current_time()}] {word} the level by : {abs(level_to_go)}")
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
        # I need to randomise the swipe by a little bit, for exemple having a range of 0 to 20 pixels
        x1, y1 = uniform(970, 990), uniform(350, 370)

        return self.swipe(x1, y1, x1 - uniform(600, 620), y1 + uniform(-3, 3))

    def swipe_left(self) -> None:
        """
        Send adb signal to swipe to the left
        """
        x1, y1 = uniform(290, 310), uniform(350, 370)

        return self.swipe(x1, y1, x1 + uniform(600, 620), y1 + uniform(-3, 3))

    def swipe_up(self) -> None:
        """
        Send adb signal to swipe upward
        """
        # Randomize the y-coordinates for the start and end points of the swipe
        y1 = uniform(150, 170)
        y2 = uniform(550, 570)

        # Keep the x-coordinate almost the same
        x = uniform(630, 650)

        return self.swipe(x, y1, x + uniform(-3, 3), y2)

    def swipe_down(self) -> None:
        """
        Send adb signal to swipe downward
        """
        # Randomize the y-coordinates for the start and end points of the swipe
        y1 = uniform(550, 570)
        y2 = uniform(130, 150)

        # Keep the x-coordinate almost the same
        x = uniform(630, 650)

        return self.swipe(x, y1, x + uniform(-3, 3), y2)

    def swipe_right_low(self) -> None:
        """
        Send adb signal to swipe t"o" the right
        """
        x1, y1, x2, y2 = (
            uniform(700, 720),
            uniform(330, 380),
            uniform(260, 280),
            uniform(330, 380),
        )
        self.swipe(x1, y1, x2, y2)

    def swipe_left_low(self) -> None:
        """
        Send adb signal to swipe to the left
        """
        x1, y1, x2, y2 = (
            uniform(700, 720),
            uniform(330, 380),
            uniform(260, 280),
            uniform(330, 380),
        )
        self.swipe(x2, y2, x1, y1)

    def swipe_up_low(self) -> None:
        """
        Send adb signal to swipe upward
        """
        x1, y1, x2, y2 = (
            uniform(540, 560),
            uniform(540, 560),
            uniform(570, 600),
            uniform(200, 220),
        )
        self.swipe(x2, y2, x1, y1)

    def swipe_down_low(self) -> None:
        """
        Send adb signal to swipe downward
        """
        x1, y1, x2, y2 = (
            uniform(540, 560),
            uniform(540, 560),
            uniform(570, 600),
            uniform(200, 220),
        )
        self.swipe(x1, y1, x2, y2)

    @get_name
    def leave_city(self, tries=0) -> bool:
        """
        -Enter and leave city if not in city
        -Leave city if in city
        """
        if self.in_city():
            self.click(uniform(24, 91), uniform(625, 680))
            self.better_sleep((1.5, 2))
        else:
            self.click(uniform(24, 91), uniform(625, 680))
            self.better_sleep((2.5, 3.5))
            if tries == 0:
                return self.leave_city(1)
            else:
                self.click(uniform(24, 91), uniform(625, 680))
                self.better_sleep((2.5, 3.5))
        return True

    # @get_name
    def find_img(self, target: str, source: ndarray = None, confidence=0.9):
        # self.print(f"Loading {target}")
        # print(f"[ {date.today()} {current_time()} ] [ {self.name} ] Loading {target}")
        result = self.adb.find_img(target=target, source=source, confidence=confidence)
        # self.print(f"Successfully loaded {target}")
        # print(f"[ {date.today()} {current_time()} ] [ {self.name} ] Successfully loaded {target}")

        return result

    # @get_name
    # def run_game(self, count=0) -> None:
    #     # print(self.adb.is_game_alive())
    #     a = self.adb.is_game_alive()
    #     if not a:
    #         self.print(f"Looks like game is not running", ft.colors.RED_300)
    #         co = self.find_img(target="rokicon", confidence=0.8)
    #         if co is not None:
    #             self.click(co[0] + 10, co[1] + 10)
    #             self.better_sleep((5, 5))
    #             return self.wait_until_connected()
    #         else:
    #             if count == 0:
    #                 self.adb.home_button()
    #                 self.better_sleep((5, 5))
    #                 return self.run_game(count=1)
    #             if count == 1:
    #                 if self.language is None or self.language == "eng":
    #                     for _ in range(2):
    #                         string = self.adb.shell("am start -n com.lilithgame.roc.gp/com.harry.engine.MainActivity")
    #                         self.FileSingleton.write(
    #                             self.name,
    #                             f"INFO : [{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }\n",
    #                         )
    #                         if "Error" in str(string):
    #                             break
    #                         if "Activity not started" not in str(string):
    #                             self.print("Starting the game !")
    #                             self.wait_until_connected()
    #                             self.language = "eng"
    #                             return self.run_game(count=2)
    #                         if "Activity not started" in str(string):
    #                             return
    #                 if self.language is None or self.language == "vn":
    #                     for i in range(2):
    #                         string = self.adb.shell("am start -n com.rok.gp.vn/com.harry.engine.MainActivity")
    #                         self.FileSingleton.write(
    #                             self.name,
    #                             f"INFO : [{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }\n",
    #                         )
    #                         if "Error" in str(string):
    #                             # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] shell dumpsys activity activities')
    #                             return
    #                         if "Activity not started" not in str(string):
    #                             self.print("Starting the game !")
    #                             self.wait_until_connected()
    #                             self.language = "vn"
    #                             return self.run_game(count=2)
    #                         if "Activity not started" in str(string):
    #                             return
    #                 if self.language is None or self.language == "kr":
    #                     for i in range(2):
    #                         string = self.adb.shell("am start -n com.lilithgame.rok.gpkr/com.harry.engine.MainActivity")
    #                         self.FileSingleton.write(
    #                             self.name,
    #                             f"INFO : [{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }\n",
    #                         )
    #                         if "Error" in str(string):
    #                             # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] shell dumpsys activity activities')
    #                             return
    #                         if "Activity not started" not in str(string):
    #                             self.print("Starting the game !")
    #                             self.wait_until_connected()
    #                             self.language = "kr"
    #                             return self.run_game(count=2)
    #                         if "Activity not started" in str(string):
    #                             return
    #
    #             self.print("ERROR CANNOT START THE GAME.")
    #             self.send_discord_message("ERROR CANNOT START THE GAME.")
    #             while True:
    #                 self.set_status("ERROR CANNOT START GAME")
    #                 self.script_pause()
    #                 sleep(1)

    @get_name
    def run_game(self, count=0) -> None:
        a = self.adb.is_game_alive()

        if not a:
            self.print(f"Looks like the game is not running", ft.colors.RED_300)
            co = self.find_img(target="rokicon", confidence=0.8)

            if co is not None:
                self.click(co[0] + 10, co[1] + 10)
                self.better_sleep((10, 10))
                return self.wait_until_connected()
            else:
                if count == 0:
                    self.adb.home_button()
                    self.better_sleep((3, 3))
                    return self.run_game(count=1)

                languages = ["eng", "vn", "kr"]
                package_name = {"eng": "com.lilithgame.roc.gp", "vn": "com.rok.gp.vn", "kr": "com.lilithgame.rok.gpkr"}

                for language in languages:
                    string = self.adb.shell(f"am start -n {package_name[language]}/com.harry.engine.MainActivity")

                    self.FileSingleton.write(
                        self.name,
                        f"INFO : [{self.name}]{string=}\n{'Error' in str(string) = }\n{'Activity not started' in str(string) = }\n",
                    )

                    if "does not exist" in str(string):
                        continue
                    if "Activity not started" not in str(string):
                        self.print("Starting the game!", ft.colors.GREEN_200)
                        self.better_sleep((5, 5))
                        self.wait_until_connected()
                        self.language = language
                        return self.run_game(count=2)
                    else:
                        return
                self.print("ERROR CANNOT START THE GAME.", ft.colors.RED)
                self.send_discord_message("ERROR CANNOT START THE GAME.")
                self.debug(self.adb.shell("pm list packages"))
                while True:
                    self.set_status("ERROR CANNOT START GAME")
                    self.script_pause()
                    self.better_sleep((1, 1))

    # @get_name
    def better_sleep(self, limits: tuple[float, float], reduce_speed=True):
        a = limits[0]
        b = limits[1]

        if reduce_speed:
            if self.context_profile.sleep_factor.enabled:
                a *= self.context_profile.sleep_factor.factor
                b *= self.context_profile.sleep_factor.factor

        sleep_duration = uniform(a, b)
        interval_duration = 0.01  # Durée de chaque intervalle (en secondes)
        num_intervals = int(sleep_duration / interval_duration)

        for _ in range(num_intervals):
            sleep(interval_duration)
            self.script_pause()

    def handle_captcha_limit(self):
        s = SupabaseClient()
        nb_captcha = s.increamentCaptchaCount()

        subscription_tier = ApiSingleton().getTier()

        if ss.application_settings.captcha.api_key:
            return

        if subscription_tier == "tier4":
            if nb_captcha == 200 * 30:
                self.generate_toast(
                    "Captcha limit.",
                    "Your captcha requests are nearing the limit. Please try to minimize captcha solves to avoid being rate limited or Upgrade plan to increase limit.",
                    ft.icons.WARNING_OUTLINED,
                    ft.colors.AMBER,
                )
            if nb_captcha >= 230 * 30:
                self.send_discord_message("Captcha limit exceeded. You may want to upgrade your tier.", False)
                self.print("You have exceeded the captcha limit. Please try again later.", ft.colors.RED)
                self.set_status("Captcha Limit Exceeded")
                while True:
                    self.better_sleep((60 * 5, 60 * 5))
        elif subscription_tier == "tier3":
            if nb_captcha == 140 * 30:
                self.generate_toast(
                    "Captcha limit.",
                    "Your captcha requests are nearing the limit. Please try to minimize captcha solves to avoid being rate limited or Upgrade plan to increase limit.",
                    ft.icons.WARNING_OUTLINED,
                    ft.colors.AMBER,
                )
            if nb_captcha >= 170 * 30:
                self.send_discord_message("Captcha limit exceeded. You may want to upgrade your tier.", False)
                self.print("You have exceeded the captcha limit. Please try again later.", ft.colors.RED)
                self.set_status("Captcha Limit Exceeded")
                while True:
                    self.better_sleep((60 * 5, 60 * 5))
        elif subscription_tier == "tier2":
            if nb_captcha == 100 * 30:
                self.generate_toast(
                    "Captcha limit.",
                    "Your captcha requests are nearing the limit. Please try to minimize captcha solves to avoid being rate limited or Upgrade plan to increase limit.",
                    ft.icons.WARNING_OUTLINED,
                    ft.colors.AMBER,
                )
            if nb_captcha >= 130 * 30:
                self.send_discord_message("Captcha limit exceeded. You may want to upgrade your tier.", False)
                self.print("You have exceeded the captcha limit. Please try again later.", ft.colors.RED)
                self.set_status("Captcha Limit Exceeded")
                while True:
                    self.better_sleep((60 * 5, 60 * 5))
        elif subscription_tier == "tier1":
            if nb_captcha == 50 * 30:
                self.generate_toast(
                    "Captcha limit.",
                    "Your captcha requests are nearing the limit. Please try to minimize captcha solves to avoid "
                    "being rate limited or Upgrade plan to increase limit.",
                    ft.icons.WARNING_OUTLINED,
                    ft.colors.AMBER,
                )
            if nb_captcha >= 70 * 30:
                self.send_discord_message("Captcha limit exceeded. You may want to upgrade your tier.", False)
                self.print("You have exceeded the captcha limit. Please try again later.", ft.colors.RED)
                self.set_status("Captcha Limit Exceeded")
                while True:
                    self.better_sleep((60 * 5, 60 * 5))
        else:
            return False
        return True

    @get_name
    def check_captcha_slider(self, deadstop=0):
        while self.find_img("slider_captcha", confidence=0.83) and deadstop != 5:
            if deadstop == 0:
                self.print(
                    "Captcha detected !",
                )

            self.handle_captcha_limit()
            captcha = self.save_captcha_slider()

            self.solve_slider(captcha)
            deadstop += 1
            self.better_sleep((2, 3))
        if deadstop == 5:
            self.print("Unable to resolve the slider captcha", "red")
            self.set_status("Error")
            self.send_discord_message("Error in resolving the slider captcha.")
            while True:
                self.better_sleep((1, 1))
        elif deadstop != 0:
            self.print("Captcha successfully resolved!")

    @get_name
    def save_captcha_slider(self):
        captcha = self.adb.get_cv2_img()[139:511, 499 : 1280 - 353]

        for y in range(30):
            for i in range(captcha.shape[0]):
                captcha[y][i] = (255, 255, 255)

        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (10, 30)
        fontScale = 1
        color = (0, 0, 0)
        thickness = 2
        captcha = cv2.putText(
            captcha,
            "Click in center of puzzle",
            org,
            font,
            fontScale,
            color,
            thickness,
            cv2.LINE_AA,
        )

        return captcha

    @get_name
    def solve_slider(self, file=None):
        if file is None:
            file = f"captcha{self.sel}.jpg"

        if ss.application_settings.captcha.api_key:
            api_key = ss.application_settings.captcha.api_key
        else:
            api_key = ApiSingleton().getApiKey()

        solver = TwoCaptcha(api_key, defaultTimeout=120, pollingInterval=5)
        try:
            result = solver.coordinates(file, lang="en", hintText="Please locate the CENTER of the puzzle hole")

            self.debug(result)

            co = string_to_co_slide(result["code"])
            self.debug(co)
            slider_x, slider_y = self.find_img("slider_captcha")
            self.swipe_arg(slider_x + 25, slider_y, co[0] + 499, slider_y, 3000)
            self.better_sleep((2, 3))
        except Exception as e:
            self.debug(e)
            self.print("Cannot resolve this captcha slider!", ft.colors.RED)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
            traceback_str = "".join(traceback_list)

    def save_captcha(self):
        cv_image = self.adb.get_cv2_img()

        cropped_image = cv_image[100:460, 410:860]
        # cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
        # im_pil = Image.fromarray(cropped_image)
        # im_pil.save(f"captcha{self.sel}.jpg", optimize=True, quality=80)
        # self.better_sleep((0.5,0.5))
        # size = os.path.getsize(rf"{os.getcwd()}\captcha{self.sel}.jpg")
        # if size > 99999:
        #     self.print(f"Captcha is too big ({size}), refreshing it..")
        #     self.refresh_captcha()
        #     return self.save_captcha()
        #
        return cropped_image

    def refresh_captcha(self):
        co = self.find_img(target="refresh_resolve", confidence=0.9)
        # print(f"{co = }")
        if co is not None:
            x, y = co[0] + 5, co[1] + 5
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
        co = self.find_img(source=cv_image[280:370, :], target="already_connected", confidence=0.9)
        if co is not None:
            co = self.find_img(source=cv_image[720 // 2 :, 1280 // 3 : 1280 // 2], target="reconnect", confidence=0.9)
        if co is not None:

            if self.context_profile.log_back_from_device_switch.enabled:
                value = randint(
                    self.context_profile.log_back_from_device_switch.duration.min,
                    self.context_profile.log_back_from_device_switch.duration.max,
                ) * 60 + randint(0, 59)

                self.print(f"Waiting for the timer to end.. {value / 60:0.1f} minutes")
                self.better_sleep((value, value))
                self.click(1280 // 3 + co[0] + uniform(0, 50), 720 // 2 + co[1] + uniform(-10, 20))
                self.print("Reconnection..")
                self.better_sleep((5, 10))
                self.run_game()
                return True
            else:
                self.add_log("Auto Log-back off", ft.colors.RED)
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
        co = self.find_img(target="mightiest_gov", source=cv_image[: 720 // 3, 1280 // 2 :])
        if co is not None:
            self.click(co[0] + uniform(10, 30) + 1280 // 2, co[1] + uniform(10, 30))
            self.better_sleep((1.3, 2))
            cv_image = self.adb.get_cv2_img()
        return cv_image

    @get_name
    def close_osiris_popup(self, cv_image=None):
        if cv_image is None:
            cv_image = self.adb.get_cv2_img()
        if self.find_img(target="osiris_invitation", source=cv_image[: 720 // 2, 1280 // 4 : 1280 - 1280 // 4]):
            self.click(1280 / 2, 720 / 2)
            self.better_sleep((3.5, 4.7))
            self.click(960, 108)
            self.better_sleep((1.8, 2.7))
            cv_image = self.adb.get_cv2_img()
        return cv_image

    @get_name
    def check_reconnect(self, cv_image=None, cropped=False):
        """
        Check and reconnect
        """
        if cv_image is None:
            cv_image = self.adb.get_cv2_img()

        co = self.find_img(source=cv_image[: 720 // 2, :], target="network_disconnected", confidence=0.85)

        if co:
            print(f"Disconnect detected.. ({co})")
            if self.context_profile.log_back_from_error.enabled:
                value = randint(
                    self.context_profile.log_back_from_device_switch.duration.min,
                    self.context_profile.log_back_from_device_switch.duration.max,
                ) * 60 + randint(0, 59)

                self.print("You just got disconnected", ft.colors.AMBER)
                self.print(f"Waiting for the timer to end.. {value / 60:0.1f} minutes")
                self.better_sleep((value, value))

                co = self.find_img(target="reconnect", confidence=0.85)
                a = (co[0] + uniform(0, 100), co[1] + uniform(0, 20))
                print(f"Reconnect detected.. ({co})")

                self.click(a[0], a[1])
                self.print("Reconnection..")
                self.better_sleep((5, 10))
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
        limit = 30
        while condition and limit:
            self.run_game()
            screen = self.adb.get_cv2_img()
            if (
                self.find_img(target="menu_button", confidence=0.8, source=screen)
                or self.find_img(target="map_icon", confidence=0.8, source=screen)
                or self.find_img(target="hammer", confidence=0.8, source=screen)
                or self.find_img(target="inbox", confidence=0.8, source=screen)
            ):
                condition = False

            if co := self.find_img(target="mightiest_gov", confidence=0.8, source=screen):
                self.click(uniform(co[0] + 5, co[0] + 20), uniform(co[1] + 5, co[1] + 20))
                condition = False

            self.better_sleep((5, 5))
            self.close_windows()
            self.check_captcha_slider()
            self.check_captcha()

            screen = self.check_reconnect()
            self.check_log_back(screen)
            screen = self.close_upgrade_popup()
            screen = self.check_download_page(screen)
            screen = self.close_osiris_popup(screen)

            if self.find_img(target="reconnect_sdk", source=screen):
                self.leave_game()
                self.run_game()

            limit = limit - 1

            if not limit:
                self.leave_game()
                self.run_game()

    @get_name
    def close_upgrade_popup(self, source=None):
        if source is None:
            source = self.adb.get_cv2_img()
        for i in range(3):
            co = self.find_img(f"upgrade_popup_{i}", confidence=0.67, source=source)
            if co is not None:
                self.click(uniform(1102, 1030), uniform(92, 118))
                self.better_sleep((2, 4))
                source = self.adb.get_cv2_img()
        return source

    @get_name
    def leave_kd_buff(self, source=None):
        if source is None:
            source = self.adb.get_cv2_img()
        co = self.find_img(target="kingdom_buff", source=source[: 720 // 2, : 1280 // 2])
        if co is not None:
            self.click(uniform(70, 270), uniform(100, 542))
            self.better_sleep((1.8, 3))
            source = self.adb.get_cv2_img()
        return source

    def pil_to_array(self, image):
        try:
            cv_image = array(image)
            return cv_image
        except OSError:
            self.print("Cannot load the image..")
            self.better_sleep((1, 1))

            return self.pil_to_array(image)

    @get_name
    def check_chest(self):
        for _ in range(2):
            self.script_pause()
            cv_image = self.adb.get_cv2_img()
            cropped_image = cv_image[20:200, 400:]
            chest = None
            for i in range(1, 4):
                self.script_pause()
                chest = self.find_img(
                    target=f"verification_chest{i}",
                    source=cropped_image,
                    confidence=0.6,
                )
                if chest is not None:
                    break
            if chest is not None:
                if self.context_profile.captcha_solver.enabled:
                    # print(co)
                    self.click(400 + chest[0] + uniform(0, 10), 20 + chest[1] + uniform(0, 10))
                    self.better_sleep((3, 4))
                    return True
                else:
                    self.add_log(f"[{current_time()}] Captcha verification is Off")
                    self.set_status("Captcha is Off")
                    self.send_discord_message("Captcha detected, Captcha verification off.")
                    while True:
                        self.better_sleep((1, 1.1))

            self.better_sleep((0.3, 0.3))
        return False

    @get_name
    def check_captcha(self, chest=True, DefaultApiKey=True) -> bool:
        """
        Check and resolve verification
        """
        if not self.context_profile.captcha_solver.enabled:
            return True

        if chest:
            self.check_chest()
            self.better_sleep((1, 1.1))

        co = self.find_img(target="verification_button", confidence=0.6)

        if co is not None:
            self.click(co[0] + uniform(0, 40), co[1] + uniform(0, 10))
            self.better_sleep((2, 2.1))
            while self.find_img(target="close_refresh_ok", confidence=0.75) is None:
                co = self.find_img(target="verification_button")
                if co is not None:
                    self.click(co[0] + uniform(0, 80), co[1] + uniform(0, 20))
                self.better_sleep((2.4, 3))

        i = 0
        resolved = False
        previous_text = self.get_text()

        while self.find_img(target="close_refresh_ok", confidence=0.75) is not None:
            if not ss.application_settings.captcha.api_key:
                self.handle_captcha_limit()

            self.solve_captcha(i, DefaultApiKey)
            i += 1
            if i == 6:
                self.print("Error, unable to resolve the captcha for 5 times in a row !")
                self.send_discord_message("Error, unable to resolve the captcha for 5 times in a row. You have to solve it manually.")
                while self.find_img(target="close_refresh_ok", confidence=0.75):
                    self.better_sleep((10, 10))
            resolved = True

        self.set_status(previous_text)
        return resolved

    @get_name
    def solve_captcha(self, compteur: int = 0, DefaultApiKey: bool = True):
        try:
            self.print("Verification detected")
            self.set_status("Resolving captcha")

            if DefaultApiKey:
                api_key = ApiSingleton().getApiKey()
            else:
                api_key = ss.application_settings.captcha.api_key
                if api_key == "":
                    return self.print("This feature require a custom ApiKey")

            if ss.application_settings.captcha.api_key != "":
                api_key = ss.application_settings.captcha.api_key

            self.print("Trying to resolve the captcha")

            captcha = self.save_captcha()

            solver = TwoCaptcha(api_key, defaultTimeout=120, pollingInterval=5)

            result = solver.coordinates(captcha, lang="en")

            self.debug(result)

            co = string_to_co(result["code"])

            if self.adb.find_img_cv(captcha) is not None:
                for x, y in co:
                    self.click(x + 410, y + 100)
                    self.better_sleep((0.4, 0.795))

                self.click(uniform(700, 830), uniform(480, 520))
                self.better_sleep((1, 1.795))

            captchaId = result["captchaId"]
            self.better_sleep((3, 4))

            if self.find_img(target="close_refresh_ok", confidence=0.75) is None:
                resolved = True
            else:
                resolved = False

            if captchaId is not None:
                self.report_feedback(captchaId, resolved, solver)

        except NetworkException as e:
            self.print(e)
            print(e)
            self.print("An error occurred with your network, waiting for few seconds before retrying")
            self.better_sleep((10 * max(1, compteur + 1), 15 * max(1, compteur + 1)))

            if compteur < 5:
                return self.solve_captcha(compteur + 1)

        except TimeoutException as e:
            self.print(e)
            print(e)
            self.print("Request timeout, waiting for few seconds before retrying")
            self.better_sleep((10 * max(1, compteur + 1), 15 * max(1, compteur + 1)))

            if compteur < 5:
                return self.solve_captcha(compteur + 1)

        except ApiException as e:
            self.print(e)
            print(e)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
            traceback_str = "".join(traceback_list)
            self.print("An error occurred with 2captcha.com, waiting for few seconds before retrying")
            self.better_sleep((10 * max(1, compteur + 1), 15 * max(1, compteur + 1)))
            if self.refresh_captcha():
                if compteur < 5:
                    return self.solve_captcha(compteur + 1)

        except Exception as e:
            traceback.print_exc()
            self.print(f"Exception raised :\n{e}\n")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
            traceback_str = "".join(traceback_list)
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
    def leave_game(self, force=False) -> None:
        """
        Send adb signal to leave application
        """
        self.print(f"Leaving the game..")
        self.adb.shell("input keyevent KEYCODE_APP_SWITCH")
        self.better_sleep((2, 2.1))
        self.click(920, 62)
        self.better_sleep((2, 2.1))

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

        if self.find_img(target="download_page", source=screen[: 720 // 2, 1280 // 4 : 1280 - 1280 // 4], confidence=0.8):
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
            self.better_sleep((2, 3))

    @get_name
    def in_city(self) -> bool:
        """
        Check if the current view is set in the city
        :return: True if in city, False if not
        """
        return (
            self.find_img(
                target="checkpoint_star",
                source=self.adb.get_cv2_img()[:60, 380:600],
                confidence=0.97,
            )
            is None
        )

    def get_config(self):
        return self.context_profile

    @get_name
    def close_windows(self, screen=None):
        if screen is None:
            image = self.adb.get_cv2_img()

        while cos := self.adb.find_multiple_img(target="close_window", source=image[: 720 // 2, 1280 // 2 :]):
            co = cos[-1]
            self.adb.click(co[0] + uniform(3, 9) + 1280 // 2, co[1] + uniform(3, 9))
            self.better_sleep((1.3, 2.8))
            image = self.adb.get_cv2_img()

        while cos := self.adb.find_multiple_img(target="close_window2", source=image[: 720 // 2, : 1280 // 4], confidence=0.83):
            co = cos[-1]
            self.adb.click(co[0] + uniform(3, 9), co[1] + uniform(3, 9))
            self.better_sleep((1.3, 2.8))
            image = self.adb.get_cv2_img()

        while cos := self.adb.find_multiple_img(target="close_window3", source=image[: 720 // 2, 1280 // 2 :], confidence=0.83):
            co = cos[-1]
            self.adb.click(co[0] + uniform(3, 9) + 1280 // 2, co[1] + uniform(3, 9))
            self.better_sleep((1.3, 2.8))
            image = self.adb.get_cv2_img()

        while cos := self.adb.find_multiple_img(
            target="close_chat", source=image[720 // 4 : 720 - 720 // 4, : 1280 // 2 + 50], confidence=0.9
        ):
            co = cos[-1]
            self.adb.click(co[0] + uniform(3, 9), co[1] + uniform(3, 9) + 720 // 4)
            self.better_sleep((1.3, 2.8))
            image = self.adb.get_cv2_img()

    def get_text(self):
        return self.tile.get_text()

    def modify_image(self, re_open):
        img = cv2.resize(re_open, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

        if len(img.shape) == 2:
            img = cv2.merge([img, img, img])

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply a threshold to the image to make the text more visible
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        # Perform some morphological operations to remove noise and smooth the image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        dilate = cv2.dilate(opening, kernel, iterations=1)
        return dilate

    def get_neighboring_image(
        self,
        image,
        center_point,
        grid_width=1280,
        grid_height=720,
        up=50,
        left=20,
        right=60,
        down=85,
    ):
        """Gets the neighboring points around a center point on the grid."""
        x, y = center_point[0], center_point[1]
        min_x = max(0, x - left)
        max_x = min(grid_width - 1, x + right)
        min_y = max(0, y - up)
        max_y = min(grid_height - 1, y + down)

        return image[min_y:max_y, min_x:max_x]

    @get_name
    def recenter(self, deadstop=0, path="marauders.searching_radius"):
        image = self.adb.get_cv2_img()

        if co := self.find_img(source=image, target="green_home_button"):
            # reader = Reader()
            if (250 > co[0] > 130) and (co[1] > 560):
                return
            if deadstop == 10:
                self.click(co[0], co[1])
                self.better_sleep((2, 3))
                return
            x, y = co[0] - 10, co[1] - 10
            x2, y2 = co[0] + 50, co[1] + 50
            # Fill the specified region with dark gray color
            cv2.rectangle(image, (x, y), (x2, y2), (50, 50, 50), -1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = self.get_neighboring_image(image=image, center_point=co)
            first_try = image[0:35, :]
            second_try = image[-30:, :]

            word = ""

            first = self.extract_text(first_try, allowlist="0123456789KM")
            second = self.extract_text(second_try, allowlist="0123456789KM")
            # print(f"{first = } {second = }")
            # return
            if re.match(r"\d+KM", second):
                word = second
            if re.match(r"\d+KM", first):
                word = first
            if re.match(r"\d+KM", word):
                self.debug(word)
                # print(distances)
                # if distances:
                if word.split("KM")[0].isnumeric() and int(word.split("KM")[0]) > rgetattr(self.context_profile.tasks, path) + 15:
                    if co[0] < 500 and co[1] < 220:
                        self.swipe(co[0] + 90, co[1] + 90, 640, 360)
                        # self.swipe(330, 160, 760, 530)
                    elif co[0] < 500 and co[1] > 550:
                        # self.swipe(330, 530, 760, 160)
                        self.swipe(co[0] + 90, co[1] - 60, 640, 360)

                    elif co[0] > 800 and co[1] > 550:
                        # self.swipe(980, 530, 330, 160)
                        self.swipe(co[0] - 60, co[1] - 60, 640, 360)

                    elif co[0] > 800 and co[1] < 220:
                        # self.swipe(760, 160, 330, 530)
                        self.swipe(co[0] - 60, co[1] + 90, 640, 360)
                    elif co[0] <= 500:
                        # self.swipe_left()
                        self.swipe(co[0] + 90, co[1], 640, 360)
                    elif co[0] >= 800:
                        # self.swipe_right()
                        self.swipe(co[0] - 60, co[1], 640, 360)
                    elif co[1] >= 360:
                        # self.swipe_down()
                        self.swipe(co[0], co[1] - 60, 640, 360)
                    else:
                        # self.swipe_up()
                        self.swipe(co[0], co[1] + 90, 640, 360)

                    self.better_sleep((1, 2))
                    return self.recenter(deadstop=deadstop + 1, path=path)

    @get_name
    def go_back_to_city(self, deadstop=0):
        image = self.adb.get_cv2_img()

        if co := self.find_img(source=image, target="green_home_button"):
            self.click(co[0], co[1])
            self.better_sleep((2, 3))

            return

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

            return self.go_back_to_city(deadstop=deadstop + 1)

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
            if (
                (co[0] < 550 and co[1] < 100)
                or ((1180 < co[0] < 1235) and (520 < co[1] < 620))
                or ((1159 < co[0] < 1235) and (150 < co[1] < 195))
                or (co[0] < 556 and co[1] > 630)
                or (co[0] < 110 and co[1] > 495)
                or (co[0] > 1040 and co[1] < 160)
                or (co[1] > 515 and co[0] > 1175)
                or (co[0] < 120 and co[1] < 120)
                or (co[0] < 685 and co[1] > 615)
                or co[0] < 100
                or co[1] < 35
            ):
                co = None
        return co

    @get_name
    def adjusted_leave_city(self, x_click: int, y_click: int) -> None:
        self.zoom_out_city()
        self.better_sleep((1, 2))

        ##self.little_zoom_from_x_y(x_click, y_click)
        if self.validate_co((1280 - x_click, 720 - y_click)):
            self.swipe(1280 - x_click, 720 - y_click, 1280 // 2, 720 // 2)
        else:
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
        if self.find_img(target="search_button") is not None:
            self.print("Node not found")
            return False
        return True

    @get_name
    def find_cross(self, source=None, notify=True) -> bool:
        """
        :return: True if node is occupied or someone is coming to the node
        :return: False if node is free to gather
        """
        if notify:
            self.print("Scanning the node..")
        if source is None:
            source = self.adb.get_cv2_img()[230:480, 441:814]
        img = Image.fromarray(source)

        whitelist = [
            (0, 148, 192),
            (1, 149, 193),
            (49, 161, 255),
            (4, 144, 199),
            (5, 201, 2),
            (2, 143, 197),
            (4, 145, 193),
            (3, 145, 193),
            (4, 145, 194),
            (248, 157, 48),
            (3, 147, 197),
            (2, 146, 198),
            (2, 4, 183),
            (2, 143, 191),
            (3, 146, 196),
            (2, 143, 191),
            (3, 146, 196),
            (2, 143, 191),
            (3, 146, 196),
            (1, 208, 0),
            (5, 202, 2),
            (1, 208, 0),
            (3, 146, 198),
            (3, 145, 197),
            (3, 146, 198),
            (4, 143, 195),
            (1, 117, 178),
            (2, 145, 197),
            (2, 144, 195),
            (1, 118, 176),
            (1, 117, 177)
        ]
        occupied_colors = [
            (233, 233, 233),
            (247, 156, 47),
            (207, 131, 40),
            (248, 157, 48),
            (239, 205, 165),
            (0, 0, 178),
            (2, 204, 2),
            (195, 142, 0),
            (0, 154, 14),
            (0, 154, 13),
            (1, 186, 0),
            (0, 142, 193),
            (12, 154, 1),
            (1, 215, 0),
            (1, 216, 0),
            (253, 253, 253),
            (49, 161, 255),
            (2, 197, 2),
            (247, 210, 167),
            (255, 161, 49),
            (253, 253, 253),
            (167, 121, 28),
            (28, 121, 167),
            (92, 157, 246),
            (
                246,
                157,
                92,
            ),
            (101, 200, 43),
            (43, 200, 101),
            (106, 209, 46),
            (46, 209, 106),
            (2, 189, 2),
            (57, 159, 35),
            (35, 159, 24),
            (6, 187, 5),
            (107, 211, 46),
            (46, 211, 107),
            (49, 161, 255),
            (255, 161, 49),
            (14, 154, 0),
            (0, 154, 14),
            (71, 140, 195),
            (195, 140, 71)
        ]

        for i in range(img.size[0]):
            for y in range(img.size[1]):
                pixel = img.getpixel((i, y))
                if (
                    (
                        (pixel[0] < 5)
                        and (pixel[1] < 5)
                        and (175 < pixel[2] < 196)
                        and ((pixel[0] != 2) and (pixel[1] != 4) and (pixel[2] != 183))
                    )
                    or ((pixel[0] < 2) and (116 < pixel[1] < 119) and (175 < pixel[2] < 179))
                    # or ((pixel[0] < 5) and (142 < pixel[1] < 150) and (190 < pixel[2] < 200) and (pixel[2] != 193) and (pixel[2] != 192))
                    or ((pixel[0] < 10) and (pixel[1] > 187) and (pixel[2] < 10))
                    or (pixel in occupied_colors)
                ) and (pixel not in whitelist):
                    self.print(f"Node occupied, if you think it is a mistake, please report this: {pixel}")
                    return True
        return False

    @get_name
    def enough_action_points(self) -> bool:
        cv_image = self.adb.get_cv2_img()
        img = Image.fromarray(cv_image)

        pixel_color = img.getpixel((33, 73))

        print(pixel_color)

        condition1 = (pixel_color[0] <= 10) and (225 <= pixel_color[1] <= 255) and (120 <= pixel_color[2] <= 143)
        condition2 = pixel_color == (0, 255, 142)

        if condition1 or condition2:
            return True
        else:
            return False

    def run(self):
        raise NotImplemented("Run not implemented")
