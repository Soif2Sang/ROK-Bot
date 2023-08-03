import re
import traceback
from datetime import datetime
from random import uniform, randint, random, choice
from time import sleep, time

from Task_gather_gem import GatherGem
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


    @get_class
    def run(self, end_time=None):
        """
       Gather gems
       """
        self.end_time = end_time
        self.random_macro()

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

        while self.end_time > time():
            self.scan_gem()
            max_distance = int(self.data[str(self.sel)]['schedules'][self.current_profile].get('radius') // 4)

            swipes = {
                self.swipe_up: self.swipe_right,
                self.swipe_right: self.swipe_down,
                self.swipe_down: self.swipe_left,
                self.swipe_left: self.swipe_up
            }

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
