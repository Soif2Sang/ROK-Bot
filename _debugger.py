import datetime
import json
from random import randint, uniform
from threading import Thread
from time import time

import cv2
import flet as ft
import numpy as np
import win32api
import win32con
import win32gui
from android_debug_bridge import Adb
from MTM import matchTemplates
from twocaptcha import TwoCaptcha

import taskscod.COD_Task_daily_vip

# from tasks.Task_title import Title
from tasks import Task_gather_rss_default

# from taskscod import COD_Task_alliance_donation, COD_Task_training, COD_Task_clear_fog
# from taskscod.COD_Task_daily_chest import DailyChest
# from taskscod.COD_Task_gather_rss import GatherRss
from tasks.Task import Task
from tasks.Task_academy_research import AcademyResearch
from tasks.Task_alliance_donation import AllianceDonation
from tasks.Task_alliance_pit import AlliancePit
from tasks.Task_buy_merchant import BuyMerchant
from tasks.Task_claim_daily_quests import DailyQuests
from tasks.Task_claim_mail import ClaimMail
from tasks.Task_daily_chest2 import DailyChest2
from tasks.Task_daily_vip import DailyVip
from tasks.Task_gather_gem_default import GatherGem
from tasks.Task_gather_rss_default import GatherRss
from tasks.Task_hunt_barbarians import HuntBarbarians
from tasks.Task_kingdom_ranking import KingdomRanking
from tasks.Task_maraudeurs import Marauders
from tasks.Task_rss_transfert import RssTransfer
from tasks.Task_runner import TaskRunner
from tasks.Task_training import TroopTraining
from tasks.Task_upgrade_city import UpgradeCity
from utils.android_debug_bridge_ld_player import *

# from utils.android_debug_bridge import *
DEBUG = True

# from rkp import *
# from auto_upgrade import *
file = FileSingleton()

data = file.get_data()
# with open('rkp_list.json') as config_file: data_rkp = json.load(config_file)


class Page:
    def __init__(self):
        self.UPGRADE = False


class Frame:
    def __init__(self, sel):
        self.started = True
        self.stopped = False
        self.paused = False
        self.number = sel
        self.initial_page = Page()

    def add_text(self, phrase, color="black"):
        print(phrase)

    def set_text(self, phrase, color="black"):
        print(phrase)

    def get_text(self):
        return ""

    def add_status(self, phrase, color="black"):
        return


class Bot:
    def __init__(self, adb):
        self.adb: Adb = adb
        self.device = adb.get_device()
        self.main_task = Task(Frame(adb.number))  # tasksGEM / tasks
        self.main_task.adb = adb
        # self.task = Tasks(self.adb)
        self.main_task.set_sel(str(adb.number))
        self.task = TaskRunner(self.main_task, self.main_task.tile)
        self.upgrade = UpgradeCity(self.main_task)
        self.merchant = BuyMerchant(self.main_task)
        self.rss = GatherRss(self.main_task)
        # self.rss2  =  GatherRss2(self.main_task)
        self.AlliancePit = AlliancePit(self.main_task)
        self.research = AcademyResearch(self.main_task)
        self.quests = DailyQuests(self.main_task)
        self.vip = DailyVip(self.main_task)
        self.chest = DailyChest2(self.main_task)
        self.alliance = AllianceDonation(self.main_task)
        self.trade = RssTransfer(self.main_task)
        self.cod_rss = GatherRss(self.main_task)
        self.ranks = KingdomRanking(self.main_task)
        self.mails = ClaimMail(self.main_task)
        from tasks.Task_alliance_help import AllianceHelp

        self.help = AllianceHelp(self.main_task)
        self.training = TroopTraining(self.main_task)
        self.hunt = HuntBarbarians(self.main_task)
        # self.cod_vip = taskscod.COD_Task_daily_vip.DailyVip(self.main_task)
        # self.cod_chest = DailyChest(self.main_task)
        # self.code_alliance = COD_Task_alliance_donation.AllianceDonation(self.main_task)
        # self.code_training = COD_Task_training.TroopTraining(self.main_task)
        # self.cod_scout = COD_Task_clear_fog.ClearFog(self.main_task)
        self.maraudeurs = Marauders(self.main_task)
        self.gem = GatherGem(self.main_task)
        # self.title = Title(self.main_task)
        # self.rkp = Rkp(self.adb)
        # self.rkp.set_sel('4')
        # self.up = Up(self.adb)
        # self.rkp.set_sel('3')


