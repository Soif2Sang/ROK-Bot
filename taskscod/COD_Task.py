import os
import sys
from datetime import date
from random import uniform, randint
from time import sleep
from PIL import ImageFile
from numpy import array, ndarray

from utils.functions import get_window_pid, get_name, current_time, FileSingleton

ImageFile.LOAD_TRUNCATED_IMAGES = True


class Task:
    def __init__(self, tile):
        self.FileSingleton = FileSingleton()
        self.data = self.FileSingleton.get_data()
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
        self.data = self.FileSingleton.get_data()
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
        print(f"[ {date.today()} {current_time()} ] [ {self.name} ] Loading {target}")
        result = self.adb.find_img(target=target,source=source,confidence=confidence)
        print(f"Successfully loaded {target}")
        # print(f"[ {date.today()} {current_time()} ] [ {self.name} ] Successfully loaded {target}")

        return result 
    
    @get_name
    def run_game(self, count=0) -> None:
        if (co := self.find_img(target="codicon", confidence=0.8)):
            self.print(f"Looks like game is not running")
            self.click(co[0] + 10, co[1] + 10)
            sleep(3)
            return self.wait_until_connected()
        return
        print(self.adb.is_game_alive())
        a = self.adb.is_game_alive()
        if not a:
            self.print(f"Looks like game is not running")
            co = self.find_img(target="codicon", confidence=0.8)
            if co is not None:
                self.click(co[0] + 10, co[1] + 10)
                sleep(3)
                return self.wait_until_connected()
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

    def script_pause(self):
        said = False

        if self.tile.stopped:
            self.tile.stopped = False
            self.set_text(f"[{current_time()}] You stopped the bot","Red")
            print(f"[ {date.today()} {current_time()} ] [ {self.name} ] You stopped the bot")
            sys.exit(1)

        while not self.tile.paused:
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
        return False
        # print(f'{self.data.get(self.sel).get("auto_log_back"] =}')
        if cv_image is None:
            cv_image = self.adb.get_cv2_img()
            # print(f'{co}')
        co = self.find_img(source=cv_image, target="already_connected", confidence=0.9)
        if co is not None:
            if cv_image is None:
                co = self.find_img(target="reconnect")
            else:
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
    def check_mge(self):
        co = self.find_img(target="mightiest_gov")
        if co is not None:
            self.click(co[0] + uniform(10, 30), co[1] + uniform(10, 30))
            self.better_sleep((1.3, 2))

    @get_name
    def check_reconnect(self, cv_image=None):
        return
        """
        Check and reconnect
        """

        if cv_image is None:
            co = self.find_img(target="reconnect")
        else:
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

    @get_name
    def wait_until_connected(self) -> None:
        self.print("Script is paused until game is fully loaded..")
        condition = True
        while condition:
            self.run_game()
            if self.find_img(target="cod_toolbar_button", confidence=0.8):
                condition = False
            self.better_sleep((10, 15))
            self.close_windows()

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
        cv_image = self.adb.get_cv2_img()
        return self.find_img(target='cod_city_hammer',source=cv_image,confidence=0.9) is not None

    @get_name
    def close_windows(self):
        image = self.adb.get_cv2_img()[0:322, 0:1280]
        while (co:=self.find_img(target="cod_close_window_2",source=image)):
            self.adb.click(co[0]+uniform(3,9),co[1]+uniform(3,9))
            self.better_sleep((1.3,2.8))
            image = self.adb.get_cv2_img()[0:322, 0:1280]
        while (co:=self.find_img(target="cod_close_window",source=image)):
            self.adb.click(co[0]+uniform(3,9),co[1]+uniform(3,9))
            self.better_sleep((1.3,2.8))
            image = self.adb.get_cv2_img()[0:322, 0:1280]

    def get_text(self):
        return self.tile.get_text()
