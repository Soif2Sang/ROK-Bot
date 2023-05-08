from random import uniform,randint

from pytesseract import pytesseract

from taskscod.COD_Task import Task
from utils.Task_utils import get_class, get_name, get_data

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class AllianceDonation(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
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
        return "AllianceDonation"

    @get_name
    def collect_alliance_resources(self) -> None:
        self.print("Collecting the alliance resources")
        self.click(927 + uniform(0, 20), 375 + uniform(0, 10))
        self.better_sleep((1.0, 1.395))
        self.click(1100 + uniform(-5,5), 227 + uniform(-5,5))
        self.better_sleep((0.78, 1.095))
        self.click(25 + uniform(-2,2), 34 + uniform(-2,2))
        self.better_sleep((1.0, 1.395))

    @get_name
    def open_alliance_menu(self):
        # Open du menu
        if self.find_img(target='cod_toolbar', confidence=0.8) is None:
            x, y = uniform(1200, 1250), uniform(650, 690)
            self.click(x, y)
            self.better_sleep((1.725, 1.995))
        # Open alliance menu
        x, y = 960 + uniform(-5, 5), uniform(650, 680)
        self.click(x, y)
        self.better_sleep((1.725, 2.295))

    @get_name
    def donate_to_alliance(self):
        self.click(760 + uniform(-5,5), 537 + uniform(-5,5))
        self.better_sleep((1, 1.425))
        talked = False
        while (co:=self.find_img(target="cod_donate_button")):
            if not talked:
                self.print("Donating to the alliance")
                talked = True
            x, y, arg = co[0] + uniform(0, 20), co[1] + uniform(0, 10), randint(2500, 3475)
            self.swipe_arg(x, y, x, y, arg)
            self.better_sleep((0.7, 1.3))
        # Check if the resources pop-up comes
        if self.find_img(target="get_more_rss") is not None:
            self.click(uniform(1000, 1020), uniform(129, 148))
            self.better_sleep((1, 1.425))
        self.click(uniform(1080, 1100), uniform(70, 90))
        self.better_sleep((1, 1.425))


    @get_class
    def run(self):
        self.open_alliance_menu()
        self.collect_alliance_resources()
        self.donate_to_alliance()
        self.close_windows()
