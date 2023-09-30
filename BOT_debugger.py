import datetime
import json
from random import randint, uniform
from threading import Thread
from time import time

import cv2
import flet as ft
import numpy as np

import taskscod.COD_Task_daily_vip
from tasks.Task_claim_mail import ClaimMail
# from tasks.Task_title import Title
from tasks import Task_gather_rss_default
from tasks.Task_gather_gem_default import GatherGem
from tasks.Task_gather_rss_default import GatherRss
from tasks.Task_kingdom_ranking import KingdomRanking
from tasks.Task_maraudeurs import Marauders
# from taskscod import COD_Task_alliance_donation, COD_Task_training, COD_Task_clear_fog
# from taskscod.COD_Task_daily_chest import DailyChest
# from taskscod.COD_Task_gather_rss import GatherRss
from tasks.Task import Task
from tasks.Task_academy_research import AcademyResearch
from tasks.Task_alliance_donation import AllianceDonation
from tasks.Task_claim_daily_quests import DailyQuests
from tasks.Task_daily_chest2 import DailyChest2
from tasks.Task_daily_vip import DailyVip
from tasks.Task_rss_transfert import RssTransfer
from tasks.Task_runner import TaskRunner
from tasks.Task_upgrade_city import UpgradeCity
from tasks.Task_alliance_pit import AlliancePit
from utils.bot_adb import *

#from rkp import *
#from auto_upgrade import *
file  =  FileSingleton()

data = file.get_data()
# with open('rkp_list.json') as config_file: data_rkp = json.load(config_file)

class Frame():
    def __init__(self,sel):
        self.started = True
        self.stopped = False
        self.paused = False
        self.number = sel

    def add_text(self,phrase, color="black"):
        print(phrase)

    def set_text(self,phrase, color="black"):
        print(phrase)

    def get_text(self):
        return  ""
    def add_status(self, phrase, color="black"):
        return


class Bot():
    def __init__(self,adb):
        self.adb: Adb =adb
        self.device= adb.get_device()
        self.main_task= Task(Frame(adb.number)) #tasksGEM / tasks
        self.main_task.adb = adb
        #self.task = Tasks(self.adb)
        self.main_task.set_sel(str(adb.number))
        self.task = TaskRunner(self.main_task, self.main_task.tile)
        self.upgrade = UpgradeCity(self.main_task)
        self.rss  =  GatherRss(self.main_task)
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
        # self.cod_vip = taskscod.COD_Task_daily_vip.DailyVip(self.main_task)
        # self.cod_chest = DailyChest(self.main_task)
        # self.code_alliance = COD_Task_alliance_donation.AllianceDonation(self.main_task)
        # self.code_training = COD_Task_training.TroopTraining(self.main_task)
        # self.cod_scout = COD_Task_clear_fog.ClearFog(self.main_task)
        self.maraudeurs = Marauders(self.main_task)
        self.gem = GatherGem(self.main_task)
        # self.title = Title(self.main_task)
        #self.rkp = Rkp(self.adb)
        #self.rkp.set_sel('4')
        #self.up = Up(self.adb)
        #self.rkp.set_sel('3')

def lerp(p1: tuple, p2: tuple, points: int) -> list:
    '''
    Creates a list of points with len = points between p1 and p2 using lineal interpolation

    :param p1: First point.
    :param p2: Second point.
    :param points: Number of points in between.
    '''

    output = []
    header = [_p2 - _p1 for _p1, _p2 in zip(p1, p2)]
    for p in range(points + 1):
        percent = p / points
        output.append((p1[0] + percent * header[0], p1[1] + percent * header[1]))
    print(output)
    return output

