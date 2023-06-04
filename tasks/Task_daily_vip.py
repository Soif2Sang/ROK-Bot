from random import uniform

from PIL import Image

from tasks.Task import Task
from utils.Task_utils import get_class


class DailyVip(Task):
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
        return "DailyVip"

    @get_class
    def run(self):
        cv_image = self.adb.get_cv2_img()
        img = Image.fromarray(cv_image)
        if img.getpixel((186, 50)) == (0, 0, 227):
            self.click(uniform(105, 170), uniform(56, 69))
            self.better_sleep((1.25, 2))
            cv_image = self.adb.get_cv2_img()
            img = Image.fromarray(cv_image)
            if img.getpixel((1041, 155)) == (0, 0, 227):
                self.print("Claiming daily VIP points")
                self.click(uniform(1000, 1044), uniform(163, 192))
                self.better_sleep((2, 2.5))
                if (co := self.find_img(target="close_window")):
                    self.click(co[0] + uniform(5, 10), co[1] + uniform(5, 10))
                    self.better_sleep((1, 1.5))
            co = self.find_img(target="claim_daily")
            if co is not None:
                self.print("Claiming daily VIP chest reward")
                self.click(uniform(co[0] - 5, co[0] + 80), uniform(co[1], co[1] + 25))
                self.better_sleep((4.5, 6))
                self.click(uniform(300, 1000), uniform(33, 87))
                self.better_sleep((1.25, 2))
            self.close_windows()
