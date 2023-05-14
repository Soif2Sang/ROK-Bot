
from random import uniform, shuffle, choice
from pytesseract import pytesseract

from taskscod.COD_Task import Task
from utils.Task_utils import filter_coordinate, get_class, get_data

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class CollectResource(Task):
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
        return "CollectResource"

    def collect_gold(self):
        co = self.adb.find_multiple_img(target="gold_max", confidence=0.8)
        co2 = self.adb.find_multiple_img(target="gold_min", confidence=0.8)
        co.extend(co2)
        co = list(filter(filter_coordinate, co))
        return choice(co) if co != [] else None

    def collect_food(self):
        co = self.adb.find_multiple_img(target="food_max", confidence=0.8)
        co2 = self.adb.find_multiple_img(target="food_min", confidence=0.8)
        co.extend(co2)
        co = list(filter(filter_coordinate, co))
        return choice(co) if co != [] else None

    def collect_wood(self):
        co = self.adb.find_multiple_img(target="wood_max", confidence=0.8)
        co2 = self.adb.find_multiple_img(target="wood_min", confidence=0.8)
        co.extend(co2)
        co = list(filter(filter_coordinate, co))
        return choice(co) if co != [] else None

    def collect_stone(self):
        co = self.adb.find_multiple_img(target="stone_max", confidence=0.8)
        co2 = self.adb.find_multiple_img(target="stone_min", confidence=0.8)
        co.extend(co2)
        co = list(filter(filter_coordinate, co))
        return choice(co) if co != [] else None

    @get_class
    def run(self):
        tasks = [self.collect_food, self.collect_wood, self.collect_stone, self.collect_gold]
        shuffle(tasks)
        tab = []
        for task in tasks:
            result = task()
            if result is not None:
                self.print(f"{task.__name__} found")
                tab.append(result)
            else:
                self.print(f"{task.__name__} not found")
        for cords in tab:
            self.click(cords[0] + uniform(10, 20), cords[1] + uniform(20, 30))
            self.better_sleep((0.695, 1))