class AdbInput:
    """
    Sends input events to a given adb device using ppadb and the sendevent shell command.
    """

    def __init__(self, bot : Bot, device: int = 0, eventId: int = 4):
        '''
        Creates an AdbInput object able to send inputs to an adb device
        :param client: The adb client.
        :param device: The index of the device (Default is 0)
        :param eventId: The event id. (Default is 2, change it if your device doesnt work)
        '''
        self.device = bot.device
        self.eventId = eventId

    def sendEvent(self, event: str):
        """
        Sends a raw adb event.
        :param event: The event. Composed by 3 DECIMAL numbers: Type Event Value
        """
        self.device.shell(f'sendevent /dev/input/event{self.eventId} {event}')

    def startTouch(self):
        """
        Starts a touch secuence
        (if you want to tap or swipe, use the functions \"tap\", \"swipe\" or \"smoothSwipe\")
        """

        # self.sendEvent('1 330 1')  # BTN_TOUCH Down
        # self.sendEvent('3 57 10')  # PRESSURE

    def setPosition(self, position: tuple):
        """
        Sends the POSITION_X and POSITION_Y events
        (if you want to tap or swipe, use the functions \"tap\" and \"swipe\")
        """

        self.sendEvent(f'3 53 {position[0]}')  # POSITION_X
        self.sendEvent(f'3 54 {position[1]}')  # POSITION_Y

    # Input functions
    def tap(self, position: tuple, duration: float = 0):
        """
        Taps the screen in the given location for a specific duration.
        :param position: The position to touch.
        :param duration: The duration of the tap.
        """

        # Start Tap
        self.startTouch()
        self.setPosition(position)
        self.sendEvent('0 0 0')  # SYN_REPORT
        self.device.shell(f'sleep {duration}')

        # End Tap
        self.sendEvent('1 330 0')  # BTN_TOUCH Up
        self.sendEvent('0 0 0')  # SYN_REPORT

    def swipe(self, positions: list):
        """
        Swipes in the screen going to the positions really fast
        :param positions: The points to reach
        """
        # Start the swipe
        self.startTouch()
        print("test")
        # Cycle through the positions
        for pos in positions:
            print(f"{pos = }")
            self.setPosition(pos)
            self.sendEvent('0 0 0')  # SYN_REPORT

        # End swipe
        self.sendEvent('1 330 0')  # BTN_TOUCH Up
        self.sendEvent('0 0 0')  # SYN_REPORT

    def smoothSwipe(self, positions: list, wait: float = 0, smoothness: int = 100):
        '''
        Swipes in the screen going to the positions \"smoothly\".

        :param positions: The points to reach.
        :param wait: The wait between touches (recomend using 0 or something really close)
        :param smoothness: The number of extra points added to each path to smooth it (Default = 10)
        '''

        # Get the needed points
        points = []
        for p in range(1, len(positions)):
            points += lerp(positions[p - 1] , positions[p] , smoothness)

        # Start swipe
        self.startTouch()

        # Cylce through points waiting the needed
        for point in points[:-1]:
            print(f"{point = }")
            self.setPosition(point)
            self.sendEvent('0 0 0')
            # self.device.shell(f'sleep {wait}')

        # End swipe
        self.sendEvent('1 330 0')  # BTN_TOUCH Up
        self.sendEvent('0 0 0')
        self.sendEvent('0000 0002 00000000')
        self.sendEvent('0000 0000 00000000')# SYN_REPORT
        self.sendEvent('0000 0002 00000000')
        self.sendEvent('0000 0000 00000000')# SYN_REPORT

def create_instance(number:int, master):
    adb = Adb(number)
    bot = Bot(adb)
    bot.adb.connect_to_device()
    bot.task.set_status = lambda text, color=None: print(f"[ {bot.task.name} ] Status = {text}")
    bot.task.print = lambda text, color=None: print(f"[ {bot.task.name} ] {text}")
    bot.task.current_profile="1"
    frame = object()
    frame.pr_tasks_button = object()
    frame.end_tasks_button = object()
    frame.pause = False
    frame.stop = False
    bot.task.frame = frame
    # bot.task.setup_view()
    # bot.task.better_sleep((0.9, 1.2))
    return bot

class FakeText():
    def __init__(self):
        self.value = ""

    def update(self):
        return

class lightTile():
    def ___init__(self, **kwargs):
        super().__init__(**kwargs)

        with open('user_settings.json') as config_file:
            data = json.load(config_file)

        self.started = True
        self.stopped = False
        self.text_status = FakeText()

