import traceback
from random import uniform, random
from time import sleep

from PIL import Image

from tasks.Task_gather_rss import GatherRss
from tasks.Task import Task
from utils.Task_utils import get_name, get_class


# from utils.easyOcr import Reader

class GatherRssZoom(GatherRss):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask)
        self.herite(MainTask)
        self.end_time = None
        self.block = False

    def task_name(self):
        return "GatherRss"




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
    def scan_node(self, param=None):
        """
        Scan device screenshot to find gem node,          not 100% working need improvement
        :return: None
        """
        self.restart_if_game_crashed()
        screen = self.adb.get_cv2_img()
        list_nodes = [f"{self.data[str(self.sel)]['schedules'][self.current_profile][self.node_type]}_icon_zoom"]
        for element  in ['down','up']:
            for element2 in ['left','right']:
                list_nodes.append(f"{self.data[str(self.sel)]['schedules'][self.current_profile][self.node_type]}_{element}_{element2}_icon_zoom")
        co = None
        for icon in list_nodes:
            co = self.validate_co(
                self.find_img(source=screen, target=icon, confidence=0.8))
            if co is not None:
                self.print(f"Node Found - x: {co[0]} y:{co[1]}")
                if self.already_mining(co[0], co[1], screen):
                    self.print(f"Already mining this node")
                    co = None
            if co:
                break
        if not co:
            return

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

        if self.find_cross():
            return self.adjusted_leave_city(x_click, y_click)

        if not self.click_on_node():
            return self.adjusted_leave_city(x_click, y_click)

        if self.send_troop():
            self.node_type = self.next_resource_type(self.node_type)
            self.better_sleep((1.3, 2))
            self.check_captcha()
            self.zoom_out_city()
        else:
            return "STOP"


    @get_name
    def check_if_interrupt(self, screen = None):
        if not self.adb.is_game_alive():
            return True
        self.check_download_page(screen)
        self.leave_kd_buff(screen)
        self.check_reconnect(screen)
        if self.check_log_back(screen):
            return True
        return False


    @get_name
    def swipe_scan(self, scan, direction):

        self.script_pause()
        # print(f'[ {current_time()} ] [ {self.name} ] {direction = } {scan = }')
        direction()
        screen = self.adb.get_cv2_img()

        info_screen = screen[470:700, 0:115]
        cropped_image = screen[420:540, 480:810]

        if random() > 0.9:
            self.close_windows()

        if random() > 0.7:
            if self.check_if_interrupt(screen):
                return self.run(self.end_time)
            co = self.find_img(source=screen, target="verification_button", confidence=0.6)
            if co is not None:
                self.check_captcha()

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

    @get_class
    def run(self, node_type=None):
        if node_type == "Done":
            return self.click(700,400)
        self.node_type = node_type
        self.run_game()
        if not self.random_macro():
            return
        self.check_captcha()
        self.check_reconnect()
        self.check_log_back()
        self.leave_kd_buff()

        if node_type is None:
            self.leave_city()
        else:
            self.go_back_to_city()
        self.better_sleep((1.5, 2))
        self.zoom_out_city()

        if self.node_type is None:
            self.node_type = "First"
        print(self.node_type)
        self.scan_node()

        max_distance = 5
        swipes = {self.swipe_up: self.swipe_right,
                  self.swipe_right: self.swipe_down,
                  self.swipe_down: self.swipe_left,
                  self.swipe_left: self.swipe_up}
        current_swipe = self.swipe_up

        has_to_hit = 2
        loop = 1
        current = 0

        for i in range(max_distance):

            if has_to_hit == current:
                loop += 1
                current = 0

            for y in range(i):

                if self.data[str(self.sel)]['schedules'][self.current_profile].get(
                    self.node_type, 'nothing') == 'nothing' or self.node_type == 'Done' or (not self.free_troop_commander_list()):
                    return self.click(600, 400)

                if self.swipe_scan(self.scan_node, current_swipe) == "STOP":
                    return self.click(600, 400)

            current += 1
            current_swipe = swipes[current_swipe]
        return self.run(node_type=self.next_resource_type(self.node_type))
