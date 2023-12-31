import multiprocessing
import subprocess
import traceback
from datetime import timedelta
from random import randint, shuffle, uniform
from time import sleep, time

import flet as ft
import win32gui
from PIL import Image

from tasks.Task import Task
from tasks.Task_academy_research import AcademyResearch
from tasks.Task_alliance_donation import AllianceDonation
from tasks.Task_alliance_help import AllianceHelp
from tasks.Task_alliance_pit import AlliancePit
from tasks.Task_barb_fort import BarbFort
from tasks.Task_buy_merchant import BuyMerchant
from tasks.Task_claim_campaign import ClaimCampaign
from tasks.Task_claim_daily_quests import DailyQuests
from tasks.Task_claim_mail import ClaimMail
from tasks.Task_clear_fog import ClearFog
from tasks.Task_collect_resource import CollectResource
from tasks.Task_daily_chest import DailyChest
from tasks.Task_daily_vip import DailyVip
from tasks.Task_enhanced_buff import UseEnhancedBuff
from tasks.Task_gather_gem_default import GatherGemDefault
from tasks.Task_gather_gem_spiral import GatherGemSpiral
from tasks.Task_gather_rss_default import GatherRssDefault
from tasks.Task_gather_rss_zoom import GatherRssZoom
from tasks.Task_heal_troop import HealTroop
from tasks.Task_hunt_barbarians import HuntBarbarians
from tasks.Task_maraudeurs import Marauders
from tasks.Task_produce_materials import ProduceMaterials
from tasks.Task_rss_transfert import RssTransfer
from tasks.Task_training import TroopTraining
from tasks.Task_upgrade_city import UpgradeCity
from utils.android_debug_bridge import Adb
from utils.android_debug_bridge_ld_player import AdbLd
from utils.functions import current_time, get_dic_instances, get_name, get_window_pid
from utils.singletons import ApiSingleton, LinkSingleton
from views.frametime import is_in_frametime, random_time_in_frametime