def upgrade_instance(number:int):
    adb = Adb(number)
    bot = Bot(adb)
    bot.adb.connect_to_device()

    bot.main_task.print = lambda txt: print(txt)
    bot.main_task.set_text = lambda txt: print(txt)
    bot.main_task.status = lambda txt: print(txt)
    bot.main_task.script_pause = lambda: print("")




    bot.task.current_profile="1"
    # Page = customtkinter.CTk()
    frame = Frame(number)
    frame.number = number
    frame.stopped = False
    frame.started = True
    frame.add_text = lambda x,_: print(x)
    frame.set_text = lambda x, _: print(x)
    frame.get_text = ""
    bot.task.tile = frame
    bot.task.tile.stopped = False
    bot.upgrade.setup_view()
    bot.task.better_sleep((0.9, 1.2))
    claim_allaince = randint(4000,6000)
    current_sec = 0
    while 1:
        bot.task.run_game()
        while bot.upgrade.free_worker():
            bot.upgrade.run()
        else:
            sleep(60)
            current_sec += 60
            bot.alliance.close_windows()
            if current_sec > claim_allaince:
                bot.alliance.run()
                sleep(1)
                current_sec = 0
                claim_allaince = randint(4000, 6000)
            bot.upgrade.help_alliance()
            bot.upgrade.help_build()
            bot.quests.run()
            bot.vip.run()
            bot.chest.run()

def rss_transfert(number:int, type:str, amount: int):
    adb = Adb(number)
    bot = Bot(adb)
    bot.adb.connect_to_device()

    bot.main_task.print = lambda txt: print(txt)
    bot.main_task.set_text = lambda txt: print(txt)
    bot.main_task.status = lambda txt: print(txt)
    bot.main_task.script_pause = lambda: print("")




    bot.task.current_profile="1"
    # Page = customtkinter.CTk()
    frame = Frame(number)
    frame.number = number
    frame.stopped = False
    frame.started = True
    frame.add_text = lambda x,_: print(x)
    frame.set_text = lambda x, _: print(x)

    bot.task.tile = frame
    bot.task.tile.stopped = False
    bot.trade.run(type,amount)

def quest_instance(number:int, master):
    adb = Adb(number)
    bot = Bot(adb)
    bot.adb.connect_to_device()
    bot.task.print = lambda txt: print(txt)
    bot.task.set_text = lambda txt: print(txt)
    bot.task.status = lambda txt: print(txt)
    bot.task.script_pause = lambda: print("")
    bot.upgrade.script_pause = lambda: print("")
    bot.upgrade.print = lambda txt: print(txt)
    bot.upgrade.set_text = lambda txt: print(txt)
    bot.upgrade.status = lambda txt: print(txt)
    bot.upgrade.script_pause = lambda: print("")
    bot.quests = DailyQuests(bot.main_task)
    bot.quests.script_pause = lambda: print("")
    bot.quests.print = lambda txt: print(txt)
    bot.quests.set_text = lambda txt: print(txt)
    bot.quests.status = lambda txt: print(txt)
    bot.quests.script_pause = lambda: print("")



    bot.task.current_profile="1"
    # master = customtkinter.CTk()
    frame = object()
    frame.pr_tasks_button = object()
    frame.end_tasks_button = object()
    frame.adb = bot.adb
    frame.pause = False
    frame.stop = False
    frame.update_label2 = lambda x,_: print(x)
    bot.task.frame = frame
    # bot.task.setup_view()
    # bot.task.better_sleep((0.9, 1.2))
    print(bot.quests.run())


def research_instance(number:int, master):
    adb = Adb(number)
    bot = Bot(adb)
    bot.adb.connect_to_device()
    bot.task.print = lambda txt: print(txt)
    bot.task.set_text = lambda txt: print(txt)
    bot.task.status = lambda txt: print(txt)
    bot.task.script_pause = lambda: print
    bot.upgrade.script_pause = lambda: print
    bot.upgrade.print = lambda txt: print(txt)
    bot.upgrade.set_text = lambda txt: print(txt)
    bot.upgrade.status = lambda txt: print(txt)
    bot.upgrade.script_pause = lambda: print
    bot.research.script_pause = lambda: print
    bot.research.print = lambda txt: print(txt)
    bot.research.set_text = lambda txt: print(txt)
    bot.research.status = lambda txt: print(txt)
    bot.research.script_pause = 5
    bot.task.current_profile="1"
    # master = customtkinter.CTk()
    frame = object()
    frame.pr_tasks_button = object()
    frame.end_tasks_button = object()
    frame.adb = bot.adb
    frame.pause = False
    frame.stop = False

    frame.update_label2 = lambda x,_: print(x)
    bot.task.frame = frame
    # bot.task.setup_view()
    # bot.task.better_sleep((0.9, 1.2))
    bot.research.run()

