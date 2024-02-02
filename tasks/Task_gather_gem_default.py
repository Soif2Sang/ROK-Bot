from datetime import datetime
from random import randint, uniform
from time import time

import cv2

from tasks.Task import Task
from tasks.Task_gather_gem import GatherGem
from utils.functions import get_class, get_name
from utils.singletons import EmulatorSingleton

# from utils.easyOcr import Reader


class GatherGemDefault(GatherGem):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask)
        self.herite(MainTask)
        self.end_time = None
        self.block = False
        self.nodes_gathered = 0

    def task_name(self):
        return "GatherGem"

    def recenter(self, deadstop=0):
        if self.data[str(self.sel)]["schedules"][self.current_profile].get("recenter_feature", False):
            return super().recenter(deadstop)

    @get_class
    def run(self, end_time=None):
        """
        Gather gems
        """
        self.end_time = end_time

        if EmulatorSingleton().getEmulator() == "bluestacks" and not self.random_macro():
            return

        self.run_game()
        self.check_captcha()
        self.leave_city()
        self.better_sleep((1.5, 2))
        self.zoom_out_city()
        self.better_sleep((1.5, 2))
        self.scan_gem()
        self.better_sleep((0.125, 0.195))
        randomization = self.go_to(
            self.data[str(self.sel)]["schedules"][self.current_profile].get("city_x", 500),
            self.data[str(self.sel)]["schedules"][self.current_profile].get("city_y", 500),
        )
        # print(f"{randomization = }")

        enable_gem_node_limit = self.data[self.sel]["schedules"][self.current_profile]["gather_gem_enable_node_limit"]
        gem_node_limit = self.data[self.sel]["schedules"][self.current_profile]["gather_gem_note_limit"]

        radius = self.data[str(self.sel)]["schedules"][self.current_profile].get("radius", 50) // 10
        width = radius + 1
        height = radius + 1
        starting_time = time()
        time_restart = time()

        if self.end_time is None:
            self.end_time = starting_time + (
                randint(
                    self.data[str(self.sel)]["schedules"][self.current_profile].get("gather_gem_duration1") * 60,
                    self.data[str(self.sel)]["schedules"][self.current_profile].get("gather_gem_duration2") * 60,
                )
            )

        self.print(f"Gathering gems till around : {datetime.fromtimestamp(self.end_time).strftime('%H:%M:%S')}")
        while self.end_time > time() and (
            enable_gem_node_limit == False or (enable_gem_node_limit and self.nodes_gathered < gem_node_limit)
        ):
            self.run_game()
            if self.data[str(self.sel)]["schedules"][self.current_profile].get("restart_game", True):
                random_time = uniform(4000, 5800)
                if time() > time_restart + random_time:
                    self.print("Time to restart the game during gathering gems !")
                    self.leave_game(force=True)
                    self.print(f"Game is stopped, game starting in about 7sec")
                    self.better_sleep((5, 10))
                    self.run_game()
                    self.print("Function is going to restart")
                    self.check_captcha()
                    self.leave_city()
                    # print("premier leave city")
                    self.better_sleep((1.5, 2))
                    self.zoom_out_city()
                    self.better_sleep((1.5, 2))
                    self.scan_gem()
                    self.better_sleep((0.125, 0.195))
                    randomization = self.go_to(
                        self.data[str(self.sel)]["schedules"][self.current_profile].get("city_x", 500),
                        self.data[str(self.sel)]["schedules"][self.current_profile].get("city_y", 500),
                    )
                    time_restart = time()

            pil_image = self.adb.get_curr_device_screen_img()
            cv_image = self.pil_to_array(pil_image)
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            cropped_image = cv_image[0:100, 0:800]
            if self.find_img(target="block_icon", source=cropped_image, confidence=0.90) is not None:
                self.print("Block icon detected. Cancelling the function !")
                return

            self.scan_gem()
            self.check_reconnect(cv_image)
            if self.check_if_interrupt():
                return self.run(self.end_time)
            self.check_captcha(False)
            self.leave_kd_buff()

            # print("test")
            if randomization == 0:
                for y in range(width - 1):
                    for i in range(width):
                        if self.end_time < time():
                            return
                        if self.block:
                            return
                        if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                            return
                        self.swipe_scan(self.scan_gem, self.swipe_right)

                    self.recenter()
                    self.check_captcha(False)
                    self.leave_kd_buff()
                    if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                        return
                    self.swipe_scan(self.scan_gem, self.swipe_down)

                    for i in range(width):
                        if self.end_time < time():
                            return
                        if self.block:
                            return
                        if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                            return
                        self.swipe_scan(self.scan_gem, self.swipe_left)

                    self.recenter()
                    self.check_captcha(False)
                    self.leave_kd_buff()

                    if y != (width - 2):
                        if self.end_time < time():
                            return
                        if self.block:
                            return
                        if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                            return
                        self.swipe_scan(self.scan_gem, self.swipe_down)
                        self.recenter()

            if randomization == 2:
                for y in range(width - 1):
                    for i in range(width):
                        if self.end_time < time():
                            return
                        if self.block:
                            return
                        if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                            return
                        self.swipe_scan(self.scan_gem, self.swipe_left)

                    self.recenter()
                    self.check_captcha(False)
                    self.leave_kd_buff()
                    if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                        return
                    self.swipe_scan(self.scan_gem, self.swipe_up)

                    for i in range(width):
                        if self.end_time < time():
                            return
                        if self.block:
                            return
                        if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                            return
                        self.swipe_scan(self.scan_gem, self.swipe_right)

                    self.recenter()
                    self.check_captcha(False)
                    self.leave_kd_buff()

                    if y != (width - 2):
                        if self.end_time < time():
                            return
                        if self.block:
                            return
                        if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                            return
                        self.swipe_scan(self.scan_gem, self.swipe_up)
                        self.recenter()

            if randomization == 1:
                for y in range(height - 1):
                    for i in range(height):
                        if self.end_time < time():
                            return
                        if self.block:
                            return
                        if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                            return
                        self.swipe_scan(self.scan_gem, self.swipe_down)

                    self.recenter()
                    self.check_captcha(False)
                    self.leave_kd_buff()
                    if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                        return
                    self.swipe_scan(self.scan_gem, self.swipe_left)

                    for i in range(height):
                        if self.end_time < time():
                            return
                        if self.block:
                            return
                        if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                            return
                        self.swipe_scan(self.scan_gem, self.swipe_up)

                    self.recenter()
                    self.check_captcha(False)
                    self.leave_kd_buff()

                    if y != (height - 2):
                        if self.end_time < time():
                            return
                        if self.block:
                            return
                        if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                            return
                        self.swipe_scan(self.scan_gem, self.swipe_left)
                        self.recenter()

            if randomization == 3:
                for y in range(height - 1):
                    for i in range(height):
                        if self.end_time < time():
                            return
                        if self.block:
                            return
                        if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                            return
                        self.swipe_scan(self.scan_gem, self.swipe_up)

                    self.recenter()
                    self.check_captcha(False)
                    self.leave_kd_buff()
                    if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                        return
                    self.swipe_scan(self.scan_gem, self.swipe_right)

                    for i in range(height):
                        if self.end_time < time():
                            return
                        if self.block:
                            return
                        if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                            return
                        self.swipe_scan(self.scan_gem, self.swipe_down)

                    self.recenter()
                    self.check_captcha(False)
                    self.leave_kd_buff()

                    if y != (height - 2):
                        if self.end_time < time():
                            return
                        if self.block:
                            return
                        if enable_gem_node_limit and self.nodes_gathered >= gem_node_limit:
                            return
                        self.swipe_scan(self.scan_gem, self.swipe_right)
                        self.recenter()

            self.better_sleep((1.525, 2.795))
            # self.leave_city()
            # print("second leave cit")
            randomization = self.go_to(
                self.data[str(self.sel)]["schedules"][self.current_profile].get("city_x", 500),
                self.data[str(self.sel)]["schedules"][self.current_profile].get("city_y", 500),
                randomization,
            )
            self.print(f"Current path n°{randomization}")
            self.zoom_out_city()
        self.print("Gathering gem time elapsed !")
