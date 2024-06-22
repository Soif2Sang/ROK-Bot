from random import uniform

from tasks.Task import Task, get_name
from utils.functions import get_class

roles = {
    "justice": [300, 400],
    "duke": [530, 400],
    "architect": [750, 400],
    "scientist": [980, 400],
}


class Title(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.sel)
        self.herite(MainTask)

    def task_name(self):
        return "TitleBot"

    @get_name
    def go_to(self, kd, x, y, last=None) -> int:
        """
        Define starting path
        :param: x -> int x map location
        :param: y -> int y map location
        :return: starting location between 0,1,2,3
        """

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
                string = f"input text {kd}"
                self.adb.shell(string)
                self.better_sleep((0.3, 0.5))
                self.script_pause()
        self.better_sleep((0.3, 0.5))
        for i in range(2):
            self.click(uniform(590, 685), uniform(130, 150))
            self.better_sleep((0.3, 0.5))
            if i == 0:
                string = f"input text {x}"
                self.script_pause()
                self.adb.shell(string)
                self.better_sleep((0.3, 0.5))
        self.better_sleep((0.3, 0.5))
        for i in range(2):
            self.click(uniform(750, 830), uniform(130, 150))
            self.better_sleep((0.3, 0.5))
            if i == 0:
                self.script_pause()
                string = f"input text {y}"
                self.adb.shell(string)
                self.better_sleep((0.3, 0.5))
        self.better_sleep((0.3, 0.5))

        self.click(uniform(870, 900), uniform(130, 150))

        self.better_sleep((1, 2))

    @get_class
    def run(self, type: str, kingdom: str, x: int, y: int):
        self.leave_city_simple()
        self.go_to(kingdom, x, y)
        self.better_sleep((1.5, 3))
        for i in range(8):
            self.click(640 + uniform(-20, 20), 360 + uniform(-20, 20))
            self.better_sleep((1.5, 3))
            co = self.find_img("title_button")
            if co:
                break
        if not co:
            return False
        self.click(co[0], co[1])
        self.better_sleep((1.5, 3))

        self.click(roles[type][0], roles[type][1])
        self.better_sleep((1.5, 3))
        self.click(630, 640)
        self.better_sleep((1.5, 3))
        self.close_windows()
        return True
