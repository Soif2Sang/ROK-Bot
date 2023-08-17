import re
import traceback
from datetime import datetime
from random import uniform, randint, random, choice
from time import sleep, time

from tasks.Task_gather_gem import GatherGem
from tasks.Task import Task
from utils.Task_utils import get_name, get_class


# from utils.easyOcr import Reader


class GatherGemSpiral(GatherGem):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask)
        self.herite(MainTask)
        self.end_time = None
        self.block = False

    def task_name(self):
        return "GatherGem"

    def recenter(self, deadstop = 0):
        if self.data[str(self.sel)]['schedules'][self.current_profile].get('recenter_feature', False):
            return super().recenter(deadstop)

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


    @get_class
    def run(self, end_time=None):
        """
       Gather gems
       """
        self.end_time = end_time
        if not self.random_macro():
            return

        self.run_game()
        self.check_captcha()
        self.check_reconnect()
        self.check_log_back()
        self.leave_kd_buff()

        self.leave_city()
        self.better_sleep((1.5, 2))
        self.zoom_out_city()

        starting_time = time()
        if self.data[str(self.sel)]['schedules'][self.current_profile].get('gather_gem_duration1') > \
                self.data[str(self.sel)]['schedules'][
                    self.current_profile].get('gather_gem_duration2'):
            self.data[self.sel]['schedules'][self.current_profile]['gather_gem_duration1'], \
                self.data[self.sel]['schedules'][self.current_profile]['gather_gem_duration2'] = \
                self.data[self.sel]['schedules'][self.current_profile]['gather_gem_duration2'], \
                    self.data[self.sel]['schedules'][self.current_profile]['gather_gem_duration1']

        if self.end_time is None:
            self.end_time = starting_time + (
                    randint(
                        self.data[str(self.sel)]['schedules'][self.current_profile].get('gather_gem_duration1'),
                        self.data[str(self.sel)]['schedules'][self.current_profile].get('gather_gem_duration2')
                    ) * 60
            )

        self.print(f"Gathering gems till around : {datetime.fromtimestamp(self.end_time).strftime('%H:%M:%S')}")
        self.go_city(self.data[str(self.sel)]['schedules'][self.current_profile].get('city_x', 500),
                     self.data[str(self.sel)]['schedules'][self.current_profile].get('city_y', 500))

        max_distance = int(self.data[str(self.sel)]['schedules'][self.current_profile].get('radius') // 4)

        swipes = {
            self.swipe_up: self.swipe_right,
            self.swipe_right: self.swipe_down,
            self.swipe_down: self.swipe_left,
            self.swipe_left: self.swipe_up
        }

        while self.end_time > time():
            self.scan_gem()

            random_function = choice(list(swipes.keys()))
            current_swipe = swipes[random_function]

            has_to_hit = 2
            loop = 1
            current = 0

            for i in range(max_distance):
                self.recenter()
                if has_to_hit == current:
                    loop += 1
                    current = 0
                for y in range(loop):
                    if self.end_time < time(): return
                    if self.block: return
                    self.swipe_scan(self.scan_gem, current_swipe)

                current += 1
                current_swipe = swipes[current_swipe]

            self.go_city(self.data[str(self.sel)]['schedules'][self.current_profile].get('city_x', 500),
                         self.data[str(self.sel)]['schedules'][self.current_profile].get('city_y', 500))
