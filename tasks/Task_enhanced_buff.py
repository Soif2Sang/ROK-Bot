from random import uniform, shuffle

import cv2

from tasks.Task import Task
from utils.Task_utils import get_class, get_name


class UseEnhancedBuff(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.herite(MainTask)

    def task_name(self):
        return "UseEnhancedBuff"

    @get_name
    def get_remaining_buffs(self):
        buffs_to_do = []
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = self.pil_to_array(pil_image)
        image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        image = image[0:110, 0:680]
        here = False
        for buffs_string in ['purple', 'blue']:
            co = self.find_img(source=image, target=f'buffs\\enhanced_gathering_{buffs_string}', confidence=0.8)
            if co is not None:
                here = True
                break
        if not here:
            buffs_to_do.append("speed")
        for rss_type in ['food', 'wood', 'stone', 'gold']:
            here = False
            for buff_type in ['blue', 'green']:
                co = self.find_img(source=image, target=f'buffs\\enhanced_{rss_type}_{buff_type}', confidence=0.8)
                if co is not None:
                    here = True
                    break
            if not here:
                buffs_to_do.append(rss_type)
        return buffs_to_do

    @get_class
    def run(self):
        buffs_to_do = []
        buffs_to_do.extend(self.get_remaining_buffs())

        self.print(f"Buffs : {buffs_to_do}")
        if buffs_to_do:
            if self.find_img(target='menu_opened') is None:
                x, y = uniform(1200, 1250), uniform(650, 690)
                # else:
                #     # x, y = temp3[0] + uniform(0, 20), temp3[1] + uniform(0, 15)
                self.click(x, y)
                self.better_sleep((0.725, 1.295))
            x, y = uniform(910, 950), uniform(650, 690)
            self.click(x, y)
            self.better_sleep((1.895, 2.3))
            x, y = uniform(490, 600), uniform(65, 100)
            self.click(x, y)
            self.better_sleep((1.195, 2))
            shuffle(buffs_to_do)
            if "speed" in buffs_to_do:
                buffs_to_do.remove("speed")
                buffs_to_do.insert(0, "speed")
            scrolled = False
            for element in buffs_to_do:
                # print(element)
                self.print(f"Trying to enable {element} boost")
                co = self.find_img(target="no")
                if co is not None:
                    self.print(f"{element} is already enabled", "red")
                    self.click(co[0] + uniform(0, 30), co[1] + uniform(1, 15))
                    self.better_sleep((1.9, 3))
                if element == "speed":
                    co = self.find_img(target='items\\enhanced_gathering_purple')
                    if co is None:
                        co = self.find_img(target='items\\enhanced_gathering_blue')
                    if co is not None:
                        x, y = co[0] + uniform(10, 60), co[1] + uniform(10, 60)
                        self.click(x, y)
                        self.better_sleep((1.195, 2))
                        x, y = uniform(910, 1050), uniform(575, 622)
                        self.click(x, y)
                        self.better_sleep((1.195, 2))
                if not scrolled:
                    scrolled = True
                    x1, y1 = uniform(586, 800), uniform(457, 487)
                    x2, y2 = x1 + uniform(-10, 10), y1 - uniform(300, 350)
                    self.swipe(x1, y1, x2, y2)
                    self.better_sleep((1.195, 2))
                if element != "speed":
                    co = self.find_img(target=f'items\\enhanced_{element}_blue')
                    if co is None:
                        co = self.find_img(target=f'items\\enhanced_{element}_green')
                    if co is not None:
                        x, y = co[0] + uniform(10, 60), co[1] + uniform(10, 60)
                        self.click(x, y)
                        self.better_sleep((1.195, 2))
                        x, y = uniform(910, 1050), uniform(575, 622)
                        self.click(x, y)
                        self.better_sleep((1.195, 2))

            co = self.find_img(target="no")
            if co is not None:
                self.click(co[0] + uniform(0, 30), co[1] + uniform(1, 15))
                self.better_sleep((1.9, 3))
            self.better_sleep((1, 2))
            co = self.find_img(target="cross")
            if co is not None:
                # print("Cross found")
                self.click(co[0] + uniform(0, 50), co[1] + uniform(0, 50))
                self.better_sleep((1, 2))
