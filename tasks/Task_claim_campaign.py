from random import uniform

import cv2
from tasks.Task import Task
from utils.Task_utils import get_class, get_data
from utils.easyOcr import Reader


class ClaimCampaign(Task):
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
        return "ClaimCampaign"

    def has_notification(self):
        cv_image = self.adb.get_cv2_img()
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
        cropped_image = cv_image[630:655, 841:865]

        number = self.extract_text(img=cropped_image, allowlist="12345670.")
        print(number)
        if '.' in number:
            return True
        try:
            return int(number) > 15
        except Exception as e:
            return False

    @get_class
    def run(self):
        # Open du menu
        if self.find_img(target='menu_opened', confidence=0.8) is None:
            x, y = uniform(1200, 1250), uniform(650, 690)
            self.click(x, y)
            self.better_sleep((1.725, 1.995))

        if self.has_notification():
            self.click(uniform(808, 850), uniform(651, 692))
            self.better_sleep((1.3, 2.2))
            self.click(uniform(150, 266), uniform(250, 390))
            self.better_sleep((1.3, 2.2))
            self.click(uniform(101, 149), uniform(208, 255))
            self.better_sleep((1.3, 2.2))
            co = self.find_img(target="chest_confirm_button")
            if co is not None:
                self.print("Claiming the daily rewards from the expedition.")
                self.click(co[0] + uniform(0, 149), co[1] + uniform(0, 20))
                self.better_sleep((1.3, 2.2))
            for _ in range(2):
                self.click(uniform(21, 56), uniform(14, 58))
                self.better_sleep((1.3, 2.2))