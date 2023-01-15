
import json
import traceback
from datetime import datetime, timedelta
from random import uniform, randint, shuffle
from time import time, sleep
from Task_alliance_donation import AllianceDonation
from Task_barb_fort import BarbFort
from Task_buy_merchant import BuyMerchant
from Task_claim_campaign import ClaimCampaign
from Task_clear_fog import ClearFog
from Task_collect_resource import CollectResource
from Task_daily_chest import DailyChest
from Task_daily_vip import DailyVip
from Task_enhanced_buff import UseEnhancedBuff
from Task_gather_gem import GatherGem
from Task_heal_troop import HealTroop
from Task_hunt_barbarians import HuntBarbarians
from Task_produce_materials import ProduceMaterials
import cv2
import numpy as np
from pytesseract import pytesseract

from Task import Task
from Task_utils import get_class, get_name, current_time

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'

class TaskRunner(Task):
    def __init__(self, MainTask:Task, frame):
        super().__init__(frame)
        print("TaskRunner hehe")
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.current_profile = MainTask.current_profile
        self.frame = MainTask.frame
        self.adb = MainTask.frame.adb
        self.ppid = MainTask.ppid
        self.pid = MainTask.pid
        self.language = MainTask.language
        self.name = MainTask.name
        self.resource_type = MainTask.resource_type
        self.sel = MainTask.sel

    def task_name(self):
        return "runner"

    def execute_tasks(self, lib_tasks):
        co = self.adb.find_img(target="hide_quests")
        if co is not None:
            self.click(co[0] + uniform(0, 20), co[1] + uniform(0, 20))
        self.check_download_page()
        current_task = 1
        for func in lib_tasks:
            self.check_download_page()
            self.leave_kd_buff()
            self.print(f"----- Task {current_task}/{len(lib_tasks)} -----".center(60))
            self.print(f"Currently executing : {self.get_current_task(func.task_name())}")
            self.set_current_task(func.task_name())
            self.run_game()
            self.check_log_back()
            self.check_reconnect()
            self.check_resolve()
            # self.set_status()
            if func.task_name() in ["AllianceDonation", "CollectResource", "BuyMerchant", "ClearFog", "HealTroop",
                                 "DailyChest"]:
                self.go_city()
            try:
                # print(f"{ func.__name__ in ['gather_rss','gather_gem'] =}")
                if func.task_name() in ["GatherRss", "GatherGem"]:
                    pil_image = self.adb.get_curr_device_screen_img()
                    cv_image = np.array(pil_image)
                    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
                    cv_image = cv_image[0:100, 0:800]
                    # print(f'{self.adb.find_img_src_conf(cv_image,"block_icon",0.90)=}')
                    if self.adb.find_img(target="block_icon", source=cv_image, confidence=0.90) is None:
                        func.run()
                else:
                    func.run()
                self.better_sleep((1, 2))
            except Exception as e:
                self.print(f"Exception during {func.task_name()}")
                exception = traceback.format_exc()
                self.print(f"{exception}")
                self.leave_game()
                self.better_sleep((5, 10))
                self.run_game()
            self.better_sleep((0.795, 1.2))
            current_task += 1
            if ('BuyMerchant' in func.task_name()) or ('GatherRss' in func.task_name()):
                self.check_resolve()
                self.better_sleep((0.795, 1.2))

    def get_available_task(self, profile=None):
        self.data = self.update_data()
        if profile is None:
            profile = self.data.get(self.sel)
        else:
            profile = self.data.get(self.sel).get('schedules').get(profile)
        # print(profile)
        lib_tasks = []
        if profile.get('claim_campaign', False):
            lib_tasks.append(ClaimCampaign(self))
        if profile.get('collect_ressource', False):
            lib_tasks.append(CollectResource(self))
        if profile.get('buy_merchant', False):
            lib_tasks.append(BuyMerchant(self))
        if profile.get('gather_rss', False):
            lib_tasks.append(BuyMerchant(self))
        if profile.get('use_enhanced_buff', False):
            lib_tasks.append(UseEnhancedBuff(self))
        if profile.get('check_donation', False):
            lib_tasks.append(AllianceDonation(self))
        if profile.get('defeat_barbarians', False):
            lib_tasks.append(HuntBarbarians(self))
        if profile.get('gather_gem', False):
            lib_tasks.append(GatherGem(self))
        if profile.get('scout_fog', False):
            lib_tasks.append(ClearFog(self))
        if profile.get('claim_daily_vip', False):
            lib_tasks.append(DailyVip(self))
        if profile.get('start_fort', False):
            lib_tasks.append(BarbFort(self))
        if profile.get('heal_troop', False):
            lib_tasks.append(HealTroop(self))
        if profile.get('material_production', False):
            lib_tasks.append(ProduceMaterials(self))
        if profile.get('claim_daily_chest', False):
            lib_tasks.append(DailyChest(self))
        shuffle(lib_tasks)
        tasks_name = [task.task_name() for task in lib_tasks]

        if "hunt_barbarians" in tasks_name and "GatherRss" in tasks_name:
            a = tasks_name.index("hunt_barbarians")
            b = tasks_name.index("GatherRss")
            if a > b:
                lib_tasks[a], lib_tasks[b] = lib_tasks[b], lib_tasks[a]

        if "BarbarianFort" in tasks_name:
            for element in ["GatherRss", "GatherGem","hunt_barbarians"]:
                if element in tasks_name:
                    a = lib_tasks.index("BarbarianFort")
                    b = lib_tasks.index(element)
                    if a > b:
                        lib_tasks[a], lib_tasks[b] = lib_tasks[b], lib_tasks[a]
        return lib_tasks

    @get_name
    def enter_profile(self):
        self.click(uniform(28, 64), uniform(24, 52))
        self.better_sleep((1.925, 2.795))

    @get_name
    def enter_setting(self):
        self.click(uniform(957, 1000), uniform(511, 554))
        self.better_sleep((1.925, 2.795))

    @get_name
    def enter_characters(self):
        self.click(uniform(312, 374), uniform(333, 400))
        self.better_sleep((4, 6))

    @get_name
    def get_first_character(self) -> tuple[float, float]:
        self.print("Switching Character")
        self.set_status(f"Switching Character")
        x, y = uniform(15, 80), uniform(10, 60)
        self.click(x, y)
        self.better_sleep((1.925, 2.795))
        x, y = uniform(950, 1015), uniform(510, 560)
        self.click(x, y)
        self.better_sleep((1.925, 2.795))
        x, y = uniform(315, 380), uniform(330, 400)
        self.click(x, y)
        self.better_sleep((4, 5.795))
        trigger_stop = 0
        while self.adb.find_img(target="logged_icon") is None:
            self.check_resolve()
            print(
                f'[ {current_time()} ] [ {self.name} ] while get_first_character')
            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)
            self.swipe(x, y, x2, y2)
            self.better_sleep((1.925, 2.795))
            trigger_stop += 1
            if trigger_stop > 4:
                self.print("Error in character switch. Bot is now stopped")
                self.set_status("Error.")
                while True:
                    self.script_pause()
                    sleep(1)
        x, y = self.adb.find_img(target="logged_icon")
        co = self.adb.find_img(target="logged_icon")
        self.print("Current character detected.")
        if x < 1280 // 2:
            x2 = x + uniform(480, 780)
            y2 = y + uniform(-20, 0)
            self.click(x2, y2)
            self.better_sleep((2.425, 2.795))
        elif y > 520 and x > 1280 // 2:
            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)
            self.swipe(x, y, x2, y2)
            self.better_sleep((2.425, 2.795))
            x, y = self.adb.find_img(target="logged_icon")
            self.better_sleep((2.025, 2.795))
            x2 = x - uniform(100, 320)
            y2 = y + uniform(80, 100)
            self.click(x2, y2)
            self.better_sleep((2.425, 2.795))
        elif x > 1280 // 2:
            x2 = x - uniform(100, 320)
            y2 = y + uniform(80, 100)
            self.click(x2, y2)
            self.better_sleep((2.425, 2.795))
            # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] test login" + str(
            #     self.adb.find_img(target="character_login_confirm")))
            # print(f'[ {current_time()} ] [ {self.name} ] TEST Login')
        self.better_sleep((2.425, 2.795))
        # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] character login" + str(
        #     self.adb.find_img(target="character_login_confirm")))
        if self.adb.find_img(target="character_login_confirm") is not None:
            self.print("Switching between character")
            x, y = uniform(700, 900), uniform(490, 527)
            self.click(x, y)
            # self.better_sleep((10, 15))
            # self.check_crash()
            # self.run_game()
            return co[0] + uniform(0, 5), co[1] + uniform(0, 5),
        else:
            self.print("No more characters, going back to the first character")
            x, y = uniform(400, 800), uniform(200, 250)
            x2, y2 = x + uniform(-20, 20), uniform(580, 645)
            self.swipe(x, y, x2, y2)
            self.better_sleep((3.5, 4.7))
            x, y = uniform(660, 1000), uniform(215, 280)
            self.click(x, y)
            self.better_sleep((1.8, 2.7))
            x, y = uniform(700, 910), uniform(491, 522)
            self.click(x, y)
            return uniform(660, 1000), uniform(215, 280)


    @get_name
    def change_character_param(self, co_first, nb_chars=0):
        self.print("Switching Character")
        self.set_status(f"Switching Character")
        deadstop = 0
        self.enter_profile()
        self.enter_setting()
        self.enter_characters()
        while self.adb.find_img(target="logged_icon") is None:
            if deadstop == 5:
                self.print(f"Error in character switch. Bot is now stopped")
                self.set_status("Error.")
                while True:
                    self.script_pause()
                    sleep(1)
            self.check_resolve()
            y1, x1 = uniform(290, 480), uniform(460, 560)
            x2, y2 = x1 + uniform(-30, 30), y1 + uniform(-100, -50)
            self.swipe(x1, y1, x2, y2)
            self.better_sleep((1.925, 2.795))
            deadstop = deadstop + 1
        x, y = self.adb.find_img(target="logged_icon")
        self.print('Current character detected.')
        if x < 1280 // 2:
            self.print(f"x < 1280 // 2")
            self.click(x + uniform(480, 780), y + uniform(-20, 0))
            self.better_sleep((2.425, 2.795))
        elif y > 520 and x > 1280 // 2:
            self.print("y > 520 and x > 1280 // 2")
            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)
            self.swipe(x, y, x2, y2)
            self.better_sleep((2.425, 2.795))
            x, y = self.adb.find_img(target="logged_icon")
            self.better_sleep((2.025, 2.795))
            self.click(x - uniform(100, 320), y + uniform(80, 100))
            self.better_sleep((2.425, 2.795))
        elif x > 1280 // 2:
            self.print("x > 1280 // 2")
            self.click(x - uniform(100, 320), y + uniform(80, 100))
            self.better_sleep((2.425, 2.795))
        self.better_sleep((3.425, 3.995))
        if self.adb.find_img(target="character_login_confirm") is not None:
            self.print("Switching to the next character")
            self.click(uniform(700, 900), uniform(490, 527))
            return True
        else:
            self.print("No more characters, going back to the first character")
            x, y = uniform(400, 800), uniform(200, 250)
            if nb_chars // 6 == 0:
                rounds = 1
            else:
                rounds = nb_chars // 6
            if rounds == 0:
                rounds = +1
            for _ in range(rounds):
                x2, y2 = x + uniform(-20, 20), uniform(580, 645)
                self.swipe(x, y, x2, y2)
                self.better_sleep((3.5, 4.7))
            self.click(co_first[0] + uniform(30, 300), co_first[1] + uniform(-30, 0))
            self.better_sleep((1.8, 2.7))
            x, y = uniform(700, 910), uniform(491, 522)
            self.click(x, y)
            return False


    @get_name
    def routine_scheduled(self):
        print("starting")
        self.adb.connect_to_device()
        self.data = self.update_data()

        loop_task = 1 if not self.data.get(self.sel).get("loop_task") else 9999999999999

        starting_time = time()
        for i in range(loop_task):
            loop_time = time()
            self.set_status("Starting..")
            self.print(" Script is starting ! ".center(56, "-"))
            self.data = self.update_data()
            for profile in self.data[self.sel]['schedules']:
                if self.data[self.sel]['schedules'][profile]['enabled']:
                    self.current_profile = profile
                    self.print(f" Profile n°{profile} enabled ! ".center(60))
                    if self.data.get(self.sel).get('schedules').get(self.current_profile).get("switch_character"):
                        self.print(f"---- Character n°1 ----".center(60))
                    self.run_game()
                    self.check_log_back()
                    self.check_reconnect()
                    self.leave_kd_buff()
                    self.check_mge()
                    self.check_resolve()
                    # First character
                    self.execute_tasks(self.get_available_task(profile))
                    if self.data.get(self.sel).get('schedules').get(self.current_profile).get("switch_character",
                                                                                              False):
                        co_first = self.get_first_character()
                        boolean = True
                        self.wait_until_connected()

                        self.run_game()
                        # Characters remaining
                        nb_characters = 2
                        while boolean:
                            self.print(f"---- Character n°{nb_characters} ----".center(60))
                            self.run_game()
                            self.check_resolve()
                            self.check_mge()

                            self.execute_tasks(self.get_available_task(profile))
                            self.better_sleep((2.2, 4))

                            nb_characters += 1
                            boolean = self.change_character_param(co_first, nb_characters)
                            self.wait_until_connected()
                    if not self.data[self.sel]['scheduler']:
                        break

            if self.data.get(self.sel).get("loop_task"):
                ttw1, ttw2 = self.data.get(self.sel).get("time_to_wait_loop1", 60), self.data.get(self.sel).get(
                    "time_to_wait_loop2", 90)
                self.print(f"Run nb°{i} took {(time() - loop_time) / 60:0.1f} minutes to complete.")
                if ttw1 > ttw2:
                    ttw1, ttw2 = ttw2, ttw1
                time_before_redo_tasks = int(randint(ttw1, ttw2) * 60) + randint(0, 60)
                self.print(f"Script is paused for {time_before_redo_tasks / 60:0.1f} minutes")
                self.set_status((datetime.fromtimestamp(time_before_redo_tasks) - timedelta(hours=1)).strftime("%H:%M:%S"))
                if self.data.get(self.sel).get("leave_game_loop", False):
                    if time_before_redo_tasks < 600:
                        self.leave_game(force=True)
                    else:
                        self.leave_game(force=False)

                for _ in range(time_before_redo_tasks):
                    self.script_pause()
                    sleep(1)

        self.print(f"The bot took {(time() - starting_time) // 60} minutes to complete all the tasks, bot is waiting for your instructions.")
        return
