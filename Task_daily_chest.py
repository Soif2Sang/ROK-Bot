import json
import traceback


from random import uniform
import cv2
from pytesseract import pytesseract

from Task import Task, get_name
from Task_utils import get_class,get_data

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class DailyChest(Task):
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
        return "DailyChest"

    @get_name
    def close_chest_popup(self):
        for i in range(2):
            co = self.find_img(target=f"popup{i}",confidence=0.8)
            if co is not None:
                self.click(uniform(1102, 1030), uniform(92, 118))
                self.better_sleep((2, 4))
    @get_name
    def claim_legendary_chest(self):
        try:
            co = self.find_img(target='legendary_chest')

            if co is not None:
                self.click(co[0] + uniform(10, 20), co[1] + uniform(10, 20))
                self.better_sleep((1.7, 3))
                if (chest := self.find_img(target="open_chest")) is not None:
                    self.click(chest[0] + uniform(20, 100), chest[1] + uniform(10, 40))
                    self.better_sleep((3, 5))
                    while confirm := self.find_img(target="confirm_tavern"):
                        self.click(confirm[0] + uniform(20, 100), confirm[1] + uniform(10, 40))
                        self.better_sleep((1.7, 3))
                self.click(uniform(25, 55), uniform(20, 56))
                self.better_sleep((2.5, 5))
                self.close_chest_popup()
        except Exception as e:
            traceback.print_exc()

    @get_class
    def run(self):
        self.claim_legendary_chest()
        self.better_sleep((1.7, 3))
        cv_image = self.adb.get_cv2_img()
        chests = ['material_chest', 'golden_chest', 'silver_chest']
        entered = False
        for chest in chests:
            if entered:
                break
            if co := self.find_img(source=cv_image, target=chest, confidence=0.85):
                entered = True
                self.click(co[0] + uniform(0, 35), co[1] + uniform(0, 35))
                self.better_sleep((1.7, 3))
                open_chests = self.adb.find_multiple_img("open_chest")
                for open in open_chests:
                    self.print("Opening a chest..")
                    self.click(open[0] + uniform(0, 100), open[1] + uniform(10, 40))
                    self.better_sleep((5, 8))
                    while confirm := self.find_img(target="confirm_tavern"):
                        self.click(confirm[0] + uniform(20, 100), confirm[1] + uniform(10, 40))
                        self.better_sleep((1.7, 3))
                self.better_sleep((1.7, 3))

        if entered:
            self.click(uniform(25, 55), uniform(20, 56))
            self.better_sleep((1.7, 3))
            self.close_chest_popup()