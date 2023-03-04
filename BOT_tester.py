
from threading import Thread

import customtkinter

from Task import Task
from Task_academy_research import AcademyResearch
from Task_alliance_donation import AllianceDonation
from Task_claim_daily_quests import DailyQuests
from Task_daily_vip import DailyVip
from Task_rss_transfert import RssTransfert
from Task_runner import TaskRunner
from Task_upgrade_city import UpgradeCity
from bot_adb import *
from OLD_Tasks_lib import *
#from rkp import *
#from auto_upgrade import *

with open('user_settings.json') as config_file: data = json.load(config_file)
# with open('rkp_list.json') as config_file: data_rkp = json.load(config_file)

class Frame():
    def __init__(self,sel):
        self.pause = False
        self.stop = False
        self.sel = sel

class Bot():
    def __init__(self,adb):
        self.adb=adb
        self.device= adb.get_device()
        self.main_task= Task(Frame(adb.number)) #tasksGEM / tasks
        self.main_task.adb = adb
        #self.task = Tasks(self.adb)
        self.main_task.set_sel(str(adb.number))
        self.task = TaskRunner(self.main_task, self.main_task.frame)
        self.upgrade = UpgradeCity(self.main_task)
        self.research = AcademyResearch(self.main_task)
        self.quests = DailyQuests(self.main_task)
        self.vip = DailyVip(self.main_task)
        self.alliance = AllianceDonation(self.main_task)
        self.transfert = RssTransfert(self.main_task)
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
    bot.task.print = lambda txt: print(txt)
    bot.task.current_profile="1"
    frame = customtkinter.CTkFrame(master)
    frame.pr_tasks_button = customtkinter.CTkButton(master)
    frame.end_tasks_button = customtkinter.CTkButton(master)
    frame.pause = False
    frame.stop = False
    bot.task.frame = frame
    # bot.task.setup_view()
    # bot.task.better_sleep((0.9, 1.2))
    return bot
    while 0:
        while bot.adb.find_img("upgrade_stone") is not None or bot.adb.find_img("upgrade_stone2"):
            bot.upgrade.run()
        else:
            sleep(30)
            bot.upgrade.help_alliance()
    bot.task.dynamique_city_upgrade()
    bot.task.kill_emulator()

def upgrade_instance(number:int, master):
    adb = Adb(number)
    bot = Bot(adb)
    bot.adb.connect_to_device()

    bot.main_task.print = lambda txt: print(txt)
    bot.main_task.set_text = lambda txt: print(txt)
    bot.main_task.status = lambda txt: print(txt)
    bot.main_task.script_pause = lambda: print("")

    # bot.task.print = lambda txt: print(txt)
    # bot.task.set_text = lambda txt: print(txt)
    # bot.task.status = lambda txt: print(txt)
    # bot.task.script_pause = lambda: print("")
    #
    # bot.upgrade.script_pause = lambda: print("")
    # bot.upgrade.print = lambda txt: print(txt)
    # bot.upgrade.set_text = lambda txt: print(txt)
    # bot.upgrade.status = lambda txt: print(txt)
    # bot.upgrade.script_pause = lambda: print("")
    #
    # bot.quests.script_pause = lambda: print("")
    # bot.quests.print = lambda txt: print(txt)
    # bot.quests.set_text = lambda txt: print(txt)
    # bot.quests.status = lambda txt: print(txt)
    # bot.quests.script_pause = lambda: print("")



    bot.task.current_profile="1"
    # master = customtkinter.CTk()
    frame = customtkinter.CTkFrame(master)
    frame.pr_tasks_button = customtkinter.CTkButton(master, fg_color="white")
    frame.end_tasks_button = customtkinter.CTkButton(master)
    frame.adb = bot.adb
    frame.pause = False
    frame.stop = False
    frame.update_label2 = lambda x,_: print(x)
    bot.task.frame = frame
    bot.task.frame.pause = False
    bot.upgrade.setup_view()
    bot.task.better_sleep((0.9, 1.2))
    claim_allaince = randint(4000,6000)
    current_sec = 0
    while 1:
        while bot.upgrade.free_worker():
            bot.upgrade.run()
        else:
            sleep(60)
            current_sec += 60
            if current_sec>claim_allaince:
                bot.alliance.run()
                sleep(1)
                current_sec = 0
                claim_allaince = randint(4000, 6000)
            bot.upgrade.help_alliance()
            bot.upgrade.help_build()
            bot.quests.run()
            bot.vip.run()


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
    frame = customtkinter.CTkFrame(master)
    frame.pr_tasks_button = customtkinter.CTkButton(master)
    frame.end_tasks_button = customtkinter.CTkButton(master)
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
    frame = customtkinter.CTkFrame(master)
    frame.pr_tasks_button = customtkinter.CTkButton(master)
    frame.end_tasks_button = customtkinter.CTkButton(master)
    frame.adb = bot.adb
    frame.pause = False
    frame.stop = False

    frame.update_label2 = lambda x,_: print(x)
    bot.task.frame = frame
    # bot.task.setup_view()
    # bot.task.better_sleep((0.9, 1.2))
    bot.research.run()



if __name__ == "__main__":
    master = customtkinter.CTk()
    adb = Adb(2)
    bot = Bot(adb)
    bot.adb.connect_to_device()

    bot.main_task.print = lambda txt: print(txt)
    bot.main_task.set_text = lambda txt: print(txt)
    bot.main_task.status = lambda txt: print(txt)
    bot.main_task.script_pause = lambda: print("")
    bot.task.current_profile="1"
    master = customtkinter.CTk()
    frame = customtkinter.CTkFrame(master)
    frame.pr_tasks_button = customtkinter.CTkButton(master, fg_color="white")
    frame.end_tasks_button = customtkinter.CTkButton(master)
    frame.adb = bot.adb
    frame.pause = False
    frame.stop = False
    frame.update_label2 = lambda x,_: print(x)
    bot.task.frame.write = lambda _: _
    bot.task.frame = frame
    bot.task.frame.pause = False

    bot.transfert.run()


    master.mainloop()