def create_instance(number: int, master):
    adb = Adb(number)
    bot = Bot(adb)
    bot.adb.connect_to_device()
    bot.task.set_status = lambda text, color=None: print(
        f"[ {bot.task.name} ] Status = {text}"
    )
    bot.task.print = lambda text, color=None: print(f"[ {bot.task.name} ] {text}")
    bot.task.current_profile = "1"
    frame = object()
    frame.pr_tasks_button = object()
    frame.end_tasks_button = object()
    frame.pause = False
    frame.stop = False
    bot.task.frame = frame
    # bot.task.setup_view()
    # bot.task.better_sleep((0.9, 1.2))
    return bot


class FakeText:
    def __init__(self):
        self.value = ""

    def update(self):
        return


class lightTile:
    def ___init__(self, **kwargs):
        super().__init__(**kwargs)

        with open("user_settings.json") as config_file:
            data = json.load(config_file)

        self.started = True
        self.stopped = False
        self.text_status = FakeText()


def get_bot(number):
    adb = Adb(number)
    bot = Bot(adb)
    bot.adb.connect_to_device()

    bot.adb.pause = False
    bot.main_task.print = lambda txt: print(txt)
    bot.main_task.set_text = lambda txt: print(txt)
    bot.main_task.status = lambda txt: print(txt)
    bot.main_task.script_pause = lambda: print("")

    bot.task.current_profile = "1"
    # Page = customtkinter.CTk()
    frame = Frame(number)
    frame.number = number
    frame.stopped = False
    frame.started = True
    frame.paused = False
    frame.add_text = lambda x, _: print(x)
    frame.set_text = lambda x, _: print(x)

    bot.task.tile = frame
    bot.task.tile.stopped = False
    return bot


def perf(function):
    start = time()
    a = function()
    print(f"It took {time() - start}")
    return a


if __name__ == "__main__":
    # upgrade_all()

    # print(TwoCaptcha("9c5059a65dd40980bd2fc113f616060e").balance())

    bot = get_bot("Nougat64_13")
    # bot.task.zoom_out_city()
    bot.research.run()
    exit()

    hwnd = win32gui.FindWindow(None, bot.task.adb.name)
    print(bot.task.adb.name)
    hwndChild = win32gui.GetWindow(hwnd, win32con.GW_CHILD)

    # print(hwnd ,hwndChild)
    bot.task.script_pause()
    bot.task.script_pause()
    win32gui.SendMessage(hwndChild, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
    win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, win32con.VK_F6, 0)
    bot.task.better_sleep((0.45, 0.45))
    win32gui.SendMessage(hwndChild, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
    win32api.PostMessage(hwndChild, win32con.WM_KEYUP, win32con.VK_F6, 0)
    bot.task.better_sleep((1.4, 2))
    bot.task.script_pause()
    win32gui.SendMessage(hwndChild, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
    win32api.PostMessage(hwndChild, win32con.WM_KEYDOWN, win32con.VK_F6, 0)
    bot.task.better_sleep((0.17, 0.17))
    win32gui.SendMessage(hwndChild, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)
    win32api.PostMessage(hwndChild, win32con.WM_KEYUP, win32con.VK_F6, 0)
    bot.task.better_sleep((1.4, 2))

    exit()
    icons = []
    for i in range(14):
        icons.append((f"GemDeposit{i}", bot.adb.images.get_file_name(f"GemDeposit{i}")))
    total = 0
    for icon in icons:
        # co = self.validate_co(
        #     self.find_img(source=screen, target=icon[0], confidence=0.77))
        # if co is None:
        #     co = self.validate_co(
        #         self.find_img(source=screen, target=icon[1], confidence=0.77))
        screen = bot.adb.get_cv2_img()
        start = time()

        bot.task.find_img(source=screen, target=icon[0], confidence=0.795)
        print(f"It took {time() - start}")
        total += start

    print(f"It took {total}")
    start = time()

    matchTemplates(listTemplates=icons, image=screen, score_threshold=0.795)
    print(f"It took {time() - start}")

    exit()
    print(bot.task.find_img("building_speedups", confidence=0.7))
    exit()
    techs = bot.task.adb.find_multiple_img(target="research_tech", confidence=0.7)
    cards = bot.task.adb.find_multiple_img(target="research_card", confidence=0.9)
    print(techs)
    print(cards)
    duos = set()
    for card in cards:
        for tech in techs:
            if (tech[1] > card[1] and tech[1] < card[1] + 100) and (
                tech[0] > card[0] - 150 and tech[0] < card[0]
            ):
                duos.add(card)
    print(duos)
    exit()
