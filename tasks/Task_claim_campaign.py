from random import shuffle, uniform

import cv2

from tasks.Task import Task
from utils.functions import get_class

# from utils.easyOcr import Reader


class ClaimCampaign(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.sel, MainTask.contextManager)
        self.herite(MainTask)
        self.context_task = self.context_profile.tasks.claim_daily_expedition_rewards

    def task_name(self):
        return "ClaimCampaign"

    def has_notification(self):
        cv_image = self.adb.get_screen()
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
        cropped_image = cv_image[630:655, 740:760]

        _, cropped_image = cv2.threshold(cropped_image, 128, 255, cv2.THRESH_BINARY_INV)

        # Remove small noise using morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        cropped_image = cv2.morphologyEx(cropped_image, cv2.MORPH_OPEN, kernel)

        number = self.extract_text(img=cropped_image, allowlist="0123456789.")

        if "." in number:
            return True
        try:
            return int(number) > 15
        except Exception as e:
            return False

    def is_new_shop_available(self):
        screen = self.adb.get_screen()
        if screen[93, 165][0] > 220 and screen[93, 165][1] == 0 and screen[93, 165][1] == 0:
            return True
        return False

    @get_class
    def run(self):
        # Open du menu
        self.open_menu()
        if self.has_notification():
            self.click(uniform(700,740), uniform(651, 692))
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
                if self.context_task.enable_buy_items or self.context_task.enable_buy_heads:
                    self.click(160, 100)
                    self.better_sleep((1.3, 2.2))

                    items = [(626, 466), (800, 466), (990, 466), (626, 600), (800, 600), (990, 600)]
                    ethel = (1000, 275)
                    refresh = (1040, 330)
                    shuffle(items)

                    if self.context_task.enable_buy_heads:
                        for i in range(3):
                            self.click(ethel[0] + uniform(-3, 3), ethel[1] + uniform(-3, 3))
                            self.better_sleep((0.7, 1.2))

                    if self.context_task.enable_buy_items:
                        for i in range(2):
                            for item in items:
                                self.click(item[0] + uniform(-3, 3), item[1] + uniform(-3, 3))
                                self.better_sleep((0.7, 1.2))
                            if i == 0:
                                self.click(refresh[0], refresh[1])
                                self.better_sleep((0.7, 1.2))

            self.close_windows()
