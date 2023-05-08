from random import uniform, shuffle

from pytesseract import pytesseract

from taskscod.COD_Task import Task
from utils.Task_utils import get_data

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class TroopTraining(Task):
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
        return "TroopTraining"

    def run(self):
        names = ['infantry','cavalry','archery',"siege"]
        pos = {
            "t1":[160,627],
            "t2": [265, 627],
            "t3": [375, 627],
            "t4": [475, 627],
            "t5": [580, 627],
        }
        shuffle(names)
        for name in names:
            print(name)
            if self.data[str(self.sel)]['schedules'][str(self.current_profile)][f"{name}_enable"]:
                position = self.data[str(self.sel)]['schedules'][str(self.current_profile)][f"{name}_camp"]
                print(position)
                if position is None or len(list(position))<2:
                    continue
                print("here")
                for i in range(2):
                    self.click(position[0]+uniform(-8,8),position[1]+uniform(-8,8))
                    self.better_sleep((1.2,3))
                if (co:=self.find_img(target=f"cod_{name}_badge",confidence=0.75)) is None:
                    self.print(f"Unable to locate {name}")
                    continue
                if self.find_img(target=f"cod_training_speed",confidence=0.8) is not None:
                    self.print(f"Already training {name}")
                    continue
                self.click(co[0] + uniform(-8, 8), co[1] + uniform(-8, 8))
                self.better_sleep((1.2, 2.3))
                co = pos[self.data[str(self.sel)]['schedules'][str(self.current_profile)][f"{name}_tier"]]
                self.click(co[0] + uniform(-15, 15), co[1] + uniform(-15, 15))
                self.better_sleep((1.2, 2.3))
                self.click(uniform(1000,1100),uniform(615,650))
                self.better_sleep((1.2, 2.3))
                self.close_windows()