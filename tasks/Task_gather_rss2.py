import re
import traceback
from random import uniform, random
from time import sleep

import cv2
from PIL import Image

from tasks.Task import Task
from utils.Task_utils import get_name, get_class


# from utils.easyOcr import Reader


class GatherRss2(Task):
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

    def task_name(self):
        return "GatherRss2"

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

        self.zoom_out_city()

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
    def find_cross(self, source=None) -> bool:
        """
        :return: True if node is occupied or someone is coming to the node
        :return: False if node is free to gather
        """
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
                    self.print(f"{img.getpixel((i, y))}")
                    self.print("Node occupied")
                    return True
        return False

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
            self.better_sleep((40, 60))
            self.check_captcha()
            self.leave_city()
            # print("premier leave city")
            self.better_sleep((1.5, 2))
            self.zoom_out_city()
            self.better_sleep((1.5, 2))
            self.scan_node()
            self.better_sleep((0.125, 0.195))
            self.go_to(self.data[str(self.sel)]['schedules'][self.current_profile].get('city_x', 500),
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
            self.print("Error sending a new march to the node !", "red")

    @get_name
    def send_troop(self) -> bool:
        self.better_sleep((1.8, 3))
        self.print("Trying to send a new troop..")
        if self.data[str(self.sel)]['schedules'][self.current_profile]['rss_custom_preset']:
            self.send_new_troop()
            self.better_sleep((0.7, 1.1))
        else:
            co = self.find_img(target="new_troops_button", confidence=0.7)
            if co is None:
                return False
            x, y = co[0], co[1]
            x, y = x + uniform(0, 160), y + uniform(0, 30)
            self.click(x, y)
            self.better_sleep((2.325, 2.795))
            x, y = self.find_img(target="troops_march_button")
            x, y = x + uniform(0, 80), y + uniform(0, 20)
            self.click(x, y)
            self.better_sleep((1.1, 2))
        if self.find_img(target="troops_march_button") is not None:
            self.click(uniform(1106, 1123), uniform(36, 55))
            self.better_sleep((1.1, 1.5))
            self.print("Cannot send the troop")
            return False
        self.print("Troop sent !", "green")
        return True

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
    def recenter(self):
        image = self.adb.get_cv2_img()
        if (co := self.find_img(source=image, target="green_home_button")):
            # reader = Reader()

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
            print(word)
            if re.match(r'\d+KM', word):
                if word.split("KM")[0].isnumeric() and int(word.split("KM")[0]) > int(
                        self.data[str(self.sel)]['schedules'][self.current_profile].get('radius', 40)) * 1.5:
                    if co[0] < 500 and co[1] < 220:
                        self.swipe(330, 160, 760, 530)
                    elif co[0] < 500 and co[1] > 550:
                        self.swipe(330, 530, 760, 160)
                    elif co[0] > 800 and co[1] > 550:
                        self.swipe(980, 530, 330, 160)
                    elif co[0] > 800 and co[1] < 220:
                        self.swipe(760, 160, 330, 530)
                    elif co[0] < 500:
                        self.swipe_left()
                    elif co[0] > 800:
                        self.swipe_right()
                    elif co[1] > 360:
                        self.swipe_down()
                    elif co[1] < 360:
                        self.swipe_up()
                    self.better_sleep((1, 2))
                    return self.recenter()

    @get_name
    def scan_node(self, param=None):
        """
        Scan device screenshot to find gem node,          not 100% working need improvement
        :return: None
        """
        self.restart_if_game_crashed()
        screen = self.adb.get_cv2_img()
        nodes = self.adb.find_multiple_img(source=screen,
                                           target=f"{self.data[str(self.sel)]['schedules'][self.current_profile][self.node_type]}_icon_zoom",
                                           confidence=0.7)
        print(nodes)
        print(f"{self.data[str(self.sel)]['schedules'][self.current_profile][self.node_type]}_icon")
        nodes = filter(self.validate_co, nodes)
        for co in list(nodes):
            if co is not None:
                self.print(f"Gem node Found - x: {co[0]} y:{co[1]}")
                if self.already_mining(co[0], co[1], screen):
                    self.print(f"Already mining this gem node")
                    continue
                self.print(f"Node x:{co[0]}, y:{co[1]}")
                self.click(co[0], co[1])
                x_click = co[0]
                y_click = co[1]
                self.better_sleep((2, 2.5))
                self.check_captcha()
                self.check_download_page()
                self.leave_kd_buff()
                if self.check_log_back():
                    self.print("You interrupted gem gathering by connecting from an other device, bot is restarting it")
                    return self.run(self.end_time)
                screen = self.adb.get_cv2_img()
                cv_image = screen[0:100, 0:800]
                if self.find_img(target="block_icon", source=cv_image, confidence=0.9) is not None:
                    self.print("Bot detected the block icon, now cancelling the function..")
                    self.block = True
                    return

                if self.find_cross():
                    return self.adjusted_leave_city(x_click, y_click)

                if not self.click_on_node():
                    return self.adjusted_leave_city(x_click, y_click)

                if self.free_troop_selection():
                    self.click(uniform(1172, 1222), uniform(77, 112))
                    # self.better_sleep((0.6, 1))

                self.better_sleep((1.3, 2))

                if self.send_troop():
                    self.node_type = self.next_resource_type(self.node_type)
                    print(self.node_type)
                return self.zoom_out_city()

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

        self.better_sleep((0.5, 0.7))
        return scan()

    @get_name
    def next_resource_type(self, place: str) -> str:
        # print(f'[ {current_time()} ] [ {self.name} ] next_resource_type call')
        if place == "First":
            return "Second"
        elif place == "Second":
            return "Third"
        elif place == "Third":
            return "Fourth"
        elif place == "Fourth":
            return "Fifth"
        elif place == "Fifth":
            return "Sixth"
        elif place == "Sixth":
            return "Seventh"
        elif place == "Seventh":
            return "Done"

    @get_class
    def run(self, node_type=None):
        """
       Gather gems
       """
        self.run_game()
        self.random_macro()
        self.check_captcha()
        self.check_reconnect()
        self.check_log_back()
        self.leave_kd_buff()

        self.leave_city()
        self.better_sleep((1.5, 2))
        self.zoom_out_city()

        if node_type is None:
            self.node_type = "First"
        print(self.node_type)
        self.scan_node()

        max_distance = 6
        swipes = {self.swipe_up: self.swipe_right,
                  self.swipe_right: self.swipe_down,
                  self.swipe_down: self.swipe_left,
                  self.swipe_left: self.swipe_up}
        current_swipe = self.swipe_up

        for i in range(max_distance):
            for y in range(i):

                if self.data[str(self.sel)]['schedules'][self.current_profile][
                    self.node_type] == 'nothing' or self.node_type == 'Done' or (not self.free_troop_commander_list()):
                    return

                self.swipe_scan(self.scan_node, current_swipe)

            current_swipe = swipes[current_swipe]
        return self.run(node_type=self.next_resource_type(node_type))
