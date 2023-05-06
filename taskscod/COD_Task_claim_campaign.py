
from random import uniform

import cv2
from pytesseract import pytesseract

from tasks.Task import Task
from utils.Task_utils import get_class, get_data

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'

class ClaimCampaign(Task):
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
        return "ClaimCampaign"

    @get_class
    def run(self):
        # Open du menu
        if self.find_img(target='menu_opened', confidence=0.8) is None:
            x, y = uniform(1200, 1250), uniform(650, 690)
            self.click(x, y)
            self.better_sleep((1.725, 1.995))
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image =self.pil_to_array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        cropped_image = cv_image[630:660, 843:895]

        number = pytesseract.image_to_string(cropped_image, config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=12345670.')
        # print(number)
        if not '.' in number:
            try:
                condition = int(number) > 15
            except Exception as e:
                condition = False
            if condition:
                self.click(uniform(808, 850), uniform(651, 692))
                self.better_sleep((1.3, 2.2))
                self.click(uniform(150, 266), uniform(250, 390))
                self.better_sleep((1.3, 2.2))
                self.click(uniform(101, 149), uniform(208, 255))
                self.better_sleep((1.3, 2.2))
                co = self.find_img(target="chest_confirm_button")
                if co is not None:
                    self.click(co[0] + uniform(0, 149), co[1] + uniform(0, 20))
                    self.better_sleep((1.3, 2.2))
                for _ in range(2):
                    self.click(uniform(21, 56), uniform(14, 58))
                    self.better_sleep((1.3, 2.2))