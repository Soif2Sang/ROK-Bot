from random import uniform

from PIL import Image
from pytesseract import pytesseract

from taskscod.COD_Task import Task
from utils.functions import get_class

pytesseract.tesseract_cmd = r".\\tesseract\\tesseract.exe"


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

    @get_class
    def run(self):
        if not self.data[self.sel]["schedules"][self.current_profile][
            "research_center"
        ]:
            return
        co = self.data[self.sel]["schedules"][self.current_profile]["research_center"]
        self.click(co[0], co[1])
        self.better_sleep((1.2, 1.7))
        self.click(co[0], co[1])
        self.better_sleep((1.2, 1.7))
        if not (co := self.find_img("cod_research")):
            return self.close_windows()
        self.click(co[0] + uniform(5, 10), co[1] + uniform(5, 10))
        self.better_sleep((2, 2.7))
        if not (co := self.find_img("cod_research_button", confidence=0.8)):
            return self.close_windows()
        self.click(co[0] + uniform(5, 10), co[1] + uniform(5, 10))
        self.better_sleep((1.2, 1.7))
        if not (co := self.find_img("cod_research_top")):
            return self.close_windows()
        self.click(co[0] + uniform(5, 10), co[1] + uniform(5, 10))
        self.better_sleep((1.2, 1.7))
        if co := self.find_img("cod_research_button", confidence=0.8):
            self.click(co[0] + uniform(5, 10), co[1] + uniform(5, 10))
        self.close_windows()
