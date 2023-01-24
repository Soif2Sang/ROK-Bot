import json
from random import uniform, choice
from pytesseract import pytesseract
from Task import Task
from Task_utils import get_class, get_name

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class UpgradeCity(Task):
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
        if co := self.adb.find_img(target='help_build', confidence=0.8):
            self.click(co[0] + uniform(0, 10), co[1] + uniform(20, 40))
            self.better_sleep((0.9, 1.2))

    @get_name
    def recursive_upgrade(self):
        co = self.adb.find_img(target="upgrade_build")
        if co is not None:
            self.click(co[0] + uniform(0, 20), co[1] + uniform(0, 30))
            self.better_sleep((0.9, 1.2))
            if co := self.adb.find_img(target="upgrade_go"):
                self.click(co[0] + uniform(0, 50), co[1] + uniform(0, 20))
                self.better_sleep((0.9, 1.2))
                return self.recursive_upgrade()
            else:
                self.click(uniform(916, 1050), uniform(530, 560))
                self.better_sleep((1.7, 2.2))
                if (co:=self.adb.find_img(target="hire_constructor")) is not None or (co:=self.adb.find_img(target="hire_constructor2")):
                    self.click(co[0] + uniform(0,110), co[1] + uniform(0,40))
                    self.better_sleep((1.7, 2.2))
                    self.click(uniform(916, 1050), uniform(530, 560))
                    self.better_sleep((1.7, 2.2))
                while co := self.adb.find_img(target="close_window"):
                    self.click(co[0] + uniform(10, 15), co[1] + uniform(10, 15))
                    self.better_sleep((1.7, 2.2))
            self.better_sleep((1.7, 2.2))
            self.help_build()
            self.better_sleep((1.7, 2.2))

    @get_name
    def setup_view(self):
        x = uniform(33, 76)
        y = uniform(517, 560)
        # print(x,y)
        self.click(x, y)
        self.better_sleep((0.9, 1.5))
        x = uniform(1096, 1120)
        y = uniform(186, 210)
        self.click(x, y)
        self.better_sleep((0.9, 1.5))
        x = uniform(1223, 1241)
        y = uniform(28, 46)
        self.click(x, y)
        self.better_sleep((0.9, 1.5))

    @get_name
    def is_city_hall_upgradable(self):
        co = self.adb.find_img(target="upgrade_build")
        if co is not None:
            return True
        return False

    @get_name
    def help_alliance(self):
        if co := self.adb.find_img(target='help_alliance', confidence=0.75):
            self.click(co[0] + uniform(0, 10), co[1] + uniform(20, 40))
            self.better_sleep((0.9, 1.2))

    @get_name
    def free_constructor(self):
        if self.adb.find_img("upgrade_stone") is None and self.adb.find_img("upgrade_stone2") is None:
            return False
        return True

    @get_class
    def run1(self):
        for x, y in [self.pass_coordinates(), self.barracks_coordinates(), self.archery_coordinates(), self.stable_coordinates(),
                     self.siege_coordinates(), self.tavern_coordinates(), self.ch_coordinates(), self.hospital_coordinates(),
                     self.academy_coordinates(), self.alliance_center_coordinates(), self.scout_coordinates()]:
            self.setup_view()
            if not self.free_constructor():
                break
            self.better_sleep((0.9, 1.2))
            for i in range(2):
                self.click(x, y)
                self.better_sleep((0.9, 1.2))
            if self.is_city_hall_upgradable():
                self.recursive_upgrade()
            else:
                self.print("Already upgrading..")
            self.better_sleep((0.9, 1.2))
        for i in range(2):
            self.help_build()
            self.better_sleep((0.9, 1.2))
        self.better_sleep((10, 15))
        self.help_alliance()
        self.better_sleep((0.9, 1.2))

    @get_name
    def free_worker(self):
        upgrades_brut = self.adb.find_multiple_img(target="upgrade_stone",confidence=0.92)
        upgrades_brut.extend(self.adb.find_multiple_img(target="upgrade_stone2",confidence=0.92))
        upgrades_brut.extend(self.adb.find_multiple_img(target="upgrade_stone3", confidence=0.92))
        upgrades_final = list(filter(lambda co: co[1]<480, upgrades_brut))
        return upgrades_final


    @get_class
    def run(self):
        if (upgrades_final:=self.free_worker()):
            current_build = upgrades_final[0]
            self.click(current_build[0]+uniform(-5,5), current_build[1]+uniform(-20,0))
            self.better_sleep((0.9, 1.2))
            self.click(current_build[0]+uniform(-5,5), current_build[1]+uniform(-20,0))
            self.better_sleep((0.9, 1.2))
            self.recursive_upgrade()
            self.better_sleep((0.9, 1.2))
        self.better_sleep((10, 15))
        self.help_alliance()
        self.better_sleep((0.9, 1.2))