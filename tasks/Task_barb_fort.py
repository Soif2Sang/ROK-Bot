from datetime import datetime
from random import randint, uniform
from time import sleep, time

import cv2
from PIL import Image

from tasks.Task import Task, current_time, get_name
from tasks.Task_heal_troop import HealTroop
from utils.functions import get_class
from utils.singletons import EmulatorSingleton


class BarbFort(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.sel, MainTask.contextManager)
        self.herite(MainTask)
        self.context_task = self.context_profile.tasks.alliance_fort
        self.rally_time = self.context_task.mobilisation_time
        self.rally_type = self.context_task.rally_type

    def task_name(self):
        return "BarbarianFort"

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
    def enough_action_points(self) -> bool:
        cv_image = self.adb.get_cv2_img()
        img = Image.fromarray(cv_image)
        print(img.getpixel((33, 73)))
        if (
            ((10 < img.getpixel((33, 73))[0] < 20) and (225 < img.getpixel((33, 73))[1] < 240) and (120 < img.getpixel((33, 73))[2] < 135))
            or (
                (10 < img.getpixel((33, 73))[2] < 20)
                and (225 < img.getpixel((33, 73))[1] < 240)
                and (120 < img.getpixel((33, 73))[0] < 135)
            )
            or (img.getpixel((33, 73)) == (0, 255, 142))
        ):
            return True
        else:
            return False

    @get_name
    def validate_co(self, co: tuple[int, int]) -> None | tuple[int, int]:
        # sourcery skip: merge-nested-ifs
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
        x_min = max(0, x - 30)
        x_max = min(cv_image.shape[1] - 1, x + 50)
        y_min = max(0, y - 40)
        y_max = min(cv_image.shape[0] - 1, y + 50)

        cropped_image = cv_image[y_min:y_max, x_min:x_max]

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
                if (
                    (
                        (img.getpixel((i, y))[0] < 5)
                        and (img.getpixel((i, y))[1] < 5)
                        and (img.getpixel((i, y))[2] > 175)
                        and (img.getpixel((i, y))[2] < 196)
                        and ((img.getpixel((i, y))[0] != 2) and (img.getpixel((i, y))[1] != 4) and (img.getpixel((i, y))[2] != 183))
                    )
                    or ((img.getpixel((i, y))[0] == 233) and (img.getpixel((i, y))[1] == 233) and (img.getpixel((i, y))[2] == 233))
                    or ((img.getpixel((i, y))[0] == 247) and (img.getpixel((i, y))[1] == 156) and (img.getpixel((i, y))[2] == 47))
                    or ((img.getpixel((i, y))[0] == 207) and (img.getpixel((i, y))[1] == 131) and (img.getpixel((i, y))[2] == 40))
                    or ((img.getpixel((i, y))[0] == 248) and (img.getpixel((i, y))[1] == 157) and (img.getpixel((i, y))[2] == 48))
                    or ((img.getpixel((i, y))[0] == 239) and (img.getpixel((i, y))[1] == 205) and (img.getpixel((i, y))[2] == 165))
                    or (
                        (img.getpixel((i, y))[2] < 179)
                        and (img.getpixel((i, y))[2] > 175)
                        and (img.getpixel((i, y))[1] > 116)
                        and (img.getpixel((i, y))[1] < 119)
                        and (img.getpixel((i, y))[0] < 2)
                    )
                    or (
                        (img.getpixel((i, y))[0] < 5)
                        and (img.getpixel((i, y))[1] > 142)
                        and (img.getpixel((i, y))[1] < 150)
                        and (img.getpixel((i, y))[2] < 200)
                        and (img.getpixel((i, y))[2] > 190)
                    )
                    or (img.getpixel((i, y)) == (0, 0, 178))
                    or (img.getpixel((i, y)) == (178, 0, 0))
                    or (img.getpixel((i, y)) == (2, 204, 2))
                    or (img.getpixel((i, y)) == (195, 142, 0))
                    or (img.getpixel((i, y)) == (0, 142, 195))
                    or (img.getpixel((i, y)) == (0, 154, 14))
                    or (img.getpixel((i, y)) == (0, 154, 13))
                    or (img.getpixel((i, y)) == (14, 154, 0))
                    or (img.getpixel((i, y)) == (13, 154, 0))
                    or (img.getpixel((i, y)) == (1, 186, 0))
                    or (img.getpixel((i, y)) == (0, 186, 1))
                    or (img.getpixel((i, y)) == (0, 142, 193))
                    or (img.getpixel((i, y)) == (193, 142, 0))
                    or (img.getpixel((i, y)) == (12, 154, 1))
                    or (img.getpixel((i, y)) == (1, 154, 12))
                    or (img.getpixel((i, y)) == (1, 215, 0))
                    or (img.getpixel((i, y)) == (1, 216, 0))
                    or (img.getpixel((i, y)) == (0, 215, 1))
                    or (img.getpixel((i, y)) == (0, 216, 1))
                    or (img.getpixel((i, y)) == (253, 253, 253))
                    or (img.getpixel((i, y)) == (49, 161, 255))
                    or (img.getpixel((i, y)) == (255, 161, 49))
                    or (img.getpixel((i, y)) == (2, 197, 2))
                    or (img.getpixel((i, y)) == (247, 210, 167))
                    or (img.getpixel((i, y)) == (255, 161, 49))
                    or (img.getpixel((i, y)) == (167, 210, 247))
                    or (img.getpixel((i, y)) == (49, 161, 255))
                    or (img.getpixel((i, y)) == (76, 150, 30))
                    or (img.getpixel((i, y)) == (30, 150, 76))
                    or img.getpixel((i, y)) in [(178, 118, 0), (0, 118, 178)]
                    or img.getpixel((i, y)) in [(167, 121, 28), (28, 121, 167)]
                    or img.getpixel((i, y)) in [(0, 143, 195), (195, 143, 0)]
                ):
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
        while self.find_img(target=f"{color}_icon", confidence=0.90) is None and self.find_img(target="troops_march_button") is not None:
            if deadstop == 5:
                self.click(uniform(1100, 1125), uniform(250, 270))
                self.better_sleep((0.557, 0.796))
                self.print("Error in line-up selection")
                self.set_status("Error in line-up selection")
                self.send_discord_message("Error in line-up selection, human interaction required.")

                while True:
                    self.script_pause()
                    sleep(1)
            self.click(uniform(1092, 1114), uniform(247, 267))
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

        if not self.context_task.marauders_mode:
            for second_string in ["left", "mid", "right"]:
                for first_string in ["up", "mid", "down"]:
                    # f"{screen}fort_icon_day_{first_string}_{second_string}"
                    co = self.find_img(
                        source=screen,
                        target=f"fort_icon_day_{first_string}_{second_string}",
                        confidence=0.8,
                    )
                    co = self.validate_co(co)
                    if co is None:
                        co = self.find_img(
                            source=screen,
                            target=f"fort_icon_night_{first_string}_{second_string}",
                            confidence=0.8,
                        )
                        co = self.validate_co(co)
                    if co is not None:
                        self.print(f"Fort Found - x: {co[0]} y:{co[1]}")

                        if self.already_mining(co[0], co[1], screen):
                            self.print("Someone is already rallying it")
                            continue
                        self.click(co[0], co[1])
                        x_click = co[0]
                        y_click = co[1]
                        self.better_sleep((2, 2.5))

                        self.check_captcha()
                        self.print("Scanning the fort..")
                        if self.find_cross():
                            self.print("Someone is already rallying it")
                            return self.adjusted_leave_city(x_click, y_click)
                        else:
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

                                    if self.rally_time == 5:
                                        self.click(fivemins[0], fivemins[1])
                                    if self.rally_time == 10:
                                        self.click(tenmins[0], tenmins[1])
                                    if self.rally_time == 30:
                                        self.click(thirtymins[0], thirtymins[1])

                                    self.better_sleep((0.7, 1.2))
                                    self.click(co[0] + uniform(0, 147), co[1] + uniform(0, 54))

                                    self.better_sleep((1.1, 1.5))
                                    self.select_lineup_color(color="red")
                                    self.better_sleep((0.7, 1.2))

                                    if self.context_task.rally_type == "inf":
                                        # self.click(uniform(982,998),uniform(280,298))
                                        # self.better_sleep((0.7, 1.2))
                                        self.click(uniform(680, 700), uniform(96, 117))
                                        self.better_sleep((0.7, 1.2))
                                    if self.context_task.rally_type == 'cav':
                                        # self.click(uniform(982,998),uniform(390,405))
                                        # self.better_sleep((0.7, 1.2))
                                        self.click(uniform(800, 815), uniform(96, 117))
                                        self.better_sleep((0.7, 1.2))
                                    if self.context_task.rally_type == 'archers':
                                        # self.click(uniform(982,998),uniform(330,350))
                                        # self.better_sleep((0.7, 1.2))
                                        self.click(uniform(905, 930), uniform(96, 117))
                                        self.better_sleep((0.7, 1.2))

                                    # self.click(uniform(657, 680), uniform(96, 117))
                                    # self.better_sleep((0.7, 1.2))
                                    self.click(uniform(1092, 1112), uniform(304, 320))
                                    self.better_sleep((2, 3))
                                    x, y = self.find_img(target="troops_march_button", confidence=0.8)
                                    cropped_image = self.adb.get_cv2_img()[y + 27 : y + 55, x : x + 120]

                                    string = self.extract_text(img=cropped_image, allowlist="1234567890:")

                                    # print(string)
                                    print(f"{string = }")
                                    datetime_object = datetime.strptime(string, "%H:%M:%S").time()
                                    print(datetime_object)
                                    self.print("Starting the rally..")
                                    self.click(x, y)
                                    self.better_sleep((2, 3))
                                    self.go_city()
                                    self.better_sleep((2, 3))
                                    self.print(f"You selected {self.rally_time} minutes")
                                    self.print(f"Rally leader marching time is {datetime.strptime(string, '%H:%M:%S').strftime('%S')}")
                                    self.print("Bot is now paused until the rally leader come back..")
                                    time_to_wait1 = int(self.rally_time) * 60 + int(datetime.strptime(string, "%H:%M:%S").strftime("%S"))
                                    time_to_wait2 = (
                                        int(self.rally_time) * 60 + int(datetime.strptime(string, "%H:%M:%S").strftime("%S")) * 2
                                    )
                                    self.print(
                                        f"Bot will wait around {time_to_wait2 / 60} minutes to complete the task, the bot will now sleep for this time"
                                    )
                                    for _ in range(time_to_wait2 * 10):
                                        self.script_pause()
                                        sleep(0.1)
                                    HealTroop(self).run()
                                    return True
        else:
            co = self.find_img(source=screen, target="maraudeurs_forts_icon", confidence=0.8)
            co = self.validate_co(co)
            if co is not None:
                self.print(f"Fort Found - x: {co[0]} y:{co[1]}")

                if self.already_mining(co[0], co[1], screen):
                    self.print("Someone is already rallying it")
                self.click(co[0], co[1])
                self.print(f"x = {co[0]} y = {co[1]}")
                x_click = co[0]
                y_click = co[1]
                self.better_sleep((2, 2.5))

                self.check_captcha()
                if self.find_cross():
                    self.print(f"Someone is already rallying it..")
                    return self.adjusted_leave_city(x_click, y_click)
                else:
                    bo1 = self.click_on_fort()
                    if not bo1:
                        self.print(f"Unable to click on the fort, leaving the fort !")
                        # return self.adjusted_leave_city(x_click, y_click)
                        return False
                    else:
                        self.better_sleep((1, 1.5))
                        co = self.find_img(target="fort_rally_button2")
                        if co is not None:
                            fivemins = (uniform(800, 925), uniform(188, 213))
                            tenmins = (uniform(960, 1088), uniform(188, 213))
                            thirtymins = (uniform(800, 925), uniform(238, 260))
                            if self.rally_time == 5:
                                self.click(fivemins[0], fivemins[1])
                            if self.rally_time == 10:
                                self.click(tenmins[0], tenmins[1])
                            if self.rally_time == 30:
                                self.click(thirtymins[0], thirtymins[1])
                            self.better_sleep((0.7, 1.2))
                            self.click(co[0] + uniform(0, 147), co[1] + uniform(0, 54))
                            self.better_sleep((1.1, 1.5))
                            self.select_lineup_color(color="red")
                            self.better_sleep((0.7, 1.2))
                            if self.rally_type == "inf":
                                # self.click(uniform(982,998),uniform(280,298))
                                # self.better_sleep((0.7, 1.2))
                                self.click(uniform(657, 680), uniform(96, 117))
                                self.better_sleep((0.7, 1.2))
                            if self.rally_type == "cav":
                                # self.click(uniform(982,998),uniform(390,405))
                                # self.better_sleep((0.7, 1.2))
                                self.click(uniform(770, 795), uniform(96, 117))
                                self.better_sleep((0.7, 1.2))
                            if self.rally_type == "archers":
                                # self.click(uniform(982,998),uniform(330,350))
                                # self.better_sleep((0.7, 1.2))
                                self.click(uniform(886, 906), uniform(96, 117))
                                self.better_sleep((0.7, 1.2))
                            self.click(uniform(1092, 1112), uniform(330, 350))
                            self.better_sleep((0.5, 1))
                            cv_image = self.adb.get_cv2_img()
                            x, y = self.find_img(
                                source=cv_image,
                                target="troops_march_button",
                                confidence=0.8,
                            )
                            self.print("Starting the rally..")
                            self.click(x, y)
                            self.better_sleep((0.5, 1))
                            self.go_city()
                            self.better_sleep((0.5, 1))
                            if self.context_task.skip_leader_back:
                                self.print("Skipping the commander back")
                                return True
                            self.print("Bot is now paused until the rally leader come back..")
                            self.print(f"You selected {self.rally_time} minutes")
                            self.click(1180, 173)
                            self.better_sleep((1.3, 1.8))
                            default_image = self.adb.get_cv2_img()
                            default_color = default_image[231, 383]
                            while (default_color == self.adb.get_cv2_img()[231, 383]).all():
                                self.better_sleep((3, 3))
                            self.close_windows()
                            # return self.heal_troops()
                            return True

    @get_name
    def swipe_scan(self, scan, direction):
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
        radius = self.context_task.searching_radius
        randomization = randint(0, 3)

        while randomization == last or None:
            randomization = randint(0, 3)

        self.print(f"The bot selected the path nº{randomization}.")

        coordinates = {
            0: (
                x - int((radius * (4 / 3))) + randint(2, 8),
                y + int((radius * (4 / 3))) + randint(-8, -2),
            ),
            1: (
                x + int((radius * (4 / 3))) + randint(-8, -2),
                y + int((radius * (4 / 3))) + randint(-8, -2),
            ),
            2: (
                x + int((radius * (4 / 3))) + randint(-8, -2),
                y - int((radius * (4 / 3))) + randint(2, 8),
            ),
            3: (
                x - int((radius * (4 / 3))) + randint(2, 8),
                y - int((radius * (4 / 3))) + randint(2, 8),
            ),
        }

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
                self.adb.get_device().shell(f"input text {self.data[str(self.sel)]['schedules'][self.current_profile].get('kingdom')}")
                self.better_sleep((0.3, 0.5))
        self.better_sleep((0.3, 0.5))
        for i in range(2):
            self.click(uniform(590, 685), uniform(130, 150))
            self.better_sleep((0.3, 0.5))
            if i == 0:
                string = f"input text {x2}"
                self.adb.get_device().shell(string)
                self.better_sleep((0.3, 0.5))
        self.better_sleep((0.3, 0.5))
        for i in range(2):
            self.click(uniform(750, 830), uniform(130, 150))
            self.better_sleep((0.3, 0.5))
            if i == 0:
                string = f"input text {y2}"
                self.adb.get_device().shell(string)
                self.better_sleep((0.3, 0.5))
        self.better_sleep((0.3, 0.5))
        for _ in range(2):
            self.click(uniform(860, 900), uniform(123, 158))
        self.better_sleep((1, 2))
        return randomization

    @get_name
    def go_random_area(self):
        position = self.context_task.map_center_pos

        raison = self.max_distance

        x = uniform(-raison, raison) + position.x
        y = uniform(-raison, raison) + position.y - 10

        self.click(x, y)
        self.better_sleep((1, 2))

    @get_class
    def run(self):
        if EmulatorSingleton().getEmulatorType() == "bluestacks":
            self.random_macro()

        # if not self.enough_action_points():
        #     self.print("Bot detected you are low in action point, bot prefers to not start a rally !")
        #     return

        self.run_game()
        self.check_captcha()
        self.check_reconnect()
        self.check_log_back()
        self.leave_kd_buff()

        self.leave_city()
        self.better_sleep((1.5, 2))
        self.zoom_out_city()

        if self.scan_fort():
            return

        starting_time = time()
        time_to_beat = starting_time + (60 * 60)
        self.max_distance = self.context_task.searching_radius / 6

        self.print(f"Bot will search a fort until : {datetime.fromtimestamp(time_to_beat).strftime('%H:%M:%S')}")
        while time_to_beat > time():
            if self.swipe_scan(self.scan_fort, self.go_random_area):
                return
