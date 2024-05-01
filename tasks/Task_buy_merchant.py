from random import shuffle, uniform

from tasks.Task import Task
from utils.functions import filter_coordinate, get_class, get_name


class BuyMerchant(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.herite(MainTask)
        self.context_task = self.context_profile.tasks.buy_mysterious_merchant

    def task_name(self):
        return "BuyMerchant"

    @get_name
    def manage_artefact_shop(self):
        co = self.find_img(target="artefact_shop", confidence=0.7)
        if co is not None:
            self.click(co[0] + uniform(10, 35), co[1] + uniform(0, 30))
            self.better_sleep((1, 2))
            if co := self.find_img("close_window"):
                self.click(uniform(1100, 1120), uniform(73, 80))
                self.better_sleep((1, 2))

    @get_name
    def buy_from_shop_light(self):
        total = 0
        for y in range(2):
            for i in range(2):
                self.better_sleep((1.8, 2.2))
                food = self.adb.find_multiple_img(target="merchant_buy_with_food", confidence=0.8)
                wood = self.adb.find_multiple_img(target="merchant_buy_with_wood", confidence=0.8)
                food.extend(wood)

                food = list(filter(lambda co: co[1] < 470, food))
                shuffle(food)
                for element in food:
                    self.click(element[0] + uniform(0, 30), element[1] + uniform(-2, 8))
                    self.better_sleep((0.45, 0.7))
                    total += 1
                x1, y1 = uniform(586, 870), uniform(457, 487)
                x2, y2 = x1 + uniform(-10, 10), y1 - uniform(120, 150)
                if i != 1:
                    self.swipe(x1, 600, x2, 300)
            if y != 0:
                break
            co = self.find_img(target="free")
            if co is None:
                break
            self.print("Refreshing the merchant")
            x, y = co[0] + uniform(0, 50), co[1] + uniform(0, 20)
            self.click(x, y)
        if total:
            self.print(f"Bought {total} items.")

    @get_name
    def buy_from_shop(self):
        total = 0
        for y in range(2):
            for i in range(4):
                self.better_sleep((1.8, 2.2))
                screen = self.adb.get_cv2_img()
                food = self.adb.find_multiple_img(target="merchant_buy_with_food", confidence=0.8, source=screen)
                wood = self.adb.find_multiple_img(target="merchant_buy_with_wood", confidence=0.8, source=screen)
                food.extend(wood)
                shuffle(food)
                for element in food:
                    self.click(element[0] + uniform(0, 30), element[1] + uniform(-2, 8))
                    self.better_sleep((0.45, 0.7))
                    total += 1
                x1, y1 = uniform(586, 870), uniform(457, 487)
                x2, y2 = x1 + uniform(-10, 10), y1 - uniform(120, 150)
                if i != 3:
                    self.swipe(x1, y1, x2, y2)
            if y != 0:
                break
            co = self.find_img(target="free")
            if co is None:
                break
            self.print("Refreshing the merchant")
            x, y = co[0] + uniform(0, 50), co[1] + uniform(0, 20)
            self.click(x, y)
        if total:
            self.print(f"Bought {total} items.")

    @get_class
    def run(self):
        self.manage_artefact_shop()
        co = self.find_img(target="merchant_icon", confidence=0.7)
        if co is None:
            return self.print("Merchant is not here.")
        if not filter_coordinate(co):
            return self.print("Merchant seems inaccessible.")
        self.print("Robbing the shop.", "green")
        self.click(co[0] + uniform(0, 10), co[1] + uniform(0, 10))
        if self.context_task.skip_second_row:
            self.buy_from_shop_light()
        else:
            self.buy_from_shop()
        self.click(uniform(1077, 1100), uniform(64, 95))
        self.better_sleep((1, 1.5))
        if self.find_img(target=f"get_more_rss") is not None:
            self.click(uniform(1000, 1020), uniform(129, 148))
            self.better_sleep((1, 1.425))
        self.close_windows()
