import subprocess
import traceback
from datetime import timedelta
from random import choice, randint, shuffle, uniform
from time import sleep, time

import flet as ft
import win32gui
from PIL import Image

from Task_alliance_build import AllianceBuilding
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
from tasks.Task_gather_gem_map import GatherGemMap
from tasks.Task_gather_rss_default import GatherRssDefault
from tasks.Task_gather_rss_zoom import GatherRssZoom
from tasks.Task_heal_troop import HealTroop
from tasks.Task_hunt_barbarians import HuntBarbarians
from tasks.Task_maraudeurs import Marauders
from tasks.Task_produce_materials import ProduceMaterials
from tasks.Task_rss_transfert import RssTransfer
from tasks.Task_training import TroopTraining
from tasks.Task_upgrade_city import UpgradeCity
from utils.android_debug_bridge import DeviceNotFoundException
from utils.android_debug_bridge_bluestacks import AdbBluestacks
from utils.android_debug_bridge_ld_player import AdbLd
from utils.functions import (current_time, get_dic_instances,
                             get_dic_instances_ld, get_name, get_window_pid)
from utils.singletons import EmulatorSingleton
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
        self.close_windows()
        screen = self.adb.get_cv2_img()

        co = self.find_img(target="hide_quests", source=screen[:300, :300])

        if co is not None:
            self.click(co[0] + uniform(0, 20), co[1] + uniform(0, 20))

        current_task = 1
        self.debug(self.adb.resource_amount_image_to_string())
        self.check_captcha()

        for func in lib_tasks:
            self.print(f"Task {current_task}/{len(lib_tasks)}", "blue")
            self.print(
                f"Currently executing : {self.get_current_task(func.task_name())}",
                "blue",
            )

            if not self.adb.is_game_alive():
                self.run_game()

            screen = self.check_reconnect()
            screen = self.check_mge(screen)
            screen = self.check_download_page(screen)
            screen = self.leave_kd_buff(screen)
            self.check_log_back(screen)
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
                "AcademyResearch",
            ]:
                self.go_city()
            try:
                if func.task_name() in ["GatherRss", "GatherGem"]:
                    if self.find_img(target="block_icon", confidence=0.90, source=screen):
                        self.print("Bot detected that you got restricted", "red")
                        continue
                if func.task_name() in ["GatherRss", "GatherGem"]:
                    self.check_captcha()

                func.random_interaction = self.random_interaction
                func.run()

                if func.task_name() in ["GatherRss", "GatherGem"]:
                    self.check_captcha()
            except Exception as e:
                traceback.print_exc()
                self.send_discord_message(f"Something wrong happened when running {func.task_name()}")
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
        self.check_captcha()

    def get_available_task(self, profile: str = None):
        # self.data = self.update_data()
        if profile is None:
            profile = self.data.get(self.sel)
        else:
            profile = self.data.get(self.sel).get("schedules").get(profile)
        # print(profile)
        lib_tasks = []

        gem_task = {
            "default": GatherGemDefault,
            "spiral": GatherGemSpiral,
            "map": GatherGemMap
        }

        rss_task = {
            "default": GatherRssDefault,
            "zoom": GatherRssZoom
        }

        tasks = [
            ("claim_campaign", ClaimCampaign),
            ("collect_ressource", CollectResource),
            ("buy_merchant", BuyMerchant),
            (
                "gather_rss",
                rss_task[profile.get("gather_rss_method")],
            ),
            ("use_enhanced_buff", UseEnhancedBuff),
            ("check_donation", AllianceDonation),
            ("defeat_barbarians", HuntBarbarians),
            (
                "gather_gem",
                gem_task[profile.get("gather_gem_method")],
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

        for task_key, task_class in tasks:
            if profile.get(task_key, False):
                if task_key == "gather_rss":
                    if profile["gather_rss_availability"] == "all":
                        lib_tasks.append(task_class(self))
                    elif profile["gather_rss_availability"] == "only_first" and self.character_index == 1:
                        lib_tasks.append(task_class(self))
                    elif profile["gather_rss_availability"] == "all_except_first" and self.character_index != 1:
                        lib_tasks.append(task_class(self))
                elif task_key == "gather_gem":
                    if profile["gather_gem_availability"] == "all":
                        lib_tasks.append(task_class(self))
                    elif profile["gather_gem_availability"] == "only_first" and self.character_index == 1:
                        lib_tasks.append(task_class(self))
                    elif profile["gather_gem_availability"] == "all_except_first" and self.character_index != 1:
                        lib_tasks.append(task_class(self))
                else:
                    lib_tasks.append(task_class(self))

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

        if profile.get("claim_mails", False):
            lib_tasks.append(ClaimMail(self))

        if profile.get("help_alliance_building", False):
            lib_tasks.insert(0, AllianceBuilding(self))

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
    def switch_character(self, co_first=None, nb_chars=0, fail=0) -> tuple[float, float] or bool:
        self.print("Switching to the next character", color=ft.colors.PURPLE)
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

        if self.find_img("star") is None:
            self.click(uniform(600, 900), uniform(170, 177))
            self.better_sleep((1.925, 2.795))

        stop = 0
        while Image.fromarray(self.adb.get_cv2_img()).getpixel((344, 326)) == first_color:
            self.better_sleep((2, 3))
            stop += 1

            if stop == 10:
                self.print("It seems the game is unable to load the characters menu..", ft.colors.RED_300)
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

            self.print("Looking for the current character")

            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)

            self.swipe(x, y, x2, y2)
            self.better_sleep((1.925, 2.795))

            trigger_stop += 1
            if trigger_stop == 4:
                self.close_windows()
                self.close_upgrade_popup()
                self.check_captcha()
                self.print("Cannot locate the current user, trying to restart the task", ft.colors.RED_300)
                return self.switch_character(co_first, nb_chars, fail + 1)

            if fail > 2:
                self.print("Cannot switch to the next character. Bot is now stopped", ft.colors.RED)
                self.set_status("Error.")
                self.send_discord_message("Cannot switch to the next character, your action is required.")
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
            self.send_discord_message(
                "Unable to find more characters, the current character is maybe the last favorite or there's simply no favorite characters"
            )
            self.close_windows()
            return False
        else:
            self.print("No more characters, going back to the first character")
            x, y = uniform(400, 800), uniform(250, 260)
            if nb_chars // 6 == 0:
                rounds = 1
            else:
                rounds = nb_chars // 6
            if rounds == 0:
                rounds = +1
            for _ in range(rounds):
                x2, y2 = x + uniform(-20,20), uniform(580, 645)
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
        all_prefered_characters = self.adb.find_multiple_img(source=screen, target="star")
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

            cords = cleaned_next_characters[0] + uniform(-100, -50), cleaned_next_characters[1] + uniform(-5, 5)
            self.click(cords[0], cords[1])
            return cords[0], cords[1]
        return False

    @get_name
    def change_character_param(self, co_first, nb_chars=0, fail=0):
        self.print("Switching to the next character", color=ft.colors.PURPLE)
        self.set_status(f"Switching Character")
        self.close_windows()
        self.enter_profile()
        self.better_sleep((1.925, 2.795))
        self.enter_setting()
        self.better_sleep((1.925, 2.795))
        first_color = Image.fromarray(self.adb.get_cv2_img()).getpixel((344, 326))
        self.enter_characters()
        self.better_sleep((0.925, 1.795))

        stop = 0

        while Image.fromarray(self.adb.get_cv2_img()).getpixel((344, 326)) == first_color:
            self.better_sleep((1, 2))
            stop += 1

            if stop == 10:
                self.print("It seems the game is unable to load the characters menu..", ft.colors.RED_300)
                return self.change_character_param(self, co_first, nb_chars, fail)

        self.better_sleep((1.925, 2.795))
        trigger_stop = 0

        while self.find_img(target="logged_icon", confidence=0.7) is None:
            self.check_captcha()
            self.check_captcha_slider()

            self.print("Looking for the current character")

            y, x = uniform(290, 480), uniform(460, 560)
            x2, y2 = x + uniform(-30, 30), y + uniform(-100, -50)

            self.swipe(x, y, x2, y2)
            self.better_sleep((1.925, 2.795))

            trigger_stop += 1
            if trigger_stop == 4:
                self.close_windows()
                self.close_upgrade_popup()
                self.check_captcha()
                self.print("Cannot locate the current user, trying to restart the task", ft.colors.RED_300)
                return self.change_character_param(co_first, nb_chars, fail + 1)

            if fail > 2:
                self.print("Cannot switch to the next character. Bot is now stopped", ft.colors.RED)
                self.set_status("Error.")
                self.send_discord_message("Cannot switch to the next character, your action is required.")
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
    def start_emulator(self, emulator: str, deadstop=0):
        if deadstop == 3:
            self.print("Cannot start the emulator", ft.colors.RED)
            self.send_discord_message("Cannot start the emulator", image=False)
            while True:
                self.better_sleep((1, 1))

        self.FileSingleton.get_path()
        data = self.FileSingleton.get_data()
        emulator_choice = EmulatorSingleton().getEmulator()

        if not win32gui.FindWindow(None, self.name):
            print(f"Bot will wait until the device is properly booted.")
            self.set_status("Booting")
            EmulatorSingleton().startEmulator(emulator)
            try:
                self.adb.wait_boot_complete(timeout=120, timedelta=10)

                sleep(10)

                self.adb.shell("echo boot completed")
                self.debug("Boot completed")
            except (TimeoutError, DeviceNotFoundException, Exception) as e:
                self.debug("Timed out waiting for boot")
                self.debug(e)
                self.adb.print("Timed out waiting for boot")
                self.adb.print(str(e))
                self.kill_instance()
                sleep(1)
                return self.start_emulator(emulator, deadstop + 1)

        if emulator_choice == "ld":
            instances = get_dic_instances_ld()
        else:
            instances = get_dic_instances()

        for instance in instances:
            data[str(instance)]["instance"] = instances[str(instance)]["instance"]
            data[str(instance)]["name"] = instances[str(instance)]["name"]
            data[str(instance)]["port"] = int(instances[str(instance)]["port"])

        self.data = data
        self.FileSingleton.write_data(data)
        # self.worker.main_task.adb.connect_to_device()
        # self.worker.runner.adb.connect_to_device()

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
                    ft.colors.RED,
                )
                self.generate_toast(
                    "Warning ",
                    "No active profiles found! Navigate to the profile settings and enable at least one option.",
                    ft.icons.INFO,
                    ft.colors.YELLOW_800,
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
                            self.print("In order to mimic a player, the bot will wait a random time")
                            self.set_timer(randint(0, 60 * 10))
                            self.set_status("Starting..")
                    else:
                        print(f"Profile {profile} no rules set")
                    self.current_profile = profile
                    self.print(f"Profile n°{profile} enabled ! ", "blue")

                    if self.get_config().get("switch_character"):
                        self.print(f"Character n°1", ft.colors.CYAN_ACCENT_700)
                    # First character
                    self.execute_tasks(self.get_available_task(profile), profile)

                    if self.get_config().get("switch_character", False):
                        self.check_captcha()
                        co_first = self.switch_character()
                        self.wait_until_connected()
                        # Characters remaining
                        boolean = True
                        self.character_index = 2
                        while co_first and boolean:
                            self.print(f"Character n°{self.character_index}", ft.colors.CYAN_ACCENT_700)
                            self.character_index += 1
                            self.execute_tasks(self.get_available_task(profile), profile)
                            self.better_sleep((1.2, 4))

                            self.check_captcha()
                            boolean = self.switch_character(co_first, self.character_index, 0)
                            self.wait_until_connected()
                    if not self.data[self.sel]["scheduler"]:
                        break

            if self.data.get(self.sel).get("loop_task"):
                ttw1 = self.data.get(self.sel).get("time_to_wait_loop1", 60)
                ttw2 = self.data.get(self.sel).get("time_to_wait_loop2", 90)

                self.print(f"Run nb°{i} took {timedelta(seconds=int(time() - loop_time))} to complete.")
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
    def run_groups(self):
        pass
        #     thread.start()
        #
        # for thread in threads:
        #     thread.join()

    @get_name
    def run3(self, tiles=None):
        if tiles is None:
            tiles = self.tile.get_enabled_sel_object()

        if not tiles:
            self.generate_toast("Warning", "No emulator selected!", ft.colors.AMBER)
            return

        emulator = EmulatorSingleton().getEmulator()

        self.set_sel(tiles[0].number)
        self.data = self.update_data()
        loop_task = 1 if not self.data.get(self.sel).get("loop_task") else 9999999999999
        loop_time = time()

        for i in range(loop_task):
            loop_time = time()
            first = tiles[0].number
            nb_tile = 0
            for enabled_tile in tiles:
                enabled_tile.set_text(f"In queue ({nb_tile})")
                nb_tile += 1

            for enabled_tile in tiles:
                starting_time = time()

                self.tile = enabled_tile
                self.set_sel(self.tile.number)

                if self.data[self.sel]["schedules"]["1"]["enable_timing"]:
                    can_go = False
                    for t in self.data[self.sel]["schedules"]["1"]["timing"]:
                        if is_in_frametime(t[0], t[1]):
                            self.print(f"Profile 1 able to run")
                            can_go = True
                            break
                    if not can_go:
                        print(f"The current time does not match the rules you set")
                        continue

                if emulator == "bluestacks":
                    self.adb = AdbBluestacks(self.tile.number)
                else:
                    self.adb = AdbLd(self.tile.number)

                self.start_emulator(self.tile.number)
                self.tile.runner = self
                self.set_status("Starting..")
                self.print("Changing adb..")
                self.print(f"{self.adb.number = } {self.adb.port =}")

                self.adb.__repr__()
                self.print("Connecting to the emulator..")
                self.adb.connect_to_device()

                # First character
                self.current_profile = "1"
                self.print("Reminder : only the first profile is available")
                if self.get_config().get("switch_character"):
                    self.print(f"Character n°1", ft.colors.CYAN_ACCENT_700)
                # First character
                self.execute_tasks(self.get_available_task(self.current_profile), self.current_profile)

                if self.get_config().get("switch_character", False):
                    self.check_captcha()
                    co_first = self.switch_character()
                    self.wait_until_connected()
                    # Characters remaining
                    boolean = True
                    self.character_index = 2
                    while co_first and boolean:
                        self.print(f"Character n°{self.character_index}", ft.colors.CYAN_ACCENT_700)
                        self.character_index += 1
                        self.execute_tasks(
                            self.get_available_task(self.current_profile),
                            self.current_profile,
                        )
                        self.better_sleep((2.2, 4))

                        self.check_captcha()
                        boolean = self.switch_character(co_first, self.character_index, 0)
                        self.wait_until_connected()

                self.set_status("")
                self.leave_game()
                self.kill_instance()
                self.print("Shutdown the emulator, waiting for 15seconds")
                self.set_timer(15)

                self.print(
                    f"The bot took {timedelta(seconds=int(time() - starting_time))} to complete all the tasks on this emulator.",
                    "green",
                )

            if self.data.get(first).get("loop_task"):
                # ttw1, ttw2 = self.data.get(first).get("time_to_wait_loop1", 60), self.data.get(first).get(
                #     "time_to_wait_loop2", 90)
                ttw1 = self.data.get(first).get("time_to_wait_loop1", 60)
                ttw2 = self.data.get(first).get("time_to_wait_loop2", 90)
                # self.print("")
                self.print(f"Run nb°{i} took {(time() - loop_time) / 60:0.1f} minutes to complete.")
                if ttw1 > ttw2:
                    ttw1, ttw2 = ttw2, ttw1
                time_before_redo_tasks = int(randint(ttw1, ttw2) * 60) + randint(0, 60)
                # self.print("")
                self.tile = tiles[0]

                self.print(f"Script is paused for {time_before_redo_tasks / 60:0.1f} minutes")
                # self.set_status((datetime.fromtimestamp(time_before_redo_tasks) - timedelta(hours=1)).strftime("%H:%M:%S"))
                nb_tile = 0
                for enabled_tile in tiles:
                    enabled_tile.set_text(f"In queue ({nb_tile})")
                    nb_tile += 1

                self.set_timer(time_before_redo_tasks)
                # if self.data.get(first).get("leave_game_loop", False):
                #     if time_before_redo_tasks < 600:
                #         self.leave_game(force=True)
                #     else:
                #         self.leave_game(force=False)

    def set_status(self, text):
        super().set_status(text)
        if hasattr(self, "worker"):
            self.worker.set_text(text)

    @get_name
    def run4(self, tiles=None):
        if not tiles:
            self.generate_toast("Warning", "No emulator selected!", ft.colors.AMBER)
            return

        emulator = EmulatorSingleton().getEmulator()
        self.data = self.update_data()
        loop_task = 1 if not self.data["workers"][emulator][self.worker.number]["loop_task"] else 9999999

        for i in range(loop_task):
            cycle_started_at = time()
            nb_tile = 0
            for enabled_tile in tiles:
                enabled_tile.set_text(f"In queue ({nb_tile})")
                nb_tile += 1

            for enabled_tile in tiles:
                emulator_started_at = time()

                self.tile = enabled_tile
                self.character_index = 1
                self.set_sel(self.tile.number)
                can_go = True
                for profile in self.data[self.sel]["schedules"]:
                    can_go = False

                    if not self.data[self.sel]["schedules"][profile]["enabled"]:
                        continue
                    else:
                        if self.data[self.sel]["schedules"][profile]["enable_timing"]:
                            for t in self.data[self.sel]["schedules"][profile]["timing"]:
                                if is_in_frametime(t[0], t[1]):
                                    self.print(f"Profile 1 able to run")
                                    can_go = True
                                    break
                            if not can_go:
                                print(f"The current time does not match the rules you set")
                                continue

                    if emulator == "bluestacks":
                        self.adb = AdbBluestacks(self.tile.number, task_reference=self)
                    else:
                        self.adb = AdbLd(self.tile.number, task_reference=self)

                    self.start_emulator(self.tile.number)
                    self.tile.runner = self
                    self.set_status("Starting..")
                    
                    # First character
                    self.current_profile = profile

                    if self.get_config().get("switch_character"):
                        self.print(f"Character n°1", ft.colors.CYAN_ACCENT_700)
                    # First character
                    self.execute_tasks(self.get_available_task(self.current_profile), self.current_profile)

                    if self.get_config().get("switch_character", False):
                        self.check_captcha()
                        co_first = self.switch_character()
                        self.wait_until_connected()
                        # Characters remaining
                        boolean = True
                        self.character_index = 2
                        while co_first and boolean:
                            self.print(f"Character n°{self.character_index}", ft.colors.CYAN_ACCENT_700)
                            self.character_index += 1
                            self.execute_tasks(
                                self.get_available_task(self.current_profile),
                                self.current_profile,
                            )
                            self.better_sleep((2.2, 4))

                            self.check_captcha()
                            boolean = self.switch_character(co_first, self.character_index, 0)
                            self.wait_until_connected()

                self.set_status("")

                if not can_go:
                    self.leave_game()

                if self.data["workers"][emulator][self.worker.number]["close_emulator"]:
                    self.kill_instance()
                    self.print("Shutdown the emulator, waiting for 5 seconds")
                    self.better_sleep((5, 5))

                self.print(
                    f"The bot took {timedelta(seconds=int(time() - emulator_started_at))} to complete all the tasks on this emulator.",
                    "green",
                )



            if self.data["workers"][emulator][self.worker.number]["loop_task"]:
                waiting_cooldown = self.data["workers"][emulator][self.worker.number]["waiting_cooldown"]
                waiting_cooldown.sort()
                t1, t2 = waiting_cooldown
                time_before_redo_tasks = int(randint(t1, t2) * 60) + randint(0, 60)
                # self.print("")

                # self.print(f"Script is paused for {time_before_redo_tasks / 60:0.1f} minutes")

                for i, enabled_tile in enumerate(tiles):
                    enabled_tile.add_text(f"Run nb°{i} took {(time() - cycle_started_at) / 60:0.1f} minutes to complete.")
                    enabled_tile.set_text(f"In queue ({i})")

                self.tile = self.worker
                self.set_timer(time_before_redo_tasks)

    def kill_instance(self):
        self.pid = get_window_pid(self.adb.name)
        cmd = f"taskkill /PID {self.pid} /F"
        print(f"[ {current_time()} ] [ {self.name} ] Executing {cmd}")
        subprocess.Popen(cmd)


    def open_chat_and_leave(self):
        self.click(147, 680)
        self.better_sleep((4, 7))

    def open_random_rss_type(self):
        cords = []

        cords.append([715, 12])
        cords.append([850, 12])
        cords.append([970, 12])
        cords.append([1100, 12])

        cord = choice(cords)

        self.click(cord[0], cord[1])
        self.better_sleep((1.3, 4))

    def open_any_rankings(self):
        self.enter_profile()
        self.better_sleep((2, 5))
        self.click(400 + uniform(-10, 10), 600 + uniform(-10, 10))
        self.better_sleep((2, 5))

        cords = [[326, 212], [660, 212], [980, 212], [326, 420], [660, 420], [980, 420], [326, 600], [660, 600], [980, 600]]

        cord = choice(cords)

        self.click(cord[0], cord[1])
        self.better_sleep((4, 9))

    @get_name
    def random_interaction(self, zoomed_in=False):
        tasks = self.get_available_task(self.current_profile)


        def open_menu_and_go_canyon():
            self.open_menu()
            self.open_campaign()
            self.open_sunset_canyon()

        def open_inventory_and_go_in_any_tab():
            self.open_menu()
            self.open_inventory()
            self.open_any_inventory_tab()

        def open_commander_list_and_click_on_heros():
            self.open_menu()
            self.open_commander_tab()
            self.click_any_commander_in_list()

        interactions = [self.open_chat_and_leave, self.enter_profile, self.open_any_rankings, open_menu_and_go_canyon, open_inventory_and_go_in_any_tab, open_commander_list_and_click_on_heros]

        if zoomed_in:
            interactions.append(self.open_random_rss_type)

            if any(isinstance(task, AllianceDonation) for task in tasks):
                interactions.append(AllianceDonation(self).run)

        if any(isinstance(task, ClaimMail) for task in tasks):
            interactions.append(ClaimMail(self).run)

        func = choice(interactions)

        func()
        self.better_sleep((1.2, 2.7))
        self.close_windows()

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
                            self.print("In order to mimic a player, the bot will wait a random time")
                            self.set_timer(randint(0, 60 * 10))
                            self.set_status("Starting..")
                    else:
                        print(f"Profile {profile} no rules set")
                    print(f"Profile {profile} enabled")
                    self.current_profile = profile
                    self.print(f"Profile n°{profile} enabled ! ", "blue")

                    if self.data.get(self.sel).get("schedules").get(self.current_profile).get("switch_character"):
                        self.print(f"Character n°1", "blue")
                    # First character
                    tasks = self.get_available_task(profile)
                    self.execute_tasks(tasks, profile)
                    # self.zoom_out_city()
                    if self.data.get(self.sel).get("schedules").get(self.current_profile).get("switch_character", False):
                        co_first = self.switch_character()
                        if self.data.get(self.sel).get("schedules").get(self.current_profile).get("leave_game_switch_character", False):
                            self.leave_game()
                        self.wait_until_connected()
                        # Characters remaining
                        boolean = True
                        self.character_index = 2
                        while boolean:
                            self.print(f"Character n°{self.character_index}", "blue")
                            self.character_index += 1
                            tasks = self.get_available_task(profile)
                            self.execute_tasks(tasks, profile)
                            self.better_sleep((1.2, 4))

                            boolean = self.switch_character(co_first, self.character_index)
                            if self.data.get(self.sel).get("schedules").get(self.current_profile).get("leave_game_switch_character", False):
                                self.leave_game()
                            self.wait_until_connected()
                    if not self.data[self.sel]["scheduler"]:
                        break

            if self.data.get(self.sel).get("loop_task"):
                ttw1 = self.data.get(self.sel).get("time_to_wait_loop1", 60)
                ttw2 = self.data.get(self.sel).get("time_to_wait_loop2", 90)

                self.print(f"Run nb°{i} took {timedelta(seconds=int(time() - loop_time))} to complete.")

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
