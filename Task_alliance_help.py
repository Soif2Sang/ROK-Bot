import json
from random import uniform

from Task import Task
from Task_utils import get_class, get_name, filter_coordinate


class AllianceHelp(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.current_profile = MainTask.current_profile
        self.frame = MainTask.tile
        self.adb = MainTask.adb
        self.ppid = MainTask.ppid
        self.pid = MainTask.pid
        self.language = MainTask.language
        self.name = MainTask.name
        self.sel = MainTask.sel

    def task_name(self):
        return "AllianceHelp"

    @get_class
    def run(self):
        for i in range(1,4):
            if(co:=self.adb.find_img(f"help{i}")):
                if co is not None:
                    cond = filter_coordinate(co)
                    if cond:
                        self.click(co[0] + uniform(5, 10), co[1] + uniform(5, 10))
                        self.better_sleep((1,2))