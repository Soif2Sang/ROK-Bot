from random import uniform

from tasks.Task import Task
from utils.functions import filter_coordinate, get_class


class AllianceHelp(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.herite(MainTask)

    def task_name(self):
        return "AllianceHelp"

    @get_class
    def run(self):
        for i in range(1, 4):
            if co := self.find_img(f"help{i}", confidence=0.93):
                if filter_coordinate(co):
                    self.click(co[0] + uniform(3, 7), co[1] + uniform(20, 22))
                    self.print("Successfully helped alliance members !", "green")
                    self.better_sleep((1, 1))
