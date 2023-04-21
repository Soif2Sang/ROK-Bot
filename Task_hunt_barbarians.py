import json
from time import sleep

import numpy as np
from PIL import Image
from numpy import array
from random import uniform, choice, randint

import cv2
from pytesseract import pytesseract

from Task import Task
from Task_utils import get_name, get_class, current_time, get_data

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class HuntBarbarians(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.data = get_data()
        self.current_profile = MainTask.current_profile
        self.frame = MainTask.tile
        self.adb = MainTask.adb
        self.ppid = MainTask.ppid
        self.pid = MainTask.pid
        self.language = MainTask.language
        self.name = MainTask.name
        self.sel = MainTask.sel

    def task_name(self):
        return "HuntBarbarians"

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
    def send_new_troop(self, deadstop: int = 0, color: str = 'yellow') -> bool:
        """
        Send a new troop to gather the gem node
        :return: True is successfully
        :return: False is not successfully
        """

        self.print("Trying to send new troop..")
        self.print(f"Send new troop count : {deadstop}")
        if deadstop == 5:
            self.click(uniform(700, 800), uniform(300, 500))
            self.better_sleep((1.325, 1.795))
            return False
        self.check_if_kill()
        co = self.find_img(target="new_troops_button")
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
                        x, y = self.find_img(target="troops_march_button")
                        x, y = x + uniform(0, 20), y + uniform(0, 20)
                        self.check_if_kill()
                        self.click(x, y)
                        self.better_sleep((0.5, 0.7))
                        self.print("New Troop sent !")
                        return True

                # if self.find_img(target="choose_right", confidence=0.8):
                #     x, y = self.find_img(target="troops_march_button")
                #     x, y = x + uniform(0, 20), y + uniform(0, 20)
                #     self.check_if_kill()
                #     self.click(x, y)
                #     self.better_sleep((0.5, 0.7))
                #     return True
            self.check_if_kill()
            co = self.find_img(target="troops_march_button")
            if co is None:
                return self.send_new_troop(deadstop=deadstop + 1)
            x, y = co[0], co[1]
            x, y = x + uniform(0, 20), y + uniform(0, 20)
            self.click(x, y)
            self.check_if_kill()
            self.better_sleep((0.5, 0.7))
            self.print("New Troop sent !")
            return True
        co = self.find_img(target="march_bar")
        if co is not None and self.free_troop_gem():
            x, y = uniform(1177, 1250), uniform(80, 116)
            self.check_if_kill()
            self.better_sleep((0.5, 0.7))
            return self.send_new_troop(deadstop=deadstop + 1)
        self.print("Unable to send a new troop")
        return False

    @get_name
    def deploy_hunter(self):
        # top_left = (415,202)
        # top_right = (840,202)
        # bottom_left =(415,530)
        # top_left = (840,530)
        # list = []
        full_area = [(i, y) for i in range(420, 840, 5) for y in range(200, 530, 5) if not (795 > i > 490 and 210 < y < 490)]
        # forbidden_area = [(i, y) for i in range(490, 795,5) for y in range(230, 490,5)]
        # for element in forbidden_area:
        #     try:
        #         full_area.remove(element)
        #     except:
        #         pass
        # print("done")

        full_sent = False
        hunters = 0
        while not full_sent:
            co = choice(full_area)
            print("done", co)
            self.swipe_arg(co[0], co[1], co[0], co[1], randint(2500, 3475))
            self.better_sleep((1.325, 1.795))
            co = self.find_img(target="deploy_march_button")
            if co is not None:
                self.click(co[0] + uniform(0, 140), co[1] + uniform(0, 4))
                self.better_sleep((1.325, 1.795))
                if self.find_img(target="new_troops_button"):
                    self.send_new_troop(color='red')
                    hunters += 1
                else:
                    self.click(uniform(150, 500), uniform(150, 500))
                    full_sent = True
                self.better_sleep((1.325, 1.795))
        return hunters

    @get_name
    def enough_action_points(self) -> bool:
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = self.pil_to_array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
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
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = self.pil_to_array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        co = self.find_img(source=cv_image, target="button_level", confidence=0.8)
        if co is None:
            self.print(f'Cannot find the button_level')
            # self.set_text(f"[{current_time()}] Cannot find the level button")
            self.click_loop()
            self.better_sleep((1, 1.2))
        else:
            # x,y = uniform(225,285) , uniform(607,667)
            # self.click(x,y)
            self.better_sleep((1, 1.3))
            cv_image = cv_image[co[1] - 30:co[1], co[0] - 40:co[0] + 40]
            # cv2.imwrite("level.png", cv_image)
            string = pytesseract.image_to_string(cv_image,
                                                 config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=level:1234567890')
            string = string.replace("\n", "")
            string = string.split(":")
            self.print(f'Current level : {string[1]}')
            # self.set_text(f"[{current_time()}] Current level : {string[1]}")
            level_to_go = level - int(string[1])
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
                self.better_sleep((0.115, 0.300))
            return

    @get_name
    def check_ap_box(self) -> bool:
        self.print(f'Check if AP pop-op box is detected')
        if self.find_img(target="ap_bottle"):
            co = self.find_img(target="daily_ap_claim")
            if co is None:
                co = self.find_img(target="close_window")
                self.click(co[0], co[1])
                self.better_sleep((1.325, 1.795))
            else:
                x, y = co[0] + uniform(0, 30), co[1] + uniform(0, 20)
                self.click(x, y)
            self.better_sleep((1.325, 1.795))
            co = self.find_img(target="close_window")
            if co is not None:
                self.click(co[0], co[1])
                self.better_sleep((1.325, 1.795))
            self.print(f'Detected')
            return True
        self.print(f'Not detected')
        return False

    @get_name
    def wait_until_kill(self):
        self.print(f"Waiting for the troops to kill the barbarian..")
        while self.find_img(target="troop_idle") is None or self.find_img(target="troop_walking") is not None:
            self.script_pause()
            self.check_log_back()
            self.check_reconnect()
            self.check_if_kill()
            self.check_captcha()
            self.better_sleep((3, 5))
            print(f"[ {current_time()} ] [ {self.name} ] Waiting for the troops to kill the barbarian..")

    @get_name
    def recall(self, nb_troop: int) -> bool:
        self.print('Recalling troops')
        print(nb_troop)
        x, y = uniform(1170, 1183), uniform(160, 175)
        self.click(x, y)
        self.better_sleep((1.595, 2))
        nb_to_go = nb_troop
        breakint = 0
        while nb_to_go > 0:
            print(nb_to_go)
            co = self.find_img(target="return_button")
            while co is None and breakint != 4:
                print(
                    f'[ {current_time()} ] [ {self.name} ] Return button not found')

                y, x = uniform(290, 480), uniform(460, 560)
                x2, y2 = x + uniform(-30, 30), y + uniform(-200, -100)
                self.swipe(x, y, x2, y2)
                self.better_sleep((2, 3))
                co = self.find_img(target="return_button")
                breakint += 1
            if co is not None:
                self.click(co[0] + uniform(0, 10), co[1] + uniform(0, 10))
            self.better_sleep((1.695, 2))
            nb_to_go = nb_to_go - 1
        sleep(0.5)
        x, y = uniform(1080, 1093), uniform(72, 88)
        self.click(x, y)
        return True

    @get_class
    def run(self):
        wanted_level = 24
        hunter_selection = False
        self.leave_city()
        self.better_sleep((1, 1.3))
        nb_hunter = self.deploy_hunter()
        if nb_hunter == 0:
            return
        while self.enough_action_points():
            self.better_sleep((1.5, 3))

            self.click_loop()  # Clicking on the loop
            self.better_sleep((1, 2))
            x, y = uniform(225, 285), uniform(607, 667)

            self.click(x, y)  # Selecting the barbarian section
            self.better_sleep((1, 1.3))
            self.set_search_level(wanted_level)  # Setting the barbarian level to the desired level

            x, y = uniform(200, 330), uniform(466, 506)
            self.click(x, y)  # Searching the barbarian
            self.better_sleep((1, 2))

            reduced_level = wanted_level
            while self.find_img(target="search_button") is not None:
                reduced_level = reduced_level - 1
                self.set_search_level(reduced_level)

                x, y = uniform(200, 330), uniform(466, 506)
                self.click(x, y)  # Searching the barbarian

                self.better_sleep((1, 2))
            wanted_level = reduced_level
            self.click(1280 // 2 + uniform(-10, 10), 720 // 2 + uniform(-10, 10))  # Selecting the barbarian
            self.better_sleep((1, 1.4))
            button_attack = self.find_img(target="attack_button")
            if button_attack is None:
                continue  # Skipping all the code bellow to re-execute the barbarian search
            self.click(button_attack[0] + uniform(0, 170), button_attack[1] + uniform(0, 40))
            self.better_sleep((1.5, 2))

            if not hunter_selection:
                self.print(f'Selecting the whole troops from scratch')
                self.better_sleep((2, 3))
                x, y = uniform(1163, 1180), uniform(670, 685)
                self.click(x, y)
                self.better_sleep((2.2, 3.5))
                tab = self.adb.find_multiple_img("selected_icon")
                tab = tab[nb_hunter:-1]
                for element in tab:
                    x, y = element[0] + uniform(0, 5), element[1] + uniform(0, 5)
                    self.click(x, y)
                    self.better_sleep((0.3, 0.5))
                hunter_selection = True
                self.click(uniform(1163, 1183), uniform(665, 685))
                self.better_sleep((1.2, 1.5))

            self.print('Selecting the whole troops')
            self.better_sleep((2, 3))
            self.click(uniform(1163, 1183), uniform(665, 685))
            self.better_sleep((1.2, 1.5))

            self.click(uniform(940, 1075), uniform(640, 670))
            self.better_sleep((1.2, 1.5))
            self.print(f'Check if AP pop-op box is detected')
            if self.check_ap_box():
                self.print('Pop-up found, recalling troops')
                break

            self.check_captcha()
            self.wait_until_kill()
        self.check_ap_box()
        self.recall(nb_troop=nb_hunter)
