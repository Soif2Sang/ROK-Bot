import re
import traceback
from datetime import datetime
from random import uniform, randint, random, choice
from time import sleep, time

import cv2
from PIL import Image

from tasks.Task import Task
from tasks.Task_alliance_help import AllianceHelp
from utils.Task_utils import get_name, get_class


# from utils.easyOcr import Reader


class GatherGem(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.herite(MainTask)
        self.end_time = None
        self.block = False

    def task_name(self):
        return "GatherGem"

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
    def click_on_node(self) -> bool:
        """
        Click on node and click on send troop menu
        :return: True is successful
        :return: False is not successful
        """
        i = 0
        self.print("Clicking on the node..")
        while self.find_img(target="resource_gather_button", confidence=0.70) is None:
            x, y = uniform(610, 650), uniform(340, 388)
            self.click(x, y)
            self.better_sleep((0.725, 0.995))
            i = i + 1
            if i == 4:
                return False
        self.better_sleep((1.0, 1.395))
        co = self.find_img(target="resource_gather_button", confidence=0.70)
        if co is not None:
            x, y = co[0], co[1]
            self.click(x + uniform(0, 150), y + uniform(0, 30))
            self.better_sleep((1.325, 2.795))
            return True
        else:
            self.print("Unable to click on the node, leaving the node !")
            return False

    @get_name
    def select_lineup_color(self, color: str) -> None:
        """
        Change the line-up until the yellow line-up is selected.
        """
        deadstop = 0

        while self.find_img(target=f'{color}_icon', confidence=0.95) is None and self.find_img(
                target="troops_march_button") is not None:
            if deadstop == 5:
                self.click(uniform(700, 800), uniform(271, 300))
                self.better_sleep((0.557, 0.796))
                self.print("Error in line-up selection")
                self.set_text("Error in line-up selection")
                self.send_discord_message("Error in line-up selection, human interaction required.")
                while True:
                    self.script_pause()
                    sleep(0.1)
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
            self.run_game()
            # self.better_sleep((40, 60))
            self.check_captcha()
            self.leave_city()
            # print("premier leave city")
            self.better_sleep((1.5, 2))
            self.zoom_out_city()
            self.better_sleep((1.5, 2))
            self.scan_gem()
            self.better_sleep((0.125, 0.195))
            self.go_city(self.data[str(self.sel)]['schedules'][self.current_profile].get('city_x', 500),
                         self.data[str(self.sel)]['schedules'][self.current_profile].get('city_y', 500))

    @get_name
    def send_new_troop(self, deadstop: int = 0, color: str = 'yellow') -> bool:
        """
        Send a new troop to gather the gem node
        :return: True is successfully
        :return: False is not successfully
        """
        try:
            self.print("Trying to send new troop..")
            self.print(f"Send new troop count : {deadstop}")
            if deadstop == 5:
                self.click(uniform(700, 800), uniform(300, 500))
                self.better_sleep((1.325, 1.795))
                return False
            co = self.find_img(target="new_troops_button", confidence=0.70)
            if co is not None:
                # print("Home button found")
                x, y = co[0], co[1]
                x, y = x + uniform(0, 20), y + uniform(0, 20)
                self.click(x, y)
                self.better_sleep((1.825, 2.495))
                x_click, y_click = uniform(1090, 1111), uniform(329, 348)
                self.better_sleep((1.225, 1.795))
                self.select_lineup_color(color=color)
                default_image = self.adb.get_cv2_img()
                for i in range(7):  # change if you have 6-7 troops
                    default_color = default_image[282 + i * 54, 1100]
                    x_click, y_click = uniform(1096, 1118), uniform(282 + i * 54, 302 + i * 54)
                    self.click(x_click, y_click)
                    self.better_sleep((1, 2))
                    new_image = self.adb.get_cv2_img()
                    if (default_color != new_image[282 + i * 54, 1100]).all():
                        x, y = self.find_img(target="troops_march_button")
                        x, y = x + uniform(0, 20), y + uniform(0, 20)

                        self.click(x, y)
                        self.better_sleep((0.5, 0.7))
                        self.print("New Troop sent !", "green")
                        return True
                co = self.find_img(target="troops_march_button")
                if co is None:
                    return self.send_new_troop(deadstop=deadstop + 1)
                x, y = co[0], co[1]
                x, y = x + uniform(0, 20), y + uniform(0, 20)
                self.click(x, y)

                self.better_sleep((0.5, 0.7))
                self.print("New Troop sent !", "green")
                return True
            co = self.find_img(target="march_bar")
            if co is not None and self.free_troop_selection():
                return self.send_new_troop(deadstop=deadstop + 1)
            self.print("Unable to send a new troop", "red")
            return False
        except Exception as e:
            traceback.print_exc()
            self.print("Error sending a new march to the gem node !", "red")

    @get_name
    def send_nearest_troop_gem(self, deadstop=0) -> bool:
        """
        Send the nearest troop to gather the gem node
        :return: True if successfully
        """
        self.print("Trying to send the nearest troop..")
        try:
            for i in range(1, 4):
                points = self.adb.find_multiple_img(target=f"back_icon{i}", confidence=0.85)
                if points:
                    break
            if not points:
                return False

            if not self.data[str(self.sel)]['schedules'][self.current_profile].get('gather_gem_compare_march_duration'):
                self.click(points[0][0] + uniform(-20, 0), points[0][1] + uniform(-20, 0))
                self.better_sleep((1, 1.7))
                co = self.find_img(target="march_bar", confidence=0.8)
                if co:
                    self.click(co[0] + uniform(0, 30), co[1] + uniform(-5, +10))
                    self.better_sleep((1, 1.7))
                if self.find_img(target="troops_march_button") is not None:
                    self.click(x=uniform(1110, 1127), y=uniform(30, 55))
                    self.better_sleep((0.9, 1.3))
                    return self.send_new_troop()
                self.print("Troop sent to the node.", "green")
                return True

            timer = []
            for i in range(len(points)):
                self.click(points[i][0] + uniform(-20, 0), points[i][1] + uniform(-20, 0))
                self.better_sleep((1, 1.7))
                pil_image = self.adb.get_curr_device_screen_img()
                cv_image = self.pil_to_array(pil_image)
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
                co = self.find_img(source=cv_image, target="march_bar", confidence=0.7)
                if co is not None:
                    x, y = co[0], co[1]

                    cropped_image = cv_image[y + 27:y + 55, 956:1061]
                    cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                    # 991 996 1021 1027

                    # cv2.imwrite("test.png",cropped_image)
                    string = self.extract_text(img=cropped_image, allowlist="1234567890:")
                    # string = string.replace(":","")
                    print(string)

                    pattern = r'\d\d:\d\d:\d\d'  # Regular expression pattern

                    if not re.fullmatch(pattern, string):
                        string = '23:23:23'
                    datetime_object = datetime.strptime(string, '%H:%M:%S').time()
                    timer.append(
                        [datetime_object, (points[i][0] + uniform(-20, 0), points[i][1] + uniform(-20, 0)), (x, y)])
                else:
                    return False
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

            if self.find_img(target="troops_march_button") is not None:
                self.click(x=uniform(1110, 1127), y=uniform(30, 55))
                self.better_sleep((0.9, 1.3))
                return self.send_new_troop()
            self.print("Nearest troop sent to the node..", "green")
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
        return self.find_cross(source)

    def commander_selection_down(self):
        self.swipe_arg(1220, 360, 1220, 230, randint(1000, 1500))

    def commander_selection_up(self):
        self.swipe_arg(1220, 230, 1220, 360, randint(1000, 1500))

    def get_neighboring_image(self, image, center_point, grid_width=1280, grid_height=720, up=50, left=20, right=60,
                              down=85):
        """Gets the neighboring points around a center point on the grid."""
        x, y = center_point[0], center_point[1]
        min_x = max(0, x - left)
        max_x = min(grid_width - 1, x + right)
        min_y = max(0, y - up)
        max_y = min(grid_height - 1, y + down)

        return image[min_y:max_y, min_x:max_x]

    @get_name
    def check_if_interrupt(self):
        if not self.adb.is_game_alive():
            return True
        self.check_download_page()
        self.leave_kd_buff()
        self.check_captcha()
        if self.check_log_back():
            return True
        return False

    @get_name
    def send_troop_to_node(self):
        if self.free_troop_selection():
            self.click(uniform(1172, 1222), uniform(77, 112))

        self.better_sleep((1.3, 2))

        if self.send_new_troop():
            return True
        if self.send_nearest_troop_gem():
            if self.find_img(target="new_troops_button", confidence=0.70):
                self.send_new_troop()
            return True
        self.click(uniform(400, 700), uniform(300, 400))
        self.better_sleep((1.8, 3))
        self.check_captcha()
        self.close_windows()
        return False

    @get_name
    def scan_gem(self):
        """
        Scan device screenshot to find gem node,          not 100% working need improvement
        :return: None
        """
        self.restart_if_game_crashed()
        screen = self.adb.get_cv2_img()

        # info_screen = screen[470:700, 0:115]
        # cropped_image = screen[420:540, 480:810]
        #
        # if random() > 0.7:
        #     co = self.find_img(source=screen, target="verification_button", confidence=0.8)
        #     if co is not None:
        #         self.check_captcha()
        #     self.check_reconnect(cropped_image)
        #
        # if random() > 0.4:
        #     self.check_download_page(screen)
        #     self.leave_kd_buff(screen)
        #
        # cropped_image = screen[616:710, 1168:1270]
        #
        # if self.find_img(source=cropped_image, target="map_icon", confidence=0.8) is not None:
        #     self.click(uniform(500, 700), uniform(250, 450))
        #     self.better_sleep((1, 2))
        #     return self.zoom_out_city()
        #
        # if self.find_img(source=info_screen, target="hammer", confidence=0.8) is not None:
        #     self.click(uniform(24, 91), uniform(625, 680))
        #     self.better_sleep((1.5, 2))
        #     self.zoom_out_city()
        #     self.better_sleep((2, 3))
        #     screen = self.adb.get_cv2_img()
        #
        # if self.find_img(source=info_screen, target="gem_search_button", confidence=0.8) is not None:
        #     self.zoom_out_city()
        #     self.better_sleep((2, 3))
        #     screen = self.adb.get_cv2_img()
        icons = []
        co = None
        for second_string in ["left", "mid", "right"]:
            for first_string in ["up", "mid", "down"]:
                icons.append([f"gem_icon_day_{first_string}_{second_string}",f"gem_icon_night_{first_string}_{second_string}"])
        for icon in icons:
            co = self.validate_co(
                self.find_img(source=screen, target=icon[0], confidence=0.77))
            if co is None:
                co = self.validate_co(
                    self.find_img(source=screen, target=icon[1], confidence=0.77))
            if co is not None:
                self.print(f"Gem node Found - x: {co[0]} y:{co[1]}")
                if self.already_mining(co[0], co[1], screen):
                    self.print(f"Already mining this gem node")
                    co = None
            if co:
                break
        if co:
            self.print(f"Node x:{co[0]}, y:{co[1]}")
            self.click(co[0], co[1])
            x_click = co[0]
            y_click = co[1]
            self.better_sleep((2, 2.5))

            default = True
            blocked = False

            while not blocked:
                if self.check_if_interrupt():
                    return self.run(self.end_time)

                screen = self.adb.get_cv2_img()
                cv_image = screen[0:100, 0:800]
                if self.find_img(target="block_icon", source=cv_image, confidence=0.9) is not None:
                    self.print("Bot detected the block icon, now cancelling the function..")
                    self.block = True
                    return

                if self.find_cross():
                    break

                if not self.data[str(self.sel)]['schedules'][self.current_profile].get("gather_gem_swipe_check"):
                    if not self.click_on_node():
                        break
                    if self.send_troop_to_node():
                        break

                    scan_frequency = randint(
                        self.data[str(self.sel)]['schedules'][self.current_profile].get("gem_check1"),
                        self.data[str(self.sel)]['schedules'][self.current_profile].get("gem_check2")
                    )

                    self.print(f"Script is paused for {scan_frequency} seconds")
                    scan_frequency_timer = 0
                    random_wait = uniform(20, 30)
                    for i in range(scan_frequency):
                        self.better_sleep((1, 1))
                        scan_frequency_timer += 1
                        if scan_frequency_timer >= random_wait:
                            if self.check_if_interrupt():
                                return self.run(self.end_time)

                            timer_image = self.adb.get_cv2_img()
                            cross_image = timer_image[240:490, 490:790]
                            back_image = timer_image[150:477, 1160:]

                            if self.find_cross_source(cross_image):
                                break
                            if self.find_img(target="back_normal_view", source=back_image,
                                             confidence=0.9) is not None or \
                                    self.free_troop_commander_list():
                                self.print("This node can be gathered.")
                                break
                            if self.data[str(self.sel)]['schedules'][self.current_profile].get('alliance_help'):
                                AllianceHelp(self).run()
                            scan_frequency_timer = 0
                else:

                    if not self.adb.is_game_alive():
                        self.run_game()
                        return self.run(self.end_time)

                    if self.find_img(target="back_normal_view", confidence=0.9) is not None or \
                            self.free_troop_commander_list():
                        self.print("This node can be gathered.")
                        if not self.click_on_node():
                            break
                        if self.send_troop_to_node():
                            break

                    if self.find_img(target="extend_troops", confidence=0.9) is not None:
                        if default:
                            self.commander_selection_down()
                        else:
                            self.commander_selection_up()

                    if self.find_img(target="back_normal_view", confidence=0.9) is not None or \
                            self.free_troop_commander_list():
                        self.print("This node can be gathered.")
                        if not self.click_on_node():
                            break
                        if self.send_troop_to_node():
                            break

                    if self.find_img(target="extend_troops", confidence=0.9) is not None:
                        if default:
                            self.commander_selection_down()
                        else:
                            self.commander_selection_up()

                    if self.find_img(target="back_normal_view", confidence=0.9) is not None or \
                            self.free_troop_commander_list():
                        self.print("This node can be gathered.")
                        if not self.click_on_node():
                            break
                        if self.send_troop_to_node():
                            break

                    default = not default

                    # random_wait = uniform(20, 30)
                    self.better_sleep((15, 30))
                    if self.check_if_interrupt():
                        return self.run(self.end_time)

                    if self.data[str(self.sel)]['schedules'][self.current_profile].get('alliance_help'):
                        AllianceHelp(self).run()
            self.better_sleep((1, 1.895))
            self.check_captcha()
            self.close_windows()
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
    def go_city(self, x, y, last=None) -> int:
        """
        Define starting path
        :param: x -> int x map location
        :param: y -> int y map location
        :return: starting location between 0,1,2,3
        """
        x2, y2 = x + randint(-2, 2), y + randint(-2, 2)
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

    @get_name
    def swipe_scan(self, scan, direction):
        # print(f'[ {current_time()} ] [ {self.name} ] {direction = } {scan = }')
        direction()
        screen = self.adb.get_cv2_img()

        info_screen = screen[470:700, 0:115]
        cropped_image = screen[420:540, 480:810]

        if random() > 0.7:
            co = self.find_img(source=screen, target="verification_button", confidence=0.6)
            if co is not None:
                self.check_captcha()
            self.check_reconnect(screen)

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

        self.better_sleep((0.5, 0.7))
        return scan()

    def recenter(self, deadstop=0):
        if self.data[str(self.sel)]['schedules'][self.current_profile].get('recenter_feature', False):
            return super().recenter(deadstop)

    @get_class
    def run(self, end_time=None):
        pass