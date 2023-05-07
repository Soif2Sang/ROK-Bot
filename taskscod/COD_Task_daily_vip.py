from PIL import Image
from random import uniform

from pytesseract import pytesseract

from taskscod.COD_Task import Task
from utils.Task_utils import get_class, get_data

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class DailyVip(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.data = get_data()
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
        if not (co:=self.find_img("cod_faily_vip")):
            return

        self.click(co[0] + uniform(0,6),co[1] + uniform(0,6))
        self.better_sleep((1.2,2.2))
        if (co:=self.find_img("cod_claim_daily_vip")):
            self.click(co[0] + uniform(0,6),co[1] + uniform(0,6))
            self.better_sleep((1.2,2.2))
            self.click(co[0] + uniform(0, 6), co[1] + uniform(0, 6))
            self.better_sleep((1.2, 2.2))
        self.click(371,473)
        self.better_sleep((1.2, 2.2))
        if (co:=self.find_img("cod_claim_daily_vip")):
            self.click(co[0] + uniform(0,6),co[1] + uniform(0,6))
            self.better_sleep((1.2,2.2))
            self.click(co[0] + uniform(0, 6), co[1] + uniform(0, 6))
            self.better_sleep((1.2, 2.2))
        self.close_windows()