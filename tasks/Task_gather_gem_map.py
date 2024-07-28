from datetime import datetime
from random import randint, uniform
from time import time

import numpy as np

from utils.schemas.emulator_schemas import CordsSchema
from tasks.Task import Task
from tasks.Task_gather_gem import GatherGem
from utils.functions import get_class, get_name
from utils.singletons import EmulatorSingleton

# from utils.easyOcr import Reader


class GatherGemMap(GatherGem):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask)
        self.herite(MainTask)
        self.context_task = self.context_profile.tasks.gather_gem

        self.max_distance = 3
        self.end_time = None
        self.block = False
        self.nodes_gathered = 0
        self.position = self.context_task.map_center_pos


    def task_name(self):
        return "GatherGem"

    def recenter(self, deadstop=0):
        return super().recenter(deadstop, "gather_gem.searching_radius")

    def go_back_to_city(self, deadstop=0):
        # if self.data[str(self.sel)]["schedules"][self.current_profile].get("recenter_feature", False):
        return super().go_back_to_city(deadstop)

    @get_name
    def go_city(self, x, y, last=None) -> int:
        raise NotImplementedError("This method should not be called")
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
                self.adb.shell(f"input text {self.context_profile.tasks.gather_gem}")
                self.better_sleep((0.3, 0.5))
                self.script_pause()
        self.better_sleep((0.3, 0.5))
        for i in range(2):
            self.click(uniform(590, 685), uniform(130, 150))
            self.better_sleep((0.3, 0.5))
            if i == 0:
                string = f"input text {x2}"
                self.script_pause()
                self.adb.shell(string)
                self.better_sleep((0.3, 0.5))
        self.better_sleep((0.3, 0.5))
        for i in range(2):
            self.click(uniform(750, 830), uniform(130, 150))
            self.better_sleep((0.3, 0.5))
            if i == 0:
                self.script_pause()
                string = f"input text {y2}"
                self.adb.shell(string)
                self.better_sleep((0.3, 0.5))
        self.better_sleep((0.3, 0.5))
        self.click(uniform(860, 900), uniform(123, 158))
        self.better_sleep((1, 2))

    @get_name
    def go_random_area(self):
        raison = self.max_distance

        x = uniform(-raison, raison) + self.position.x
        y = uniform(-raison, raison) + self.position.y - 10

        self.click(x, y)
        self.better_sleep((1, 2))

    @get_name
    def find_city_position(self):
        image = self.adb.get_screen()
        image = image[:146, 1072:]

        lower_green = np.array([0, 220, 0])  # Adjust these values as needed
        upper_green = np.array([40, 250, 40])  # Adjust these values as needed

        for x in range(image.shape[1]):
            for y in range(image.shape[0]):
                if np.all(image[y, x] >= lower_green) and np.all(image[y, x] <= upper_green):
                    self.position = self.context_task.map_center_pos = CordsSchema(x=1072 + x, y=3 + y)
                    self.print("Successfully found the city position")
                    return True

        self.print("Failed to find the city position", "red")
        return False

    @get_class
    def run(self, end_time=None):
        """
        Gather gems
        """
        self.end_time = end_time

        if EmulatorSingleton().getEmulatorType() == "bluestacks" and not self.random_macro():
            return

        self.run_game()
        self.check_captcha()
        self.check_reconnect()
        self.check_log_back()
        self.leave_kd_buff()

        self.leave_city()
        self.better_sleep((1.5, 2))
        self.zoom_out_city()

        if self.context_task.map_center_pos_method == "auto":
            if not self.find_city_position():
               return

        enable_gem_node_limit = self.context_task.node_limit.enabled
        gem_node_limit = self.context_task.node_limit.fixed_node_limit

        starting_time = time()

        if self.end_time is None:
            self.end_time = starting_time + (
                randint(
                    self.context_task.duration.min * 60,
                    self.context_task.duration.max * 60,
                )
            )

        self.print(f"Gathering gems till around : {datetime.fromtimestamp(self.end_time).strftime('%H:%M:%S')}")

        self.max_distance = self.context_task.searching_radius / 6
        self.go_back_to_city()

        while self.end_time > time() and (
            enable_gem_node_limit == False or (enable_gem_node_limit and self.nodes_gathered < gem_node_limit)
        ):
            self.swipe_scan(self.scan_gem, self.go_random_area)