# def stop_start_emulators(master):
#     instances = [
#         create_instance(3, master),
#         # create_instance(4, master),
#         # create_instance(5, master)
#     ]
#     # while True:
#     # for i in instances:
#     threads = []
#     while True:
#         for instance in instances:
#             instance.task.start_emulator()
#             sleep(60)
#             instance.task.run_game()
#             t = Thread(target=lambda: instance.task.dynamique_city_upgrade())
#             t.start()
#             t.join()
#             instance.adb.home_button()
#             sleep(2)
#             instance.task.kill_emulator()
#         sleep(uniform(900, 1200))

def main(page:ft.Page):
    # Thread(target=lambda: upgrade_instance(page,8)).start()
    Thread(target=lambda: upgrade_instance(page,9)).start()
    Thread(target=lambda: upgrade_instance(page,10)).start()
    Thread(target=lambda: upgrade_instance(page,11)).start()
    # Thread(target=lambda: upgrade_instance(page,12)).start()
    # Thread(target=lambda: upgrade_instance(page,13)).start()

def get_bot(number):
    adb = Adb(number)
    bot = Bot(adb)
    bot.adb.connect_to_device()

    bot.main_task.print = lambda txt: print(txt)
    bot.main_task.set_text = lambda txt: print(txt)
    bot.main_task.status = lambda txt: print(txt)
    bot.main_task.script_pause = lambda: print("")




    bot.task.current_profile="1"
    # Page = customtkinter.CTk()
    frame = Frame(number)
    frame.number = number
    frame.stopped = False
    frame.started = True
    frame.paused = False
    frame.add_text = lambda x,_: print(x)
    frame.set_text = lambda x, _: print(x)

    bot.task.tile = frame
    bot.task.tile.stopped = False
    return bot

def upgrade_all():
    Thread(target=lambda: upgrade_instance(3)).start()
    Thread(target=lambda: upgrade_instance(4)).start()
    Thread(target=lambda: upgrade_instance(5)).start()
    Thread(target=lambda: upgrade_instance(6)).start()
    Thread(target=lambda: upgrade_instance(7)).start()
    Thread(target=lambda: upgrade_instance(8)).start()
    # Thread(target=lambda: upgrade_instance(9)).start()
    # Thread(target=lambda: upgrade_instance(10)).start()
    # Thread(target=lambda: upgrade_instance(11)).start()
    # Thread(target=lambda: upgrade_instance(12)).start()
    # Thread(target=lambda: upgrade_instance(13)).start()


if __name__ == "__main__":
    # upgrade_all()

    bot =  get_bot(0)
    bot.maraudeurs.recall(5)
    exit()
    template = cv2.imread('./barb_icon2.png')


    result = cv2.matchTemplate(bot.adb.get_cv2_img(), template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc =  cv2.minMaxLoc(result)

    print(max_val)
    print(max_loc)
    exit()

    image = cv2.imread('notification.png')[:86,:]

    lower_red = np.array([45, 45, 195])  # Adjust these values as needed
    upper_red = np.array([80, 80, 255])  # Adjust these values as needed

    # Get the shape of the image
    height, width, _ = image.shape

    # Initialize a list to store the coordinates of red pixels
    red_pixel_coordinates = []

    # Iterate through the image pixels
    start = time()
    for y in range(height):
        for x in range(width):
            pixel = image[y, x]
            if np.all(pixel >= lower_red) and np.all(pixel <= upper_red):
                red_pixel_coordinates.append((x, y))
    print(time() - start)
    # Print the coordinates of red pixels
    # for x, y in red_pixel_coordinates:
        # print(f"Red Pixel at X = {x}, Y = {y}")
