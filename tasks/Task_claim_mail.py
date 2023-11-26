import random
from random import uniform

import numpy as np
from PIL import Image

from tasks.Task import Task
from utils.functions import get_class


class ClaimMail(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.herite(MainTask)

    def task_name(self):
        return "ClaimMail"

    @get_class
    def run(self):
        screen = self.adb.get_cv2_img()
        lower_red = np.array([0, 0, 200])  # Adjust these values as needed
        upper_red = np.array([10, 10, 255])  # Adjust these values as needed

        if not (
            np.all(screen[551, 1263] >= lower_red)
            and np.all(screen[551, 1263] <= upper_red)
        ):
            return

        self.click(1230, 570)
        self.better_sleep((1, 2))

        pixel_list = [(150, 12), (310, 14), (468, 14), (618, 15)]
        random.shuffle(pixel_list)

        screen = self.adb.get_cv2_img()

        for pixel in pixel_list:
            selected_pixel = screen[pixel[1], pixel[0]]

            if np.all(selected_pixel >= lower_red) and np.all(
                selected_pixel <= upper_red
            ):
                self.click(pixel[0] - 20, 40)
                self.better_sleep((1, 2))
                self.click(111, 668)
                self.better_sleep((3, 4))
                if co := self.find_img(target="chest_confirm_button"):
                    self.click(*co)
                    self.better_sleep((1, 2))
        self.close_windows()
