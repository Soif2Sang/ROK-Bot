from random import uniform

from tasks.Task import Task, get_name
from utils.Task_utils import get_class


class AcademyResearch(Task):
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

    def task_name(self):
        return "AcademyResearch"

    @get_name
    def academy_coordinates(self):
        return uniform(760,780), uniform(270,280)

    @get_name
    def enter_academy(self):
        for _ in range(2):
            x,y=self.academy_coordinates()
            self.click(x,y)
            self.better_sleep((0.9, 1.5))
        if self.adb.find_img("building_speedups") is None:
            if co:=self.adb.find_img("academy"):
                self.click(co[0] + uniform(0,20), co[1] + uniform(0,20))
                self.better_sleep((0.9, 1.5))
                return True
            else:
                return False
        else:
            self.print("Academy already researching")
            return False

    @get_name
    def help_build(self):
        if co := self.adb.find_img(target='help_build'):
            self.click(co[0] + uniform(0, 10), co[1] + uniform(20, 40))
            self.better_sleep((0.9, 1.2))
        if co := self.adb.find_img(target='help_build2'):
            self.click(co[0] + uniform(0, 10), co[1] + uniform(20, 40))
            self.better_sleep((0.9, 1.2))



    @get_name
    def select_tech(self):
        i = 0
        if (co:=self.adb.find_img("academy_tech")) is not None:
            self.click(co[0] + uniform(-5,5), co[1] + uniform(-5,5))
            self.better_sleep((0.9, 1.2))
            self.research_tech()
            self.better_sleep((0.9, 1.2))

    @get_name
    def research_tech(self):
        self.click(uniform(950, 1040), uniform(510, 555))
        self.better_sleep((0.9, 1.2))

    @get_class
    def run(self):
        if self.enter_academy():
            self.better_sleep((0.9, 1.2))
            if self.adb.find_img("tech_speedup") is None:
                self.select_tech()
                co = self.adb.find_img("cross")
                self.click(co[0] + uniform(0, 5), co[1] + uniform(0, 5))
        self.better_sleep((5,9))
        self.help_build()