class TaskRunner(Task):
    def __init__(self, MainTask: Task, tile):
        super().__init__(MainTask.tile)
        self.herite(MainTask)

    def task_name(self):
        return "runner"

    @get_name
    def set_current_task(self, name):
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
            "RssTransfer": "Transferring rss..",
            "Maraudeurs": "Killing Marauders..",
            "UpgradeCity": "Upgrading the city..",
            "AlliancePit": "Alliance Pit",
            "AcademyResearch": "Academic researches",
        }

        return self.set_status(names.get(name, name))

    @get_name
    def get_current_task(self, name):
        names = {
            "ClaimCampaign": "Claiming campaign rewards",
            "CollectResource": "Collecting city rss",
            "BuyMerchant": "Buying merchant..",
            "GatherRssDefault": "Gathering Rss",
            "GatherRssZoom": "Gathering Rss",
            "GatherGemSpiral": "Gathering Gem",
            "GatherGemDefault": "Gathering Gem",
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
            "RssTransfer": "Transferring rss..",
            "Maraudeurs": "Killing Marauders..",
            "UpgradeCity": "Upgrading the city..",
            "AlliancePit": "Alliance Pit",
            "AcademyResearch": "Academic researches",
        }

        return names.get(name, name)

    def execute_tasks(self, lib_tasks, profile):
        self.adb.connect_to_device()
        self.run_game()
        screen = self.adb.get_cv2_img()

        self.close_windows()

        co = self.find_img(target="hide_quests", source=screen[:300, :300])
        if co is not None:
            self.click(co[0] + uniform(0, 20), co[1] + uniform(0, 20))
        current_task = 1
        self.check_captcha()

        for func in lib_tasks:
            self.print(f"Task {current_task}/{len(lib_tasks)}", "blue")
            self.print(
                f"Currently executing : {self.get_current_task(func.task_name())}",
                "blue",
            )

            self.run_game()
            screen = self.check_mge(screen)
            screen = self.check_download_page(screen)
            screen = self.leave_kd_buff(screen)
            self.check_log_back(screen)
            self.check_reconnect()
            self.set_current_task(func.task_name())
            # self.set_status()
            if self.data[self.sel]["schedules"][profile].get("alliance_help", False):
                AllianceHelp(self).run()

            if func.task_name() in [
                "CollectResource",
                "BuyMerchant",
                "ClearFog",
                "HealTroop",
                "DailyChest",
                "AutoUpgrade",
                "ProduceMaterials",
                "TroopTraining",
                "UpgradeCity",
                "AcademyResearch"
            ]:
                self.go_city()
            try:
                if func.task_name() in ["GatherRss", "GatherGem"]:
                    cv_image = self.adb.get_cv2_img()
                    cv_image = cv_image[0:100, 0:800]
                    if (
                        self.find_img(
                            target="block_icon", source=cv_image, confidence=0.90
                        )
                        is None
                    ):
                        func.run()
                    else:
                        self.print("Bot detected that you got restricted", "red")
                else:
                    if func.task_name() in ["GatherRss", "GatherGem"]:
                        self.check_captcha()
                    func.run()
                self.better_sleep((1, 2))
            except Exception as e:
                traceback.print_exc()
                self.send_discord_message(
                    f"Something wrong happened when running {func.task_name()}"
                )
                self.generate_toast(
                    "Warning",
                    f"Something wrong happened when running {func.task_name()}",
                )

                self.print(f"Exception during {func.task_name()}", "red")
                exception = traceback.format_exc()
                self.print(f"{exception}", "red")
                self.leave_game()
                self.better_sleep((5, 10))
                self.run_game()
            finally:
                self.close_windows()
                current_task += 1
            # if ('BuyMerchant' in func.task_name()) or ('GatherRss' in func.task_name()):
            #     self.check_captcha()
            #     self.better_sleep((0.795, 1.2))
            # self.check_reconnect()
        self.check_captcha()

    def get_available_task(self, profile: str = None):
        # self.data = self.update_data()
        if profile is None:
            profile = self.data.get(self.sel)
        else:
            profile = self.data.get(self.sel).get("schedules").get(profile)
        # print(profile)
        lib_tasks = []

        tasks = [
            ("claim_campaign", ClaimCampaign),
            ("collect_ressource", CollectResource),
            ("buy_merchant", BuyMerchant),
            (
                "gather_rss",
                GatherRssDefault
                if not profile.get("gather_rss_method")
                else GatherRssZoom,
            ),
            ("use_enhanced_buff", UseEnhancedBuff),
            ("check_donation", AllianceDonation),
            ("defeat_barbarians", HuntBarbarians),
            (
                "gather_gem",
                GatherGemDefault
                if not profile.get("gather_gem_spiral_method")
                else GatherGemSpiral,
            ),
            ("scout_fog", ClearFog),
            ("claim_daily_vip", DailyVip),
            ("start_fort", BarbFort),
            ("heal_troop", HealTroop),
            ("material_production", ProduceMaterials),
            ("claim_daily_chest", DailyChest),
            ("claim_daily_quests", DailyQuests),
            ("auto_upgrade", UpgradeCity),
            ("train_troops", TroopTraining),
            ("transfer_enable", RssTransfer),
            ("kill_marauders", Marauders),
            ("gather_alliance_pit", AlliancePit),
            ("academic_research", AcademyResearch),
        ]

        lib_tasks = [
            task_class(self)
            for profile_key, task_class in tasks
            if profile.get(profile_key, False)
        ]
        shuffle(lib_tasks)
        tasks_names = [task.task_name() for task in lib_tasks]

        if ("AlliancePit" in tasks_names) and ("GatherRss" in tasks_names):
            alliance_pit_index = tasks_names.index("AlliancePit")
            gather_index = tasks_names.index("GatherRss")
            if gather_index < alliance_pit_index:
                lib_tasks[alliance_pit_index], lib_tasks[gather_index] = (
                    lib_tasks[gather_index],
                    lib_tasks[alliance_pit_index],
                )

        if ("HuntBarbarians" in tasks_names) and ("GatherRss" in tasks_names):
            hunt_index = tasks_names.index("HuntBarbarians")
            gather_index = tasks_names.index("GatherRss")
            if gather_index < hunt_index:
                lib_tasks[hunt_index], lib_tasks[gather_index] = (
                    lib_tasks[gather_index],
                    lib_tasks[hunt_index],
                )

        if ("BarbarianFort" in tasks_names) and ("GatherRss" in tasks_names):
            hunt_index = tasks_names.index("BarbarianFort")
            gather_index = tasks_names.index("GatherRss")
            if gather_index < hunt_index:
                lib_tasks[hunt_index], lib_tasks[gather_index] = (
                    lib_tasks[gather_index],
                    lib_tasks[hunt_index],
                )

        if profile.get("upgrade_city", False):
            lib_tasks.append(UpgradeCity(self))

        if ("TroopTraining" in tasks_names) and self.tile.initial_page.UPGRADE:
            lib_tasks.pop(tasks_names.index("TroopTraining"))
            lib_tasks.append(TroopTraining(self))

        if profile.get("claim_mails", False):
            lib_tasks.append(ClaimMail(self))
        return lib_tasks

    @get_name
    def enter_profile(self):
        self.click(uniform(28, 64), uniform(24, 52))

    @get_name
    def enter_setting(self):
        self.click(uniform(991, 1026), uniform(570, 600))

    @get_name
    def enter_characters(self):
        self.click(uniform(312, 374), uniform(333, 400))

    @get_name
    def switch_character(
        self, co_first=None, nb_chars=0, fail=0
    ) -> tuple[float, float] or bool:
        self.print("Switching Character")
        self.set_status(f"Switching Character")
        self.close_windows()
        self.check_captcha()

        self.enter_profile()
        self.better_sleep((1.925, 2.795))
        self.enter_setting()
        self.better_sleep((1.925, 2.795))

        first_color = Image.fromarray(self.adb.get_cv2_img()).getpixel((344, 326))
        self.enter_characters()
        self.better_sleep((0.925, 1.795))

        if self.find_img('star') is None:
            self.click(uniform(600,900),uniform(170,177))
            self.better_sleep((1.925, 2.795))

        stop = 0
        while (
            Image.fromarray(self.adb.get_cv2_img()).getpixel((344, 326)) == first_color
        ):
            self.better_sleep((2, 3))
            stop += 1

            if stop == 10:
                self.print("It seems the game is unable to load the characters menu..")
                self.run_game()
                return self.switch_character(co_first, nb_chars, fail)

            if co := self.find_img(target="chest_confirm_button"):
                self.click(*co)
                self.better_sleep((1, 2))
            if co := self.find_img(target="reconnect_sdk"):
                self.click(*co)
                self.better_sleep((1, 2))

        self.better_sleep((1.925, 2.795))
        trigger_stop = 0

        while self.find_img(target="logged_icon", confidence=0.7) is None:
            self.check_captcha()
            self.check_captcha_slider()

            self.print("Looking for current character")

            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)

            self.swipe(x, y, x2, y2)
            self.better_sleep((1.925, 2.795))

            trigger_stop += 1
            if trigger_stop == 4:
                self.close_windows()
                self.close_upgrade_popup()
                self.check_captcha()
                self.print("Cannot locate the current user, trying to restart the task")
                return self.switch_character(co_first, nb_chars, fail + 1)

            if fail > 2:
                self.print("Error in character switch. Bot is now stopped")
                self.set_status("Error.")
                self.send_discord_message(
                    "Error in character switch, human interaction required."
                )
                while True:
                    self.script_pause()
                    sleep(0.1)

        x, y = self.find_img(target="logged_icon", confidence=0.7)
        default = self.find_img(target="logged_icon", confidence=0.7)
        self.print("Current character detected.")

        if y > 520 and x > 1280 // 2:
            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)
            self.swipe(x, y, x2, y2)
            self.better_sleep((2.425, 2.795))

        self.better_sleep((2.425, 2.795))

        if self.click_next_prefered_character():
            self.print("Switching to the next character")
            self.better_sleep((2.425, 2.795))
            x, y = self.find_img(target="character_login_confirm")
            self.click(x, y)
            return default
        elif co_first is None:
            self.print(
                "Unable to find more characters, the current character is maybe the last favorite or there's simply no favorite characters",
                "yellow",
            )
            self.close_windows()
            return False
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
    def click_next_prefered_character(self):
        screen = self.adb.get_cv2_img()
        logged_icon = self.find_img(source=screen, target="logged_icon", confidence=0.7)
        all_prefered_characters = self.adb.find_multiple_img(
            source=screen, target="star"
        )
        next_prefered_characters = []

        for star in all_prefered_characters:
            if logged_icon[0] > 640:
                minus = 0
            else:
                minus = 40
            if logged_icon[1] - minus < star[1]:
                next_prefered_characters.append(star)

        next_prefered_characters.sort(key=lambda co: co[1])
        cleaned_next_characters = []
        for star in next_prefered_characters:
            add = True
            for i in range(-3, 4):
                for y in range(-3, 4):
                    if (star[0] + i, star[1] + y) in cleaned_next_characters:
                        add = False
            if add:
                cleaned_next_characters.append(star)
        if cleaned_next_characters:
            if logged_icon[0] < 640:
                cleaned_next_characters.pop(0)
        if cleaned_next_characters:
            cleaned_next_characters = cleaned_next_characters[0]

            cords = cleaned_next_characters[0] + uniform(
                -100, -50
            ), cleaned_next_characters[1] + uniform(-5, 5)
            self.click(cords[0], cords[1])
            return cords[0], cords[1]
        return False

    @get_name
    def change_character_param(self, co_first, nb_chars=0, fail=0):
        self.print("Switching Character")
        self.set_status(f"Switching Character")
        self.close_windows()
        self.enter_profile()
        self.better_sleep((1.925, 2.795))
        self.enter_setting()
        self.better_sleep((1.925, 2.795))
        first_color = Image.fromarray(self.adb.get_cv2_img()).getpixel((344, 326))
        self.enter_characters()
        stop = 0

        while (
            Image.fromarray(self.adb.get_cv2_img()).getpixel((344, 326)) == first_color
        ):
            self.better_sleep((1, 2))
            stop += 1

            if stop == 10:
                self.print("It seems the game is unable to load the characters menu..")
                return self.change_character_param(self, co_first, nb_chars, fail)

        self.better_sleep((1.925, 2.795))
        trigger_stop = 0

        while self.find_img(target="logged_icon", confidence=0.7) is None:
            self.check_captcha()
            self.check_captcha_slider()

            self.print("Looking for current character")

            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)

            self.swipe(x, y, x2, y2)
            self.better_sleep((1.925, 2.795))

            trigger_stop += 1
            if trigger_stop == 4:
                self.close_windows()
                self.close_upgrade_popup()
                self.check_captcha()
                print("Cannot locate the current user, trying to restart the task")
                return self.change_character_param(co_first, nb_chars, fail + 1)

            if fail > 2:
                self.print("Error in character switch. Bot is now stopped")
                self.set_status("Error.")
                self.send_discord_message(
                    "Error in character switch, human interaction required."
                )
                while True:
                    self.script_pause()
                    sleep(0.1)

        x, y = self.find_img(target="logged_icon", confidence=0.7)
        self.print("Current character detected.")

        if y > 520 and x > 1280 // 2:
            # self.print("y > 520 and x > 1280 // 2")
            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)
            self.swipe(x, y, x2, y2)
            self.better_sleep((2.425, 2.795))

        self.better_sleep((2.425, 2.795))

        if self.click_next_prefered_character():
            self.print("Switching to the next character")
            self.click(**self.find_img(target="character_login_confirm"))
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
    def start_emulator(self, emulator: str):
        path = self.FileSingleton.get_path()
        data = self.FileSingleton.get_data()

        cmd = (
            f'{path["HD-Player"]} --instance {self.data.get(emulator).get("instance")}'
        )
        self.print(f"Executing cmd")

        subprocess.Popen(cmd)


        if win32gui.FindWindow(None, self.name) is None:
            self.print(f"Executing cmd")
            subprocess.Popen(cmd)
            print(f"Bot will wait 2 min from now.")

            self.better_sleep((120, 120))

        instances = get_dic_instances()
        for instance in instances:
            data[str(instance)]["instance"] = instances[str(instance)]["instance"]
            data[str(instance)]["name"] = instances[str(instance)]["name"]
            data[str(instance)]["port"] = int(instances[str(instance)]["port"])
        self.data = data
        self.FileSingleton.write_data(data)
        self.tile.main_task.adb.connect_to_device()
        self.tile.runner.adb.connect_to_device()

    @get_name
    def run(self):
        self.data = self.update_data()
        loop_task = 1 if not self.data.get(self.sel).get("loop_task") else 9999999999999
        starting_time = time()
        print(self.sel)
        print(self.data[self.sel]["name"])
        for i in range(loop_task):
            loop_time = time()
            self.set_status("Starting..")
            self.print("Script is starting ! ".center(20, "-"), "green")
            self.data = self.update_data()

            can_go = None
            when_go = None
            if not (
                self.data[self.sel]["schedules"]["1"]["enabled"]
                or self.data[self.sel]["schedules"]["2"]["enabled"]
                or self.data[self.sel]["schedules"]["3"]["enabled"]
            ):
                self.print(
                    "No active profiles found! Navigate to the profile settings and enable at least one option.",
                    "red",
                )
                self.generate_toast(
                    "Warning ",
                    "No active profiles found! Navigate to the profile settings and enable at least one option.",
                    ft.icons.INFO,
                )

            for profile in self.data[self.sel]["schedules"]:
                if self.data[self.sel]["schedules"][profile]["enabled"]:
                    print(f"Profile {profile} enabled")
                    if self.data[self.sel]["schedules"][profile]["enable_timing"]:
                        can_go = False
                        when_go = 0
                        print(f"Profile {profile} enabled")
                        for t in self.data[self.sel]["schedules"][profile]["timing"]:
                            if is_in_frametime(t[0], t[1]):
                                can_go = True
                                when_go = random_time_in_frametime(t[0], t[1])
                                print(f"{when_go=}")
                                self.print(f"Profile {profile} able to run")
                                break
                        if not can_go:
                            print(f"The current time does not match the rules you set")
                            sleep(5)
                            continue
                        if when_go:
                            self.print(
                                "In order to mimic a player, the bot will wait a random time"
                            )
                            self.set_timer(randint(0, 60 * 10))
                            self.set_status("Starting..")
                    else:
                        print(f"Profile {profile} no rules set")
                    self.current_profile = profile
                    self.print(f"Profile n°{profile} enabled ! ", "blue")

                    if self.get_config().get("switch_character"):
                        self.print(f"Character n°1", "blue")
                    # First character
                    self.execute_tasks(self.get_available_task(profile), profile)

                    if self.get_config().get("switch_character", False):
                        self.check_captcha()
                        co_first = self.switch_character()
                        self.wait_until_connected()
                        # Characters remaining
                        boolean = True
                        nb_characters = 2
                        while co_first and boolean:
                            self.print(f"Character n°{nb_characters}", "blue")
                            nb_characters += 1
                            self.execute_tasks(
                                self.get_available_task(profile), profile
                            )
                            self.better_sleep((1.2, 4))

                            self.check_captcha()
                            boolean = self.switch_character(co_first, nb_characters, 0)
                            self.wait_until_connected()
                    if not self.data[self.sel]["scheduler"]:
                        break

            if self.data.get(self.sel).get("loop_task"):
                ttw1 = self.data.get(self.sel).get("time_to_wait_loop1", 60)
                ttw2 = self.data.get(self.sel).get("time_to_wait_loop2", 90)

                self.print(
                    f"Run nb°{i} took {timedelta(seconds=int(time() - loop_time))} to complete."
                )
                if ttw1 > ttw2:
                    ttw1, ttw2 = ttw2, ttw1
                time_before_redo_tasks = int(randint(ttw1, ttw2) * 60) + randint(0, 60)
                self.print(
                    f"Script is paused for {timedelta(seconds=int(time_before_redo_tasks))}",
                    "#f5b400",
                )

                if self.data.get(self.sel).get("leave_game_loop", False):
                    if time_before_redo_tasks < 600:
                        self.leave_game(force=True)
                    else:
                        self.leave_game(force=False)

                self.set_timer(time_before_redo_tasks)

        self.print(
            f"The bot took {timedelta(seconds=int(time() - starting_time))} to complete all the tasks, bot is waiting for your instructions.",
            "green",
        )
        self.set_divider()
        return

    @get_name
    def run3(self):
        # print("starting")
        self.set_sel(self.tile.get_enabled_sel()[0])
        # self.adb.connect_to_device()
        self.data = self.update_data()
        i = 0
        loop_task = 1 if not self.data.get(self.sel).get("loop_task") else 9999999999999
        for i in range(loop_task):
            loop_time = time()

            first = self.tile.get_enabled_sel()[0]
            print(self.tile.get_enabled_sel())
            for emulator in self.tile.get_enabled_sel():
                self.set_sel(emulator)
                self.start_emulator(emulator)
                self.print("Changing adb..")
                self.print(f"{self.adb.number = } {self.adb.port =}")
                self.adb = Adb(emulator)
                self.adb.__repr__()
                self.print("Connecting to the emulator..")
                self.adb.connect_to_device()

                self.run_game()
                self.check_log_back()
                self.check_reconnect()
                self.leave_kd_buff()
                self.check_mge()
                self.check_captcha()
                # First character
                self.current_profile = "1"
                self.print("Reminder : only the first profile is available")
                self.execute_tasks(
                    self.get_available_task(self.current_profile), self.current_profile
                )
                self.better_sleep((2.2, 4))
                # self.go_city()
                # city_upgrade = UpgradeCity(self)
                # city_upgrade.setup_view()
                #
                # for i in range(2):
                #     sleep(5)
                #     city_upgrade.run()

                if (
                    self.data.get(self.sel)
                    .get("schedules")
                    .get(self.current_profile)
                    .get("switch_character", False)
                ):
                    co_first = self.switch_character()
                    boolean = True
                    self.wait_until_connected()

                    self.run_game()
                    # Characters remaining
                    nb_characters = 2
                    while co_first and boolean:
                        self.print(f"---- Character n°{nb_characters} ----".center(60))
                        self.run_game()
                        self.check_log_back()
                        self.check_reconnect()
                        self.leave_kd_buff()
                        self.check_mge()
                        self.check_captcha()

                        self.execute_tasks(
                            self.get_available_task(self.current_profile),
                            self.current_profile,
                        )
                        self.better_sleep((2.2, 4))

                        nb_characters += 1
                        boolean = self.switch_character(co_first, nb_characters)
                        self.wait_until_connected()

                self.leave_game()
                self.pid = get_window_pid(self.adb.name)
                cmd = f"taskkill /PID {self.pid} /F"
                print(f"[ {current_time()} ] [ {self.name} ] Executing {cmd}")
                subprocess.Popen(cmd)
                self.print("Shutdown the emulator, waiting for 15seconds")
                sleep(15)

            if self.data.get(first).get("loop_task"):
                # ttw1, ttw2 = self.data.get(first).get("time_to_wait_loop1", 60), self.data.get(first).get(
                #     "time_to_wait_loop2", 90)
                ttw1 = self.data.get(first).get("time_to_wait_loop1", 60)
                ttw2 = self.data.get(first).get("time_to_wait_loop2", 90)
                # self.print("")
                self.print(
                    f"Run nb°{i} took {(time() - loop_time) / 60:0.1f} minutes to complete."
                )
                if ttw1 > ttw2:
                    ttw1, ttw2 = ttw2, ttw1
                time_before_redo_tasks = int(randint(ttw1, ttw2) * 60) + randint(0, 60)
                # self.print("")
                self.print(
                    f"Script is paused for {time_before_redo_tasks / 60:0.1f} minutes"
                )
                # self.set_status((datetime.fromtimestamp(time_before_redo_tasks) - timedelta(hours=1)).strftime("%H:%M:%S"))
                self.set_timer(time_before_redo_tasks)
                # if self.data.get(first).get("leave_game_loop", False):
                #     if time_before_redo_tasks < 600:
                #         self.leave_game(force=True)
                #     else:
                #         self.leave_game(force=False)

    @get_name
    def run_update(self):
        # self.start_emulator()
        print("starting")
        self.DEV = True
        self.adb.connect_to_device()
        self.data = self.update_data()
        loop_task = 1 if not self.data.get(self.sel).get("loop_task") else 9999999999999
        starting_time = time()
        for i in range(loop_task):
            loop_time = time()
            self.set_status("Starting..")
            self.print("Script is starting ! ".center(20, "-"), "green")
            self.data = self.update_data()

            for profile in self.data[self.sel]["schedules"]:
                if self.data[self.sel]["schedules"][profile]["enabled"]:
                    if self.data[self.sel]["schedules"][profile]["enable_timing"]:
                        can_go = False
                        when_go = 0
                        for t in self.data[self.sel]["schedules"][profile]["timing"]:
                            if is_in_frametime(t[0], t[1]):
                                can_go = True
                                when_go = random_time_in_frametime(t[0], t[1])
                                print(f"{when_go=}")
                                self.print(f"Profile {profile} able to run")
                                break
                        if not can_go:
                            print(f"The current time does not match the rules you set")
                            sleep(5)
                            continue
                        if when_go:
                            self.print(
                                "In order to mimic a player, the bot will wait a random time"
                            )
                            self.set_timer(randint(0, 60 * 10))
                            self.set_status("Starting..")
                    else:
                        print(f"Profile {profile} no rules set")
                    print(f"Profile {profile} enabled")
                    self.current_profile = profile
                    self.print(f"Profile n°{profile} enabled ! ", "blue")

                    if (
                        self.data.get(self.sel)
                        .get("schedules")
                        .get(self.current_profile)
                        .get("switch_character")
                    ):
                        self.print(f"Character n°1", "blue")
                    # First character
                    tasks = self.get_available_task(profile)
                    self.execute_tasks(tasks, profile)
                    # self.zoom_out_city()
                    if (
                        self.data.get(self.sel)
                        .get("schedules")
                        .get(self.current_profile)
                        .get("switch_character", False)
                    ):
                        co_first = self.switch_character()
                        if (
                            self.data.get(self.sel)
                            .get("schedules")
                            .get(self.current_profile)
                            .get("leave_game_switch_character", False)
                        ):
                            self.leave_game()
                        self.wait_until_connected()
                        # Characters remaining
                        boolean = True
                        nb_characters = 2
                        while boolean:
                            self.print(f"Character n°{nb_characters}", "blue")
                            nb_characters += 1
                            tasks = self.get_available_task(profile)
                            self.execute_tasks(tasks, profile)
                            self.better_sleep((1.2, 4))

                            boolean = self.switch_character(co_first, nb_characters)
                            if (
                                self.data.get(self.sel)
                                .get("schedules")
                                .get(self.current_profile)
                                .get("leave_game_switch_character", False)
                            ):
                                self.leave_game()
                            self.wait_until_connected()
                    if not self.data[self.sel]["scheduler"]:
                        break

            if self.data.get(self.sel).get("loop_task"):
                ttw1 = self.data.get(self.sel).get("time_to_wait_loop1", 60)
                ttw2 = self.data.get(self.sel).get("time_to_wait_loop2", 90)

                self.print(
                    f"Run nb°{i} took {timedelta(seconds=int(time() - loop_time))} to complete."
                )

                if ttw1 > ttw2:
                    ttw1, ttw2 = ttw2, ttw1
                time_before_redo_tasks = int(randint(ttw1, ttw2) * 60) + randint(0, 60)

                self.print(
                    f"Script is paused for {timedelta(seconds=int(time_before_redo_tasks))}",
                    "#f5b400",
                )

                if self.data.get(self.sel).get("leave_game_loop", False):
                    self.leave_game(force=False)

                self.set_timer(time_before_redo_tasks)

        self.print(
            f"The bot took {timedelta(seconds=int(time() - starting_time))} minutes to complete all the tasks, bot is waiting for your instructions.",
            "green",
        )
        self.set_divider()
        return
