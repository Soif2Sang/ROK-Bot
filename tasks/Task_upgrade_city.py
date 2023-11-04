import random
from random import uniform
from time import sleep

import win32api
import win32con
import win32gui

from tasks.Task_alliance_help import AllianceHelp
from tasks.Task import Task
from utils.Task_utils import get_class, get_name


class UpgradeCity(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.herite(MainTask)

    def task_name(self):
        return "UpgradeCity"

    @get_name
    def ch_coordinates(self):
        return uniform(630, 650), uniform(160, 180)

    @get_name
    def archery_coordinates(self):
        return uniform(650, 670), uniform(290, 300)

    @get_name
    def barracks_coordinates(self):
        return uniform(580, 590), uniform(230, 250)

    @get_name
    def siege_coordinates(self):
        return uniform(510, 520), uniform(190, 200)

    @get_name
    def stable_coordinates(self):
        return uniform(500, 520), uniform(280, 295)

    @get_name
    def tavern_coordinates(self):
        return uniform(620, 630), uniform(350, 370)

    @get_name
    def academy_coordinates(self):
        return uniform(720, 740), uniform(330, 350)

    @get_name
    def alliance_center_coordinates(self):
        return uniform(790, 810), uniform(380, 390)

    @get_name
    def scout_coordinates(self):
        return uniform(360, 380), uniform(375, 390)

    @get_name
    def hospital_coordinates(self):
        return uniform(560, 575), uniform(390, 410)

    @get_name
    def pass_coordinates(self):
        return uniform(900, 920), uniform(510, 540)

    @get_name
    def help_build(self):
        if co := self.find_img(target='help_build', confidence=0.75):
            self.click(co[0] + uniform(0, 10), co[1] + uniform(20, 40))
            self.better_sleep((0.9, 1.2))
        if co := self.find_img(target='help_build2', confidence=0.75):
            self.click(co[0] + uniform(0, 10), co[1] + uniform(20, 40))
            self.better_sleep((0.9, 1.2))
        if co := self.find_img(target='help_build3', confidence=0.75):
            self.click(co[0] + uniform(0, 10), co[1] + uniform(20, 40))
            self.better_sleep((0.9, 1.2))

    @get_name
    def recursive_upgrade(self, type="normal"):
        stones = self.find_img(target="upgrade_build", confidence=0.7)

        if stones is not None and self.find_img('building_speedups') is None:
            self.click(stones[0] + uniform(0, 20), stones[1] + uniform(0, 30))
            self.better_sleep((0.9, 1.2))
            if cos := self.adb.find_multiple_img(target="upgrade_go"):
                co = random.choice(cos)
                self.click(co[0] + uniform(0, 50), co[1] + uniform(0, 20))
                self.better_sleep((0.9, 1.2))
                return self.recursive_upgrade()
            else:
                self.click(uniform(916, 1050), uniform(530, 560))
                self.better_sleep((1.7, 2.2))
                # if (co := self.find_img(target="hire_constructor")) is not None or (
                # co := self.find_img(target="hire_constructor2")):
                #     self.click(co[0] + uniform(0, 110), co[1] + uniform(0, 40))
                #     self.better_sleep((1.7, 2.2))
                #     self.click(uniform(916, 1050), uniform(530, 560))
                #     self.better_sleep((1.7, 2.2))
                self.close_windows()
            # self.better_sleep((1.7, 2.2))
            self.help_build()
            self.better_sleep((1.7, 2.2))


    @get_name
    def setup_view(self):
        hwnd = win32gui.FindWindow(None, self.adb.name)
        hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)
        for _ in range(2):
            win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
            win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, win32con.VK_F6, 0)
            sleep(0.17)
            win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
            win32api.PostMessage(hwndChild, win32con.WM_KEYUP, win32con.VK_F6, 0)
            self.better_sleep((1.4, 2))

    @get_name
    def is_city_hall_upgradable(self):
        co = self.find_img(target="upgrade_build", confidence=0.7
                           )
        if co is not None:
            return True
        return False

    @get_name
    def help_alliance(self):
        if co := self.find_img(target="help_alliance_high_view", confidence=0.76):
            self.click(co[0] + uniform(10, 20), co[1] + 20)
            self.print("Successfully asked alliance help.")
            self.better_sleep((0.9, 1.2))
        AllianceHelp(self).run()


    @get_name
    def free_constructor(self):
        if self.find_img("upgrade_stone") is None and self.find_img("upgrade_stone2") is None:
            return False
        return True

    @get_class
    def run1(self):
        ch_position = self.data[str(self.sel)]['schedules'][self.current_profile].get('city_hall_position', [])
        if not ch_position:
            return
        x, y = ch_position
        self.click(x, y)
        self.better_sleep((1.7, 2.5))

        if self.is_city_hall_upgradable():
            self.recursive_upgrade()
        else:
            self.print("Already upgrading..")
        self.better_sleep((0.9, 1.2))

    @get_name
    def free_worker(self):
        upgrades_brut = self.adb.find_multiple_img(target="upgrade_stone", confidence=0.78)
        upgrades_brut.extend(self.adb.find_multiple_img(target="upgrade_stone2", confidence=0.78))
        upgrades_brut.extend(self.adb.find_multiple_img(target="upgrade_stone3", confidence=0.78))
        upgrades_final = list(filter(lambda co: co[1] < 480, upgrades_brut))
        return upgrades_final

    @get_class
    def run(self):
        if self.data[str(self.sel)]['schedules'][self.current_profile].get('upgrade_city_method', 'normal'):
            self.run1()
        self.setup_view()
        for i in range(2):
            if (upgrades_final := self.free_worker()):
                self.print("Upgrade available.")
                current_build = upgrades_final[0]
                self.click(current_build[0] + uniform(-5, 5), current_build[1] + uniform(-20, 0))
                self.better_sleep((0.9, 1.2))
                self.click(current_build[0] + uniform(-5, 5), current_build[1] + uniform(-20, 0))
                self.better_sleep((0.9, 1.2))
                self.recursive_upgrade()
                self.better_sleep((0.9, 1.2))
                self.better_sleep((10, 15))
                self.help_alliance()
                self.better_sleep((0.9, 1.2))
