import json

from random import uniform, shuffle

from pytesseract import pytesseract

from Task import Task
from Task_utils import get_class, filter_coordinate

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class BuyMerchant(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.frame)
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.current_profile = MainTask.current_profile
        self.frame = MainTask.frame
        self.adb = MainTask.adb
        self.ppid = MainTask.ppid
        self.pid = MainTask.pid
        self.language = MainTask.language
        self.name = MainTask.name
        self.resource_type = MainTask.resource_type
        self.sel = MainTask.sel

    def task_name(self):
        return "BuyMerchant"

    @get_class
    def run(self):
        co = self.adb.find_img(target="merchant_icon", confidence=0.7)
        if co is None:
            return
        if not filter_coordinate(co):
            return
        x, y = co[0] + uniform(0, 10), co[1] + uniform(0, 10)
        self.print(f'Merchant icon : {x=} {y=}')
        self.click(x, y)
        for y in range(2):
            for i in range(4):
                self.better_sleep((1.8, 2.2))
                food = self.adb.find_multiple_img("merchant_buy_with_food", 0.8)
                wood = self.adb.find_multiple_img("merchant_buy_with_wood", 0.8)
                # for element in wood:
                #     food.append(element)
                food.extend(wood)
                shuffle(food)
                for element in food:
                    self.click(element[0] + uniform(0, 30), element[1] + uniform(-2, 8))
                    self.better_sleep((0.45, 0.7))
                x1, y1 = uniform(586, 870), uniform(457, 487)
                x2, y2 = x1 + uniform(-10, 10), y1 - uniform(120, 150)
                if i!=3:
                    self.swipe(x1, y1, x2, y2)
            if y != 0:
                break
            co = self.adb.find_img(target="free")
            if co is None:
                break
            x, y = co[0] + uniform(0, 50), co[1] + uniform(0, 20)
            self.click(x, y)
        x, y = uniform(1077, 1100), uniform(64, 95)
        self.click(x, y)