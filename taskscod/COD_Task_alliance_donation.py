from random import randint, uniform

from pytesseract import pytesseract

from taskscod.COD_Task import Task
from utils.functions import get_class, get_name

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class AllianceDonation(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.data = MainTask.data
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
        self.better_sleep((1.7, 2.395))
        self.click(1100 + uniform(-5,5), 227 + uniform(-5,5))
        self.better_sleep((0.78, 1.095))
        self.click(25 + uniform(-2,2), 34 + uniform(-2,2))
        self.better_sleep((1.7, 2.395))

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

    def can_donate(self):
        co = self.find_img(target="cod_donate_button")
        screen = self.adb.get_cv2_img()
        screen = screen[co[1] - 30:co[1] - 8, co[0]:co[0] + 120]
        result = pytesseract.image_to_string(screen, config=fr'--oem 1 --psm 6')
        print(result)
        result = result.replace("\n","")
        try:
            tmp = result[-5:]
            print(tmp)
            tmp = tmp.split("/")
            print(tmp)
            if int(tmp[0]) != 0 and (int(tmp[0]) < int(tmp[1])):
                return True
            else:
                return False
        except:
            return False
    @get_name
    def donate_to_alliance(self):
        self.click(760 + uniform(-5,5), 537 + uniform(-5,5))
        self.better_sleep((1.725, 2.295))
        talked = False
        limit = 7
        current = 0

        while (co:=self.find_img(target="cod_donate_button")) and self.can_donate() :
            if not talked:
                self.print("Donating to the alliance")
                talked = True
            x, y, arg = co[0] + uniform(0, 20), co[1] + uniform(0, 10), randint(2500, 3475)
            self.swipe_arg(x, y, x, y, arg)
            self.better_sleep((0.7, 1.3))
            current += 1
            if current == limit:
                break
        self.click(uniform(1080, 1100), uniform(70, 90))
        self.better_sleep((1, 1.425))


    @get_class
    def run(self):
        self.open_alliance_menu()
        self.collect_alliance_resources()
        self.donate_to_alliance()
        self.close_windows()
