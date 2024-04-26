import json
from random import uniform
from time import time

import cv2
from numpy import where

from Task_gather_gem_spiral import GatherGemSpiral

# from tasks.Task_title import Title
# from taskscod import COD_Task_alliance_donation, COD_Task_training, COD_Task_clear_fog
# from taskscod.COD_Task_daily_chest import DailyChest
# from taskscod.COD_Task_gather_rss import GatherRss
from tasks.Task import Task
from tasks.Task_academy_research import AcademyResearch
from tasks.Task_alliance_donation import AllianceDonation
from tasks.Task_alliance_pit import AlliancePit
from tasks.Task_buy_merchant import BuyMerchant
from tasks.Task_claim_campaign import ClaimCampaign
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
from utils.resources import ImageSingleton
from utils.singletons import FileSingleton

# from utils.android_debug_bridge import *
DEBUG = True

# from rkp import *
# from auto_upgrade import *
file = FileSingleton()

data = file.get_data()
# with open('rkp_list.json') as config_file: data_rkp = json.load(config_file)
from pytesseract import pytesseract

pytesseract.tesseract_cmd = r".\\tesseract\\tesseract.exe"

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
        self.main_task = Task(Frame(adb.instance))  # tasksGEM / tasks
        self.main_task.adb = adb
        # self.task = Tasks(self.adb)
        self.main_task.set_sel(str(adb.instance))
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
        self.gem = GatherGemSpiral(self.main_task)
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
            json.load(config_file)

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

def find_multiple_img(target, source, confidence=0.9):
    img_to_find = ImageSingleton().get_file_name(target)

    result = matchTemplate(source, img_to_find, TM_CCOEFF_NORMED)
    needle_w = img_to_find.shape[1]
    needle_h = img_to_find.shape[0]

    min_val, max_val, min_loc, max_loc = minMaxLoc(result)
    min_thresh = confidence
    # print(min_thresh>confidence)
    location = where(result >= min_thresh)
    location = list(zip(*location[::-1]))
    # print(location)

    rectangles = []
    for loc in location:
        rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
        rectangles.append(rect)
    # print(rectangles)

    localisations = []

    for i in range(len(rectangles)):
        if target == "back_icon":
            # print(file_name)
            # print(rectangles[i][0])
            # print(rectangles[i][0]+1000)
            localisations.append((rectangles[i][0] + 1000, rectangles[i][1]))
        else:
            localisations.append((rectangles[i][0], rectangles[i][1]))
    element_to_delete = []
    for i in range(len(localisations) - 1):
        if (
                (localisations[i][0] + 1 == localisations[i + 1][0])
                or (localisations[i][0] - 1 == localisations[i + 1][0])
                or (localisations[i][0] == localisations[i + 1][0])
        ) and (
                (localisations[i][1] + 1 == localisations[i + 1][1])
                or (localisations[i][1] - 1 == localisations[i + 1][1])
                or (localisations[i][1] == localisations[i + 1][1])
        ):
            element_to_delete.append(localisations[i])

    # print(element_to_delete)
    for element in element_to_delete:
        localisations.remove(element)
    return localisations


from cv2 import (COLOR_BGR2GRAY, THRESH_BINARY, THRESH_OTSU, TM_CCOEFF_NORMED,
                 bitwise_not, cvtColor, destroyAllWindows, imread, imshow,
                 matchTemplate, minMaxLoc, threshold, waitKey)

if __name__ == "__main__":


    bo = get_bot("4")
    default_image = bo.adb.get_cv2_img()
    for i in range(7):  # change if you have 6-7 troops
        default_color = default_image[260 + i * 50, 1097]
        x_click, y_click = uniform(1096, 1118), uniform(260 + i * 50, 275 + i * 50)
        bo.task.click(x_click, y_click)
        bo.task.better_sleep((1, 2))
        new_image = bo.task.adb.get_cv2_img()
        if (default_color != new_image[260 + i * 50, 1097]).all():
            print(f"Troop {i + 1} is selected")
        else:
            print(f"Troop {i + 1} is not selected")
    # bo.hunt.select_lineup_color(color="red")
    # bo.gem.run()
    exit()

    screen = imread("./screen_city_hall.png")

    x, y = data["0"]["schedules"]["1"].get("city_hall_position")
    label_y = max(0, y - 200)
    label_x_left = max(0, x - 100)
    label_x_right = min(720, x + 100)
    roi = screen[label_y:y, label_x_left:label_x_right]

    # Convert the ROI to grayscale
    gray = cvtColor(roi, COLOR_BGR2GRAY)

    # Threshold the grayscale image
    _, thresh = threshold(gray, 0, 255, THRESH_BINARY | THRESH_OTSU)

    # Invert the thresholded image
    thresh = bitwise_not(thresh)

    # Define the list of Tesseract configurations to test
    configurations = [
        "--oem 1 --psm 3",
        "--oem 1 --psm 4",
        "--oem 1 --psm 6",
        "--oem 3 --psm 3",
        "--oem 3 --psm 4",
        "--oem 3 --psm 6",
        "--oem 3 --psm 10"
    ]

    # Process the ROI with each configuration
    for config in configurations:
        print(f"Configuration: {config}")

        # Perform OCR with Tesseract
        text = pytesseract.image_to_string(thresh, config=config)
        print("Extracted text:")
        print(text)
        print()

        # Display the ROI with OpenCV (for visualization purposes)
        imshow('ROI', thresh)
        waitKey(0)  # Wait for any key press to close the window

    # Close all OpenCV windows
    destroyAllWindows()