import random

import numpy as np
from PIL import Image

from tasks.Task import Task
from utils.functions import get_class


class ClaimMail(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.sel, MainTask.contextManager)
        self.herite(MainTask)

    def task_name(self):
        return "ClaimMail"

    @get_class
    def run(self):
        cord_x, cord_y = 1150, 640

        if ((co:=self.find_img("mail_button", confidence=0.8)) is None):
            self.open_menu()

        if co and co[0] > 1170:
            cord_x, cord_y = 1256, 640

        screen = self.adb.get_cv2_img()
        lower_red = np.array([0, 0, 200])  # Adjust these values as needed
        upper_red = np.array([0, 0, 255])  # Adjust these values as needed

        if not (np.all(screen[cord_y, cord_x] >= lower_red) and np.all(screen[cord_y, cord_x] <= upper_red)):
            return

        self.click(cord_x + random.uniform(-40, -30), cord_y + random.uniform(20, 30))
        self.better_sleep((1, 2))

        pixel_list = [(150, 12), (310, 14), (468, 14), (618, 15)]
        random.shuffle(pixel_list)

        screen = self.adb.get_cv2_img()

        for pixel in pixel_list:
            selected_pixel = screen[pixel[1], pixel[0]]

            if np.all(selected_pixel >= lower_red) and np.all(selected_pixel <= upper_red):
                self.click(pixel[0] - 20, 40)
                self.better_sleep((1, 2))
                self.click(111, 668)
                self.better_sleep((3, 4))
                if co := self.find_img(target="chest_confirm_button"):
                    self.click(*co)
                    self.better_sleep((1, 2))
        self.close_windows()
