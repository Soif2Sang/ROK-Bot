import multiprocessing
import subprocess
import traceback
from random import uniform, randint, shuffle
from time import time, sleep
import win32gui

from tasks.Task_alliance_help import AllianceHelp
from taskscod.COD_Task_alliance_donation import AllianceDonation
from taskscod.COD_Task_clear_fog import ClearFog
from taskscod.COD_Task_training import TroopTraining
from views.Flet_time_allower import is_in_frametime, random_time_in_frametime
from taskscod.COD_Task_claim_campaign import ClaimCampaign
from taskscod.COD_Task_claim_daily_quests import DailyQuests
from taskscod.COD_Task_collect_resource import CollectResource
from taskscod.COD_Task_daily_chest import DailyChest
from taskscod.COD_Task_daily_vip import DailyVip
from taskscod.COD_Task_gather_rss import GatherRss
from pytesseract import pytesseract

from taskscod.COD_Task import Task
from utils.Task_utils import get_name, current_time, get_window_pid, get_path, get_data
from utils.bot_adb import Adb

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'

class TaskRunner(Task):
    def __init__(self, MainTask: Task, tile):
        super().__init__(tile)
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
        return "runner"

    @get_name
    def set_current_task(self, name):
        names = {
            "ClaimCampaign": "Claiming campaign rewards",
            "CollectResource":"Collecting city rss",
            "BuyMerchant" : "Buying merchant..",
            "GatherRss": "Gathering Rss",
            "GatherGem":"Gathering Gem",
            "UseEnhancedBuff": "Enabling enhanced buffs",
            "AllianceDonation": "Donating to alliance",
            "HuntBarbarians":"Killing barbarians",
            "ClearFog" : "Exploring fog",
            "DailyVip":"Daily VIP rewards",
            "DailyChest":"Daily Chest rewards",
            "BarbarianFort":"Launching fort",
            "HealTroop":"Healing troops",
            "ProduceMaterials":"Producing materials",
            "AutoUpgrade":"Upgrading the city..",
            "AllianceHelp": "Helping the alliance..",
            "DailyQuests": "Claiming daily quests..",
            "TroopTraining": "Training troop..",
            "RssTransfer": "Transferring rss.."
        }
        return self.set_status(names.get(name, name))

    @get_name
    def get_current_task(self, name):
        names = {
            "ClaimCampaign": "Claiming campaign rewards",
            "CollectResource": "Collecting city rss",
            "BuyMerchant": "Buying merchant..",
            "GatherRss": "Gathering Rss",
            "GatherGem": "Gathering Gem",
            "UseEnhancedBuff": "Enabling enhanced buffs",
            "AllianceDonation": "Donating to alliance",
            "HuntBarbarians": "Killing barbarians",
            "ClearFog": "Exploring fog",
            "DailyVip": "Daily VIP rewards",
            "DailyChest": "Daily Chest rewards",
            "BarbarianFort": "Launching fort",
            "HealTroop": "Healing troops",
            "ProduceMaterials": "Producing materials",
            "AutoUpgrade": "Upgrading the city..",
            "AllianceHelp": "Helping the alliance..",
            "claim_daily_quests": "Claiming daily quests..",
            "TroopTraining": "Training troop..",
            "RssTransfer": "Transferring rss.."
        }

        return names.get(name,name)

    def execute_tasks(self, lib_tasks, profile):
        co = self.find_img(target="hide_quests")
        if co is not None:
            self.click(co[0] + uniform(0, 20), co[1] + uniform(0, 20))
        current_task = 1
        for func in lib_tasks:
            self.run_game()
            # screen = self.adb.get_cv2_img()
            # screen = self.check_download_page(screen)
            # screen = self.leave_kd_buff(screen)
            #self.print("")
            self.print(f"Task {current_task}/{len(lib_tasks)}","blue")
            self.print(f"Currently executing : {self.get_current_task(func.task_name())}","blue")
            #self.print("")
            self.set_current_task(func.task_name())
            # self.check_log_back(screen)
            # self.check_reconnect()
            # self.set_status()
            if self.data[self.sel]['schedules'][profile].get('alliance_help', False):
                AllianceHelp(self).run()

            if func.task_name() in ["AllianceDonation", "CollectResource", "BuyMerchant", "ClearFog", "HealTroop",
                                 "DailyChest","AutoUpgrade","ProduceMaterials","TroopTraining"]:
                self.go_city()
            try:
                # print(f"{ func.__name__ in ['gather_rss','gather_gem'] =}")
                if func.task_name() in ["GatherRss", "GatherGem"]:
                    cv_image = self.adb.get_cv2_img()
                    cv_image = cv_image[0:100, 0:800]
                    if self.find_img(target="block_icon", source=cv_image, confidence=0.90) is None:
                        func.run()
                    else:
                        self.print("Bot detected that you got restricted","red")
                else:
                    func.run()
                self.better_sleep((1, 2))
            except Exception as e:
                self.print(f"Exception during {func.task_name()}","red")
                exception = traceback.format_exc()
                self.print(f"{exception}","red")
                self.leave_game()
                self.better_sleep((5, 10))
                self.run_game()
            self.close_windows()
            current_task += 1
            # if ('BuyMerchant' in func.task_name()) or ('GatherRss' in func.task_name()):
            #     self.check_captcha()
            #     self.better_sleep((0.795, 1.2))
            # self.check_reconnect()
    def get_available_task(self, profile:str =None):
        self.data = self.update_data()
        if profile is None:
            profile = self.data.get(self.sel)
        else:
            profile = self.data.get(self.sel).get('schedules').get(profile)
        # print(profile)
        lib_tasks = []
        if profile.get('claim_campaign', False):
            lib_tasks.append(ClaimCampaign(self))
        # if profile.get('collect_ressource', False):
        #     lib_tasks.append(CollectResource(self))
        # if profile.get('buy_merchant', False):
        #     lib_tasks.append(BuyMerchant(self))
        if profile.get('gather_rss', False):
            lib_tasks.append(GatherRss(self))
        # if profile.get('use_enhanced_buff', False):
        #     lib_tasks.append(UseEnhancedBuff(self))
        if profile.get('check_donation', False):
            lib_tasks.append(AllianceDonation(self))
        # if profile.get('defeat_barbarians', False):
        #     lib_tasks.append(HuntBarbarians(self))
        # if profile.get('gather_gem', False):
        #     lib_tasks.append(GatherGem(self))
        if profile.get('scout_fog', False):
            lib_tasks.append(ClearFog(self))
        if profile.get('claim_daily_vip', False):
            lib_tasks.append(DailyVip(self))
        # if profile.get('start_fort', False):
            # lib_tasks.append(BarbFort(self))
        # if profile.get('heal_troop', False):
        #     lib_tasks.append(HealTroop(self))
        # if profile.get('material_production', False):
        #     lib_tasks.append(ProduceMaterials(self))
        if profile.get('claim_daily_chest', False):
            lib_tasks.append(DailyChest(self))
        # if profile.get('claim_daily_quests',False):
        #     lib_tasks.append(DailyQuests(self))
        # if profile.get('auto_upgrade', False):
            # lib_tasks.append(UpgradeCity(self))
        if profile.get('train_troops', False):
            lib_tasks.append(TroopTraining(self))
        # if profile.get('transfer_enable',False):
        #     lib_tasks.append(RssTransfer(self))
        shuffle(lib_tasks)
        tasks_name = [task.task_name() for task in lib_tasks]

        if "HuntBarbarians" in tasks_name and "GatherRss" in tasks_name:
            a = tasks_name.index("HuntBarbarians")
            b = tasks_name.index("GatherRss")
            if a > b:
                lib_tasks[a], lib_tasks[b] = lib_tasks[b], lib_tasks[a]

        if "BarbarianFort" in tasks_name:
            for element in ["GatherRss", "GatherGem","hunt_barbarians"]:
                if element in tasks_name:
                    a = tasks_name.index("BarbarianFort")
                    b = tasks_name.index(element)
                    if a > b:
                        lib_tasks[a], lib_tasks[b] = lib_tasks[b], lib_tasks[a]
        # print(f"{lib_tasks}")
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
        while self.find_img(target="logged_icon") is None:
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
                self.send_discord_message("Error in character switch, human interaction required.")
                while True:
                    self.script_pause()
                    sleep(1)
        x, y = self.find_img(target="logged_icon")
        co = self.find_img(target="logged_icon")
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
            x, y = self.find_img(target="logged_icon")
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
            #     self.find_img(target="character_login_confirm")))
            # print(f'[ {current_time()} ] [ {self.name} ] TEST Login')
        self.better_sleep((2.425, 2.795))
        # print(f'[ {current_time()} ] [ {self.data.get(self.sel).get("name","Name not found")} ] character login" + str(
        #     self.find_img(target="character_login_confirm")))
        if self.find_img(target="character_login_confirm") is not None:
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
    def findNextChar(self):
        screen = self.adb.get_cv2_img()
        logged_icon = self.find_img(source=screen,target="logged_icon")
        stars_all = self.adb.find_multiple_img(target="star")
        stars_bellow = []
        for star in stars_all:
            if logged_icon[0] > 640:
                minus = 0
            else:
                minus = 40
            if logged_icon[1]-minus < star[1]:
                stars_bellow.append(star)
        stars_bellow.sort(key=lambda co:co[1])
        final = []
        for star in stars_bellow:
            add = True
            for i in range(-3,4):
                for y in range(-3,4):
                    if (star[0]+i,star[1]+y) in final:
                        add = False
            if add:
                final.append(star)
        if final:
            if logged_icon[0] < 640:
                final.pop(0)
        if final:
            final = final[0]
            self.click(final[0]+uniform(-100,-50),final[1]+uniform(-5,5))

    @get_name
    def change_character_param(self, co_first, nb_chars=0, trigger_stop = False):
        self.print("Switching Character")
        self.set_status(f"Switching Character")
        deadstop = 0
        self.enter_profile()
        self.enter_setting()
        self.enter_characters()
        while self.find_img(target="logged_icon") is None:
            if deadstop == 5:
                if not trigger_stop:
                    self.run_game()
                    self.print(f"Error in character switch. Restarting the character switch..")
                    return self.change_character_param(co_first, nb_chars, trigger_stop = True)
                while trigger_stop:
                    self.print(f"Error in character switch. Bot is now stopped","red")
                    self.set_status("Error.")
                    self.script_pause()
                    sleep(1)
                return
            y1, x1 = uniform(290, 480), uniform(460, 560)
            x2, y2 = x1 + uniform(-30, 30), y1 + uniform(-100, -50)
            self.swipe(x1, y1, x2, y2)
            self.better_sleep((1.925, 2.795))
            deadstop = deadstop + 1
        x, y = self.find_img(target="logged_icon")
        self.print('Current character detected.')
        if x < 1280 // 2:
            # self.print(f"x < 1280 // 2")
            self.click(x + uniform(480, 780), y + uniform(-20, 0))
            self.better_sleep((2.425, 2.795))
        elif y > 520 and x > 1280 // 2:
            # self.print("y > 520 and x > 1280 // 2")
            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)
            self.swipe(x, y, x2, y2)
            self.better_sleep((2.425, 2.795))
            x, y = self.find_img(target="logged_icon")
            self.better_sleep((2.025, 2.795))
            self.findNextChar()
        elif x > 1280 // 2:
            self.findNextChar()
        self.better_sleep((3.425, 3.995))

        if self.find_img(target="character_login_confirm") is not None:
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
    def start_emulator(self, emulator:str):
        path = get_path()
        cmd = f'{path["HD-Player"]} --instance {self.data.get(emulator).get("instance")}'
        self.print(f'Executing {cmd}')
        process = multiprocessing.Process(target=subprocess.Popen, args=(cmd,))
        process.start()

        print(f'Bot will wait 1 min from now.')
        sleep(120)
        if win32gui.FindWindow(None, self.name) is None:
            self.print(f'Executing {cmd}')
            process = multiprocessing.Process(target=subprocess.Popen, args=(cmd,))
            process.start()
            sleep(120)

    @get_name
    def run2(self):
        print("starting")
        self.set_status = lambda text, color=None: print(text)
        self.set_text = lambda text,color=None: print(text)
        self.set_sel("0")
        self.adb.connect_to_device()
        self.data = self.update_data()
        i=0
        loop_task = 1 if not self.data.get(self.sel).get("loop_task") else 9999999999999
        for i in range(loop_task):
            loop_time = time()
            for emulator in sorted(self.data):
                if emulator!="user":
                    self.set_sel(emulator)
                    self.start_emulator(emulator)
                    self.print("Changing adb..")
                    self.print(f"{self.adb.number = } {self.adb.port =}")
                    self.adb = Adb(int(emulator))
                    self.adb.__repr__()
                    self.print("Connecting to the emulator..")
                    self.adb.connect_to_device()

                    self.run_game()
                    self.check_log_back()
                    self.check_reconnect()
                    self.leave_kd_buff()
                    self.check_mge()
                    # First character
                    self.current_profile = "1"
                    self.execute_tasks(self.get_available_task(self.current_profile),self.current_profile)
                    self.better_sleep((2.2, 4))
                    self.go_city()

                    sleep(5)


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
                            self.check_mge()

                            self.execute_tasks(self.get_available_task(self.current_profile))
                            self.better_sleep((2.2, 4))

                            self.go_city()

                            sleep(5)

                            # city_upgrade.run()
                            nb_characters += 1
                            boolean = self.change_character_param(co_first, nb_characters)
                            self.wait_until_connected()

                    self.pid = get_window_pid(self.adb.name)
                    cmd = f"taskkill /PID {self.pid} /F"
                    print(f'[ {current_time()} ] [ {self.name} ] Executing {cmd}')
                    subprocess.Popen(cmd)
                    self.print("Shutdown the emulator, waiting for 15seconds")
                    sleep(15)

            if self.data.get("0").get("loop_task"):
                ttw1, ttw2 = self.data.get("0").get("time_to_wait_loop1", 60), self.data.get("0").get(
                    "time_to_wait_loop2", 90)

                #self.print("")
                self.print(f"Run nb°{i} took {(time() - loop_time) / 60:0.1f} minutes to complete.")
                if ttw1 > ttw2:
                    ttw1, ttw2 = ttw2, ttw1
                time_before_redo_tasks = int(randint(ttw1, ttw2) * 60) + randint(0, 60)
                #self.print("")
                self.print(f"Script is paused for {time_before_redo_tasks / 60:0.1f} minutes")
                # self.set_status((datetime.fromtimestamp(time_before_redo_tasks) - timedelta(hours=1)).strftime("%H:%M:%S"))
                self.set_timer(time_before_redo_tasks)
                if self.data.get("0").get("leave_game_loop", False):
                    if time_before_redo_tasks < 600:
                        self.leave_game(force=True)
                    else:
                        self.leave_game(force=False)

                for _ in range(time_before_redo_tasks):
                    self.script_pause()
                    sleep(1)

    @get_name
    def run(self):
        # self.start_emulator()
        print("starting")
        self.adb.connect_to_device()
        self.data = self.update_data()
        loop_task = 1 if not self.data.get(self.sel).get("loop_task") else 9999999999999
        starting_time = time()
        for i in range(loop_task):
            loop_time = time()
            self.set_status("Starting..")
            self.print("Script is starting ! ".center(20, "-"), "green")
            #self.print("")
            self.data = self.update_data()

            # first_profile_first_instance = True
            #
            # co_first = []
            # nb_profile = 0
            can_go = None
            when_go = None
            for profile in self.data[self.sel]['schedules']:
                if self.data[self.sel]['schedules'][profile]['enabled']:
                    print(f"Profile {profile} enabled")
                    if self.data[self.sel]['schedules'][profile]["enable_timing"]:
                        can_go = False
                        when_go = 0
                        print(f"Profile {profile} enabled")
                        for t in self.data[self.sel]['schedules'][profile]["timing"]:
                            if is_in_frametime(t[0],t[1]):
                                can_go = True
                                when_go = random_time_in_frametime(t[0],t[1])
                                self.print(f"Profile {profile} able to run")
                                break
                        if not can_go:
                            print(f"The current time does not match the rules you set")
                            sleep(5)
                            continue
                        if when_go:
                            self.print("In order to mimic a player, the bot will wait a random time")
                            self.set_timer(when_go)
                    else:
                        print(f"Profile {profile} no rules set")
                    # nb_profile += 1
                    self.current_profile = profile
                    self.print(f"Profile n°{profile} enabled ! ","blue")
                    #self.print("")
                    if self.data.get(self.sel).get('schedules').get(self.current_profile).get("switch_character"):
                        self.print(f"Character n°1", "blue")
                        #self.print("")
                    self.run_game()
                    # self.check_log_back()
                    # self.check_reconnect()
                    # self.check_mge()
                    # self.leave_kd_buff()
                    # First character
                    self.execute_tasks(self.get_available_task(profile),profile)
                    if self.data.get(self.sel).get('schedules').get(self.current_profile).get("switch_character",False):
                        self.close_windows()
                        co_first = self.get_first_character()
                        boolean = True
                        self.wait_until_connected()

                        self.run_game()
                        # Characters remaining
                        nb_characters = 2
                        while boolean:
                            self.print(f"Character n°{nb_characters}","blue")
                            #self.print("")
                            self.run_game()

                            self.check_log_back()
                            self.check_reconnect()
                            self.check_mge()
                            self.leave_kd_buff()

                            self.execute_tasks(self.get_available_task(profile),profile)
                            self.better_sleep((2.2, 4))

                            nb_characters += 1
                            self.close_windows()
                            boolean = self.change_character_param(co_first, nb_characters)
                            self.wait_until_connected()
                    if not self.data[self.sel]['scheduler']:
                        break

            if self.data.get(self.sel).get("loop_task"):
                ttw1, ttw2 = self.data.get(self.sel).get("time_to_wait_loop1", 60), self.data.get(self.sel).get(
                    "time_to_wait_loop2", 90)
                #self.print("")
                heures, minutes = divmod((int(time()) - loop_time), 60)
                minutes,secondes = divmod(int(minutes), 60)
                self.print(f"Run nb°{i} took {int(heures):02d}:{int(minutes):02d}:{int(secondes):02d} to complete.")
                if ttw1 > ttw2:
                    ttw1, ttw2 = ttw2, ttw1
                time_before_redo_tasks = int(randint(ttw1, ttw2) * 60) + randint(0, 60)
                #self.print("")
                self.print(f"Script is paused for {time_before_redo_tasks / 60:0.1f} minutes","#f5b400")
                # self.set_status((datetime.fromtimestamp(time_before_redo_tasks) - timedelta(hours=1)).strftime("%H:%M:%S"))

                if self.data.get(self.sel).get("leave_game_loop", False):
                    if time_before_redo_tasks < 600:
                        self.leave_game(force=True)
                    else:
                        self.leave_game(force=False)

                self.set_timer(time_before_redo_tasks)
        #self.print("")
        self.print(f"The bot took {(time() - starting_time) // 60} minutes to complete all the tasks, bot is waiting for your instructions.","green")
        return


    @get_name
    def run3(self):
        # print("starting")
        self.set_sel(self.tile.get_enabled_sel()[0])
        # self.adb.connect_to_device()
        self.data = self.update_data()
        i=0
        loop_task = 1 if not self.data.get(self.sel).get("loop_task") else 9999999999999
        for i in range(loop_task):
            loop_time = time()

            first=self.tile.get_enabled_sel()[0]
            for emulator in self.tile.get_enabled_sel():
                self.set_sel(emulator)
                self.start_emulator(emulator)
                self.print("Changing adb..")
                self.print(f"{self.adb.number = } {self.adb.port =}")
                self.adb = Adb(int(emulator))
                self.adb.__repr__()
                self.print("Connecting to the emulator..")
                self.adb.connect_to_device()

                self.run_game()
                self.check_log_back()
                self.check_reconnect()
                self.leave_kd_buff()
                self.check_mge()
                # First character
                self.current_profile = "1"
                self.print("Reminder : only the first profile is available")
                self.execute_tasks(self.get_available_task(self.current_profile),self.current_profile)
                self.better_sleep((2.2, 4))
                self.go_city()


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
                        self.check_log_back()
                        self.check_reconnect()
                        self.leave_kd_buff()
                        self.check_mge()

                        self.execute_tasks(self.get_available_task(self.current_profile),self.current_profile)
                        self.better_sleep((2.2, 4))

                        self.go_city()

                        # for i in range(2):
                        #     sleep(5)
                        #     city_upgrade.run()

                        nb_characters += 1
                        boolean = self.change_character_param(co_first, nb_characters)
                        self.wait_until_connected()

                self.leave_game()
                self.pid = get_window_pid(self.adb.name)
                cmd = f"taskkill /PID {self.pid} /F"
                print(f'[ {current_time()} ] [ {self.name} ] Executing {cmd}')
                subprocess.Popen(cmd)
                self.print("Shutdown the emulator, waiting for 15seconds")
                sleep(15)

            if self.data.get(first).get("loop_task"):
                # ttw1, ttw2 = self.data.get(first).get("time_to_wait_loop1", 60), self.data.get(first).get(
                #     "time_to_wait_loop2", 90)
                ttw1,ttw2 = 1,1
                #self.print("")
                self.print(f"Run nb°{i} took {(time() - loop_time) / 60:0.1f} minutes to complete.")
                if ttw1 > ttw2:
                    ttw1, ttw2 = ttw2, ttw1
                time_before_redo_tasks = int(randint(ttw1, ttw2) * 60) + randint(0, 60)
                #self.print("")
                self.print(f"Script is paused for {time_before_redo_tasks / 60:0.1f} minutes")
                # self.set_status((datetime.fromtimestamp(time_before_redo_tasks) - timedelta(hours=1)).strftime("%H:%M:%S"))
                self.set_timer(time_before_redo_tasks)
                # if self.data.get(first).get("leave_game_loop", False):
                #     if time_before_redo_tasks < 600:
                #         self.leave_game(force=True)
                #     else:
                #         self.leave_game(force=False)

                for _ in range(time_before_redo_tasks):
                    self.script_pause()
                    sleep(1)


