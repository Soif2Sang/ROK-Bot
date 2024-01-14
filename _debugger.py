import datetime
import json
import subprocess
from random import randint, uniform
from threading import Thread
from time import time

import cv2
import flet as ft
import numpy as np
import win32api
import win32con
import win32gui
from MTM import matchTemplates

from Task_claim_campaign import ClaimCampaign
from android_debug_bridge_bluestacks import AdbBluestacks
from auth import selfApi
from constants import BREZILIAN
from functions import getchecksum, increment_captcha_requests
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
from tasks.Task_gather_rss_default import GatherRss, GatherRssDefault
from tasks.Task_hunt_barbarians import HuntBarbarians
from tasks.Task_kingdom_ranking import KingdomRanking
from tasks.Task_maraudeurs import Marauders
from tasks.Task_rss_transfert import RssTransfer
from tasks.Task_runner import TaskRunner
from tasks.Task_training import TroopTraining
from tasks.Task_upgrade_city import UpgradeCity
from utils.android_debug_bridge_ld_player import AdbLd
from utils.singletons import FileSingleton, ApiSingleton

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
        self.adb: AdbLd = adb
        self.device = adb.get_device()
        self.main_task = Task(Frame(adb.number))  # tasksGEM / tasks
        self.main_task.adb = adb
        # self.task = Tasks(self.adb)
        self.main_task.set_sel(str(adb.number))
        self.task = TaskRunner(self.main_task, self.main_task.tile)
        self.upgrade = UpgradeCity(self.main_task)
        self.merchant = BuyMerchant(self.main_task)
        self.rss = GatherRssDefault(self.main_task)
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

        self.expedition = ClaimCampaign(self.main_task)
        self.help = AllianceHelp(self.main_task)
        self.training = TroopTraining(self.main_task)
        self.hunt = HuntBarbarians(self.main_task)
        self.runner = TaskRunner(self.main_task, self.main_task.tile)
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
    adb = AdbLd(number)
    bot = Bot(adb)
    bot.adb.connect_to_device()
    bot.task.set_status = lambda text, color=None: print(f"[ {bot.task.name} ] Status = {text}")
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
    # adb = Adb(number)
    adb = AdbLd(number)
    bot = Bot(adb)
    bot.adb.connect_to_device()

    bot.adb.pause = False
    bot.main_task.print = lambda txt: print(txt)
    bot.main_task.set_status = lambda txt: print(txt)
    bot.main_task.set_text = lambda txt, _=None: print(txt)
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
    from ppadb.client import Client as PPADBClient

    keyauthapp = selfApi(
        name="Rokbd" if not BREZILIAN else "RokbdBR",
        ownerid="7oofxdj8uH",
        secret="a968396e3fdfff2a2eaf14516fb283b7b7013e19cf392c863c90e0d8c41d9be0"
        if not BREZILIAN
        else "6d15b7ee5e7312238105efd4b648535835dc1ce5f4250fe2dc82910db43147b6",
        version="2.0",
        hash_to_check=getchecksum(),
    )

    keyauthapp.login("maxence", "fe")
    keys = json.loads(keyauthapp.var("keys"))
    print(keys)
    ApiSingleton().setApiKey(keys["2captcha"])
    ApiSingleton().setSupabasePublicKey(keys["supabase_public_key"])
    ApiSingleton().setSupabaseUrl(keys["supabase_url"])

    bot = get_bot("2")
    bot.task.solve_captcha()
    exit()
    bot.task.handle_captcha_limit("maxou")
    # print(id(bot.task.fileSingleton))
    #
    exit()
    # bot.expedition.run()
    # bot.vip.run()

    for i in range(15):
        print(bot.task.in_city())
    # self.find_img(
    #     target="checkpoint_star",
    #     source=self.adb.get_cv2_img()[:60, 380:600],
    #     confidence=0.97,
    # )
    print(bot.task.find_img(target="hammer"))
    exit()
    # adb_path = f"{path['HD-Player'].replace('Player', 'Adb')}"
    # cmd = f"{adb_path} connect 127.0.0.1-5564"
    # subprocess.Popen(cmd)
    # host, port = "127.0.0.1", 5037
    # client = PPADBClient(host="127.0.0.1", port=5037)
    # print()
    # d = client.device("emulator-5554")
    # print(d)
    # print(d.screencap())

    def check_emulator_status(emulator_id):
        path = fS.get_path()
        cmd = f"{path['LD-Console'].replace('ldconsole', 'adb')} -s {emulator_id} shell getprop sys.boot_completed"
        command = f"adb "
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        return result.stdout.strip() == "1"

    AdbLd("1", "emulator", 5556).wait_boot_complete()

    while True:
        print(check_emulator_status("emulator-5556"))
    exit()
    client = PPADBClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    start = time()
    print("Start", time() - start)
    a = AdbLd("5")
    print(a.wait_boot_complete(30, 0))
    print("boot complete", time() - start)
    # bot = get_bot("3")
    # bot.rss.run()
    # bot.alliance.run()
    # print(bot.task.in_city())
    # bot.rss.run()
    # file = cv2.imread('screenshot_test.png')
    # print(bot.task.find_img(target='checkpoint_star',source=file[:70, 200:600]))
    # bot.vip.run()
    # bot.rss.run()
    # bot.task.close_windows()
