from time import sleep, time

from random import uniform, randint

from pytesseract import pytesseract

from taskscod.COD_Task import Task
from utils.functions import get_class

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'

class ClearFog(Task):
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
        return "ClearFog"

    @get_class
    def run(self, starting_time=None):
        self.data = self.update_data()
        self.leave_city()
        self.better_sleep((1, 1.895))
        self.go_city()
        if starting_time is None:
            starting_time = time()
        if self.data[str(self.sel)]['schedules'][self.current_profile].get('scout_duration1', 60) > \
                self.data[str(self.sel)]['schedules'][self.current_profile].get('scout_duration2', 90):
            self.data[self.sel]['schedules'][self.current_profile]['scout_duration1'], \
                self.data[self.sel]['schedules'][self.current_profile]['scout_duration2'] = \
                self.data[self.sel]['schedules'][self.current_profile]['scout_duration2'], \
                    self.data[self.sel]['schedules'][self.current_profile]['scout_duration1']

        generated_time = (
                randint(self.data[str(self.sel)]['schedules'][self.current_profile].get('scout_duration1'),
                        self.data[str(self.sel)]['schedules'][self.current_profile].get('scout_duration2')) * 60)
        time_to_beat = starting_time + generated_time
        self.print(f"Clearing fog for ~{generated_time // 60} minutes")
        in_scout_camp = False
        said = False
        while time_to_beat > time():
            if self.check_log_back():
                self.print(f"You interrupted fog exploration by connecting from an other device, bot is restarting it")
                return self.run(starting_time)
            self.check_reconnect()
            if not in_scout_camp:
                scout =self.data[str(self.sel)]['schedules'][self.current_profile]["scout_camp"]
                # scout = (700,190)
                self.click(scout[0],scout[1])
                self.better_sleep((1.2,1.5))
                co = self.find_img("cod_scout_camp_icon",confidence=0.75)
                if not co:
                    self.close_windows()
                    return self.print("Unable to locate the scout camp","red")
                self.click(co[0], co[1])
                self.better_sleep((1.25, 1.75))
                said = False
                # co = self.find_img(target="scout_button")
                # for _ in range(2):
                #     if co is None:
                #         self.print("Unable to find the scout button")
                #         sleep(5)
                #         co = self.find_img(target="scout_button")
                # if co is None:
                #     co = self.find_img(target="scout_button2")
                #     for _ in range(2):
                #         if co is None:
                #             self.print("Unable to find the scout button")
                #             sleep(5)
                #             co = self.find_img(target="scout_button2")
                # if co is None:
                #     self.print("Unable to find the scout button, try to place the building in the center of your city so the bot can see the icons.")
                #     return
                # self.click(uniform(co[0], co[0] + 30), uniform(co[1], co[1] + 30))
                # self.better_sleep((3, 4.5))

            co = self.find_img(target="cod_scout_explore_button_in")
            if co is not None:
                self.click(uniform(co[0], co[0] + 100), uniform(co[1], co[1] + 25))
                self.better_sleep((3, 4.5))
                co = self.find_img(target="cod_scout_explore_button_out")
                if co is not None:
                    self.click(uniform(co[0], co[0] + 60), uniform(co[1], co[1] + 30))
                    self.better_sleep((3, 4.5))
                co = self.find_img(target="cod_march_button_out")
                if co is not None:
                    self.click(uniform(co[0], co[0] + 90), uniform(co[1], co[1] + 30))
                    self.better_sleep((3, 4.5))
                self.print("Scout sent !","green")
                self.go_city()
                self.better_sleep((3, 4.5))
                in_scout_camp = False
            else:
                time_to_sleep = randint(5, 10)
                if not said:
                    self.print(f"All scout seems occupied, waiting for the scout to be free..")
                    said = True
                in_scout_camp = True
                for _ in range(time_to_sleep):
                    self.script_pause()
                    sleep(1)
        self.close_windows()